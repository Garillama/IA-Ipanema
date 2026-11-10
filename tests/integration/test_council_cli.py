"""Portable council CLI planning. No models, credentials or remote services."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.support import ROOT, make_project


class CouncilCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="council CLI ")
        self.root = make_project(Path(self.tmp.name) / "agent with spaces", theme=False)
        shutil.copytree(ROOT / "tools", self.root / "tools", ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "AGENTS.md").write_text("Synthetic offline agent. No remote mutations.\n")
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("IPANEMA_")}

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / "tools/ia.py"), "orchestrate", *args],
            cwd=self.tmp.name, env=self.env, capture_output=True, text=True, timeout=20,
        )

    def plan(self, request, *options):
        run = self.cli("plan", request, "--scope", "workspace", "--file", "copy.txt", *options)
        self.assertEqual(run.returncode, 0, run.stderr)
        value = json.loads(run.stdout)
        self.assertFalse(value["execution_performed"])
        plan = json.loads(Path(value["plan"]).read_text())
        return plan

    def test_auto_preserves_single_fast_worker_for_simple_task(self):
        plan = self.plan("Corrige una errata")
        self.assertEqual(plan["classification"]["level"], "L1")
        self.assertFalse(plan["council"]["enabled"])
        self.assertEqual(len(plan["tasks"]), 1)

    def test_full_requests_three_participants_without_starting_them(self):
        plan = self.plan("Corrige una errata", "--council", "full", "--council-rounds", "2")
        self.assertTrue(plan["council"]["enabled"])
        self.assertEqual(plan["council"]["max_rounds"], 2)
        self.assertTrue(all(task["state"] == "pending" for task in plan["tasks"]))

    def test_high_risk_defaults_to_council_even_in_read_only_plan(self):
        plan = self.plan("Audita arquitectura compartida", "--read-only")
        self.assertEqual(plan["classification"]["level"], "L3")
        self.assertTrue(plan["council"]["enabled"])
        self.assertTrue(plan["read_only"])
        self.assertFalse(any(task["allowed_files"] for task in plan["tasks"]))

    def test_invalid_round_budget_and_high_risk_opt_out_are_rejected(self):
        for args in (
            ("plan", "Audita arquitectura compartida", "--scope", "workspace", "--file", "copy.txt", "--council", "off"),
            ("plan", "Corrige una errata", "--scope", "workspace", "--file", "copy.txt", "--council-rounds", "3"),
        ):
            with self.subTest(args=args):
                run = self.cli(*args)
                self.assertEqual(run.returncode, 2)

    def test_council_plan_still_requires_execute_for_inference(self):
        run = self.cli("plan", "Audita arquitectura compartida", "--scope", "workspace", "--file", "copy.txt")
        self.assertEqual(run.returncode, 0, run.stderr)
        plan_path = json.loads(run.stdout)["plan"]
        denied = self.cli("run", plan_path)
        self.assertEqual(denied.returncode, 2)
        self.assertIn("--execute", denied.stderr)


if __name__ == "__main__":
    unittest.main()
