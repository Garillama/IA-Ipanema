import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.support import ROOT, make_project, put


class CLIPortabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="ipanema relocated ")
        cls.root = Path(cls.tmp.name) / "agent with spaces"
        cls.root.mkdir()
        for folder in ("tools", "projects", ".agents", "reusable"):
            shutil.copytree(ROOT/folder, cls.root/folder, ignore=shutil.ignore_patterns("__pycache__", "*.local.json"))
        # Knowledge/evidence se copian completas; no se depende de su ruta original.
        shutil.copytree(ROOT/"ipanema-discovery", cls.root/"ipanema-discovery")
        for name in ("AGENTS.md", "README.md"):
            shutil.copy2(ROOT/name, cls.root/name)
        cls.env = {k: v for k, v in os.environ.items() if not k.startswith("IPANEMA_")}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(self.root/"tools/ia.py"), *args], cwd=cwd or self.root,
                              env=self.env, capture_output=True, text=True, timeout=30)

    def test_original_entry_runs_from_another_cwd(self):
        run = subprocess.run([sys.executable, str(ROOT/"tools/ia.py"), "--project", "ipanema", "projects", "list"],
                             cwd=self.tmp.name, env=self.env, capture_output=True, text=True, timeout=20)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["active"], "ipanema")

    def test_relocated_without_theme_starts_and_searches(self):
        run = self.run_cli("--project", "ipanema", "doctor", cwd=self.tmp.name)
        self.assertEqual(run.returncode, 0, run.stderr)
        status = json.loads(run.stdout)
        self.assertFalse(status["theme_configured"])
        self.assertFalse(status["network_performed"])
        search = self.run_cli("--project", "ipanema", "search", "hero", "--limit", "1")
        self.assertEqual(search.returncode, 0, search.stderr)
        self.assertEqual(json.loads(search.stdout)["components"][0]["path"], "sections/hero.tpl")

    def test_incomplete_config_exits_cleanly(self):
        registry = json.loads((self.root/"projects/registry.json").read_text())
        registry["projects"]["broken"] = "projects/broken.json"
        put(self.root/"projects/registry.json", registry)
        put(self.root/"projects/broken.json", {})
        result = self.run_cli("--project", "broken", "doctor")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("incompleta", json.loads(result.stderr)["error"])

    def test_register_and_select_multiple_projects(self):
        run = self.run_cli("projects", "register", "other", "--name", "Otra tienda", "--url", "https://example.invalid")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(json.loads(run.stdout)["remote_connection_checked"])
        run = self.run_cli("projects", "use", "other")
        self.assertEqual(run.returncode, 0, run.stderr)
        run = self.run_cli("projects", "list")
        result = json.loads(run.stdout)
        self.assertEqual(result["active"], "other")
        self.assertIn("ipanema", result["projects"])
        self.assertTrue((self.root/".local/config.json").is_file())

    def test_unauthorized_remote_qa_never_launches(self):
        run = self.run_cli("--project", "ipanema", "qa", "--suite", "page", "--page", "home")
        self.assertEqual(run.returncode, 2)
        self.assertIn("--allow-network", run.stderr)
        self.assertFalse((self.root/"reports/runs/ipanema").exists())


class SourceAuditIntegrationTests(unittest.TestCase):
    def test_static_audit_and_output_guards_preserve_source(self):
        with tempfile.TemporaryDirectory(prefix="ipanema source ") as folder:
            root = make_project(Path(folder))
            source = root/"theme"
            before = {str(p.relative_to(source)): p.read_bytes() for p in source.rglob("*") if p.is_file()}
            output = root/"capture"
            command = [sys.executable, str(ROOT/"tools/audit_source.py"), "--source", str(source), "--output", str(output)]
            run = subprocess.run(command, capture_output=True, text=True, timeout=20)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["sections"], 1)
            evidence = (output/"source-inventory.json").read_bytes()
            self.assertEqual(subprocess.run(command, capture_output=True, timeout=20).returncode, 2)
            self.assertEqual((output/"source-inventory.json").read_bytes(), evidence)
            nested = command[:-1] + [str(source/"bad")]
            self.assertEqual(subprocess.run(nested, capture_output=True, timeout=20).returncode, 2)
            self.assertFalse((source/"bad").exists())
            self.assertEqual(before, {str(p.relative_to(source)): p.read_bytes() for p in source.rglob("*") if p.is_file()})

    def test_controlled_correction_runs_real_qa_reverts_then_accepts(self):
        with tempfile.TemporaryDirectory(prefix="ipanema correction ") as folder:
            root=make_project(Path(folder))
            shutil.copytree(ROOT/'tools',root/'tools',ignore=shutil.ignore_patterns('__pycache__'))
            put(root/'AGENTS.md','# Fixture local\n')
            put(root/'tools/arithmetic.py','def add(a,b):\n    return a-b\n')
            put(root/'tests/unit/test_arithmetic.py',"import sys, unittest\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))\nfrom arithmetic import add\nclass Arithmetic(unittest.TestCase):\n    def test_sum(self): self.assertEqual(add(2,3),5)\n")
            env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')}
            env['PYTHONDONTWRITEBYTECODE']='1'
            def cli(*args):
                return subprocess.run([sys.executable,str(root/'tools/ia.py'),*args],cwd=root,env=env,capture_output=True,text=True,timeout=30)
            baseline=cli('qa','--suite','unit')
            self.assertEqual(baseline.returncode,1)
            baseline_path=json.loads(baseline.stdout)['report']
            attempt=json.loads(cli('attempt','begin','--scope','workspace','--file','tools/arithmetic.py','--authorize-local').stdout)['id']
            put(root/'patch.json',{'tools/arithmetic.py':'def add(a,b):\n    return a*b\n'})
            self.assertEqual(cli('attempt','apply',attempt,'--patch',str(root/'patch.json')).returncode,0)
            failed=cli('attempt','verify',attempt,'--suite','unit','--baseline',baseline_path)
            self.assertEqual(failed.returncode,1,failed.stderr)
            self.assertEqual(json.loads(failed.stdout)['status'],'reverted')
            self.assertIn('a-b',(root/'tools/arithmetic.py').read_text())
            put(root/'patch.json',{'tools/arithmetic.py':'def add(a,b):\n    result = a + b\n    return result\n'})
            self.assertEqual(cli('attempt','apply',attempt,'--patch',str(root/'patch.json')).returncode,0)
            passed=cli('attempt','verify',attempt,'--suite','unit','--baseline',baseline_path)
            self.assertEqual(passed.returncode,0,passed.stderr)
            self.assertEqual(json.loads(passed.stdout)['status'],'accepted')
            self.assertEqual(json.loads(passed.stdout)['attempt'],2)
