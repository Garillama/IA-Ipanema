"""Real namespace tests; no model inference, account access or credentials."""
from pathlib import Path
import json
import tempfile
import unittest

from tests.support import ROOT
from ipanema.core import IpanemaError
from ipanema.orchestration.isolation import command, probe, run_isolated


class Isolation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='ipanema worker isolation ')
        self.root = Path(self.tmp.name)
        self.snapshot = self.root / 'snapshot'
        self.snapshot.mkdir()
        (self.snapshot / 'allowed.txt').write_text('public fixture')

    def tearDown(self):
        self.tmp.cleanup()

    def test_environment_is_explicit_and_provider_scoped(self):
        args, env = command(['/bin/true'], self.snapshot, provider='codex')
        self.assertNotIn('SSH_AUTH_SOCK', env)
        self.assertNotIn('OPENAI_API_KEY', env)
        self.assertEqual(env['HOME'], '/worker-home')
        self.assertIn('--remount-ro', args)
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='claude', auth_env={'OPENAI_API_KEY': 'synthetic'})

    def test_private_snapshots_and_escaping_links_are_rejected(self):
        for name in ('.git', '.env.local', '.nuvem', 'ipanema.local.json'):
            p = self.snapshot / name; p.write_text('fixture')
            with self.assertRaises(IpanemaError):
                command(['/bin/true'], self.snapshot, provider='codex')
            p.unlink()
        link = self.snapshot / 'escape'; link.symlink_to('/etc')
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='codex')

    def test_home_mount_or_auth_destination_escape_rejected(self):
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='codex', runtime_paths=[Path.home()])
        own = self.root / 'own-auth-fixture.json'; own.write_text('{}')
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='codex', auth_files={own: '../other'})
        args, env = command(['/bin/true'], self.snapshot, provider='codex', auth_files={own: '.codex/auth.json'})
        self.assertIn('/worker-home/.codex/auth.json', args)
        self.assertNotIn('{}', args)

    def require_namespace(self):
        if not probe()['available']:
            self.skipTest('bwrap/user namespaces unavailable; no insecure fallback')

    def test_real_snapshot_read_only_host_hidden_and_tmp_writable(self):
        self.require_namespace()
        script = """import json,pathlib
root=pathlib.Path('/workspace')
denied=[]
for target in ('/workspace/allowed.txt','/unexpected-worker-file'):
 try:pathlib.Path(target).write_text('changed')
 except OSError:denied.append(target)
pathlib.Path('/tmp/own').write_text('ok')
print(json.dumps({'content':root.joinpath('allowed.txt').read_text(),'denied':denied,'host_home_visible':pathlib.Path('/home').exists(),'host_git_visible':pathlib.Path('/workspace/.git').exists()}))
"""
        result = run_isolated(['/usr/bin/python3', '-c', script], '', self.snapshot, provider='codex', network=False)
        self.assertEqual(result['exit_code'], 0, result['stderr'])
        self.assertIn('public fixture', result['stdout'])
        self.assertIn('"host_home_visible": false', result['stdout'])
        self.assertIn('"host_git_visible": false', result['stdout'])
        self.assertEqual((self.snapshot / 'allowed.txt').read_text(), 'public fixture')

    def test_real_time_and_output_limits(self):
        self.require_namespace()
        timeout = run_isolated(['/bin/sleep', '3'], '', self.snapshot, provider='codex', timeout=1, network=False)
        self.assertTrue(timeout['timed_out'])
        oversized = run_isolated(['/usr/bin/python3', '-c', 'print("x"*100000)'], '', self.snapshot,
                                 provider='codex', network=False, max_output_bytes=2048)
        self.assertTrue(oversized['output_limited'])
        self.assertLessEqual(len(oversized['stdout'].encode()) + len(oversized['stderr'].encode()), 2048)

    def test_real_prompt_stdin_and_auth_file_mounted_read_only(self):
        self.require_namespace()
        own = self.root / 'own-auth-fixture.json'; own.write_text('{"fixture":true}')
        script = "import pathlib,sys; p=pathlib.Path('/worker-home/.codex/auth.json'); print(sys.stdin.read()); print(p.exists());\ntry:p.write_text('x')\nexcept OSError:print('auth-readonly')"
        result = run_isolated(['/usr/bin/python3', '-c', script], 'bounded task packet', self.snapshot,
            provider='codex', auth_files={own: '.codex/auth.json'}, network=False)
        self.assertEqual(result['exit_code'], 0, result['stderr'])
        self.assertIn('bounded task packet', result['stdout']); self.assertIn('auth-readonly', result['stdout'])
        self.assertEqual(own.read_text(), '{"fixture":true}')

    def test_qa_cannot_enable_network_or_auth(self):
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='qa', network=True)
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='qa', network=False, auth_env={'OPENAI_API_KEY': 'fixture'})
        own = self.root / 'own-auth-fixture.json'; own.write_text('{}')
        with self.assertRaises(IpanemaError):
            command(['/bin/true'], self.snapshot, provider='qa', network=False, auth_files={own: 'auth.json'})

    def test_real_qa_json_stdout_and_private_artifacts(self):
        self.require_namespace()
        script = """import json,os,pathlib,sys
p=pathlib.Path('/tmp/qa-artifact.json')
p.write_text(json.dumps({'checks':[{'status':'passed'}]}))
print(json.dumps({'qa':json.loads(p.read_text()),'prompt_length':len(sys.stdin.read()),'home':os.getenv('HOME'),'unicode':'verificación'}))
"""
        result = run_isolated(['/usr/bin/python3', '-c', script], 'context' * 20000,
                              self.snapshot, provider='qa', network=False)
        self.assertEqual(result['exit_code'], 0, result['stderr'])
        report = json.loads(result['stdout'])
        self.assertEqual(report['qa']['checks'][0]['status'], 'passed')
        self.assertEqual(report['prompt_length'], len('context' * 20000))
        self.assertEqual(report['home'], '/worker-home')
        self.assertEqual(report['unicode'], 'verificación')
        self.assertFalse((self.snapshot / 'qa-artifact.json').exists())


if __name__ == '__main__':
    unittest.main()
