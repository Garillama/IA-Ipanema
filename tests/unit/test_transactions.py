from pathlib import Path
import tempfile
import unittest

from tests.support import make_project, put
from ipanema.core import IpanemaError, Project, digest, now
from ipanema import transactions as tx


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ipanema attempt ")
        self.root = make_project(Path(self.tmp.name))
        self.project = Project(self.root)
        self.name = "sections/hero.tpl"
        self.file = self.root / "theme" / self.name
        self.original = self.file.read_bytes()

    def tearDown(self):
        self.tmp.cleanup()

    def start(self, **kwargs):
        return tx.begin(self.project, [self.name], authorized=True, **kwargs)["id"]

    def test_requires_local_authorization(self):
        with self.assertRaises(IpanemaError):
            tx.begin(self.project, [self.name])

    def test_restores_preexisting_changes_not_git_head(self):
        self.file.write_text("cambio previo del usuario")
        attempt = self.start()
        tx.apply(self.project, attempt, {self.name: "cambio del intento"})
        tx.finish(self.project, attempt)
        self.assertEqual(self.file.read_text(), "cambio previo del usuario")

    def test_conflict_before_apply_preserves_file(self):
        attempt = self.start()
        self.file.write_text("otro cambio")
        with self.assertRaises(IpanemaError):
            tx.apply(self.project, attempt, {self.name: "patch"})
        self.assertEqual(self.file.read_text(), "otro cambio")

    def test_conflict_after_apply_refuses_rollback(self):
        attempt = self.start()
        tx.apply(self.project, attempt, {self.name: "propio"})
        self.file.write_text("tercero")
        with self.assertRaises(IpanemaError):
            tx.finish(self.project, attempt)
        self.assertEqual(self.file.read_text(), "tercero")

    def test_bounded_attempts(self):
        attempt = self.start(max_attempts=1)
        tx.apply(self.project, attempt, {self.name: "intento"})
        tx.finish(self.project, attempt)
        self.assertEqual(self.file.read_bytes(), self.original)
        with self.assertRaises(IpanemaError):
            tx.apply(self.project, attempt, {self.name: "otro"})

    def test_new_file_removed_only_if_owned(self):
        name = "sections/new.tpl"
        attempt = tx.begin(self.project, [name], authorized=True)["id"]
        tx.apply(self.project, attempt, {name: "nuevo"})
        tx.finish(self.project, attempt)
        self.assertFalse((self.root / "theme" / name).exists())

    def test_symlinks_and_sensitive_paths_rejected(self):
        for name in ("../escape", ".nuvem", ".git/config", ".env", "projects/sample.local.json"):
            with self.assertRaises(IpanemaError):
                tx.begin(self.project, [name], authorized=True)
        try:
            (self.root / "theme/link.tpl").symlink_to(self.file)
        except OSError:
            self.skipTest("Sistema sin permiso de symlink")
        with self.assertRaises(IpanemaError):
            tx.begin(self.project, ["link.tpl"], authorized=True)

    def test_accept_requires_post_change_qa_with_matching_hash(self):
        attempt = self.start()
        baseline = self.root / "baseline.json"
        put(baseline, {"kind": "qa", "project": "sample", "outcome": "failed", "at": now(), "checks": [{"name": "fixture", "status": "failed"}]})
        tx.apply(self.project, attempt, {self.name: "propio"})
        report = self.root / "report.json"
        put(report, {"kind": "qa", "project": "sample", "outcome": "passed", "at": now(), "checks": [{"name": "fixture", "status": "passed"}]})
        with self.assertRaises(IpanemaError):
            tx.finish(self.project, attempt, accept=True, evidence=report)
        put(report, {"kind": "qa", "project": "sample", "outcome": "passed", "at": now(), "checks": [{"name": "fixture", "status": "passed"}],
                     "verification_state": {"theme": {self.name: digest(self.file)}}})
        self.assertEqual(tx.finish(self.project, attempt, accept=True, evidence=report, baseline=baseline)["status"], "accepted")
        self.assertEqual(self.file.read_text(), "propio")
