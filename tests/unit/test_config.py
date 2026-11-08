import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.support import make_project, put
from ipanema.core import IpanemaError, Project, doctor, redact, resolve_path, safe_url, write_json
from ipanema.qa import browser_job


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ipanema config ")
        self.root = make_project(Path(self.tmp.name))
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_relative_theme_and_root_independent_of_cwd(self):
        project = Project(self.root)
        self.assertEqual(project.require_theme(), self.root / "theme")
        self.assertEqual(project.id, "sample")

    def test_precedence_and_multiple_projects(self):
        registry = {"schema_version": 2, "default": "sample", "projects": {"sample": "projects/sample.json", "second": "projects/second.json"}}
        put(self.root / "projects/registry.json", registry)
        second = json.loads((self.root / "projects/sample.json").read_text())
        second["id"] = "second"
        put(self.root / "projects/second.json", second)
        put(self.root / ".local/config.json", {"active_project": "second"})
        self.assertEqual(Project(self.root).id, "second")
        os.environ["IPANEMA_PROJECT"] = "sample"
        self.assertEqual(Project(self.root).id, "sample")
        self.assertEqual(Project(self.root, "second").id, "second")

    def test_theme_override_is_local(self):
        put(self.root / "projects/sample.local.json", {"theme_root": "other-theme"})
        self.assertEqual(Project(self.root).theme_root, self.root / "other-theme")
        os.environ["IPANEMA_THEME_ROOT"] = str(self.root / "theme")
        self.assertEqual(Project(self.root).require_theme(), self.root / "theme")

    def test_missing_theme_allows_knowledge_mode(self):
        os.environ["IPANEMA_THEME_ROOT"] = str(self.root / "missing")
        project = Project(self.root)
        self.assertFalse(doctor(project)["theme_available"])
        self.assertTrue(doctor(project)["warnings"])
        with self.assertRaises(IpanemaError):
            project.require_theme()

    def test_incomplete_or_unregistered_config(self):
        with self.assertRaises(IpanemaError):
            Project(self.root, "absent")
        put(self.root / "projects/sample.json", {})
        with self.assertRaises(IpanemaError):
            Project(self.root)

    def test_unresolved_environment_and_path_escape(self):
        with self.assertRaises(IpanemaError):
            resolve_path("${IPANEMA_UNDEFINED}/theme", self.root)
        put(self.root / "projects/registry.json", {"schema_version": 2, "default": "sample", "projects": {"sample": "../outside.json"}})
        with self.assertRaises(IpanemaError):
            Project(self.root)

    def test_refuses_evidence_in_theme_or_discovery(self):
        path = self.root / "projects/sample.json"
        data = json.loads(path.read_text())
        for dest in ("theme/evidence", "ipanema-discovery/new-evidence"):
            data["evidence_dir"] = dest
            put(path, data)
            with self.assertRaises(IpanemaError):
                Project(self.root)

    def test_no_credentials_in_project_or_url(self):
        path = self.root / "projects/sample.json"
        data = json.loads(path.read_text())
        data["password"] = "fake-test-value"
        put(path, data)
        with self.assertRaises(IpanemaError):
            Project(self.root)
        for url in ("https://user:pass@example.com", "https://example.com/?token=abc", "http://example.com"):
            with self.assertRaises(IpanemaError):
                safe_url(url)
        self.assertEqual(safe_url("http://127.0.0.1:1234/"), "http://127.0.0.1:1234/")
        self.assertEqual(redact({"password": "test", "cookie": "test"}), {"password": "[redacted]", "cookie": "[redacted]"})

    def test_network_requires_explicit_permission_and_origin(self):
        p = Project(self.root)
        with self.assertRaises(IpanemaError):
            browser_job(p, self.root / "run")
        job = browser_job(p, self.root / "run", allow_network=True)
        self.assertEqual(job["pages"][0]["url"], "https://example.invalid/")
        p.qa["pages"]["bad"] = "https://other.invalid/"
        with self.assertRaises(IpanemaError):
            browser_job(p, self.root / "run", pages=["bad"], allow_network=True)

    def test_secret_masking_does_not_corrupt_job_paths(self):
        os.environ['IPANEMA_AUDIT_PASSWORD'] = 'sample'
        destination = self.root/'job.json'
        write_json(destination, {'project':'sample','output':'reports/sample','error':'credential sample'})
        result=json.loads(destination.read_text())
        self.assertEqual(result['project'],'sample')
        self.assertEqual(result['output'],'reports/sample')
        self.assertNotIn('sample',result['error'])


if __name__ == "__main__":
    unittest.main()
