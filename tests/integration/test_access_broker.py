"""Aislamiento OS real del transporte; no inferencia ni cuenta Google."""
import json
from pathlib import Path
import tempfile
import unittest

from tests.support import ROOT, make_project
from ipanema.core import Project
from ipanema.access.policy import Policy
from ipanema.access.broker import TaskBroker
from ipanema.orchestration.isolation import probe, run_isolated


class BrokerBoundary(unittest.TestCase):
    @unittest.skipUnless(probe()['available'], 'Bubblewrap no disponible')
    def test_worker_only_sees_bound_socket_not_policy_or_other_project(self):
        with tempfile.TemporaryDirectory(prefix='ia broker ') as folder:
            root = Path(folder)
            project = Project(make_project(root/'repo', theme=False))
            policy = Policy(project)
            grant = policy.issue('codex','fixture',['devtools.read'],allow_network=True)
            snapshot = root/'view'; snapshot.mkdir()
            endpoint = root/'task.sock'
            broker = TaskBroker(project,grant['id'],endpoint)
            try:
                script = '''import json,socket
from pathlib import Path
assert not Path(%s).exists()
assert not Path(%s).exists()
s=socket.socket(socket.AF_UNIX);s.connect(%s);f=s.makefile('rw')
for i,method,params in [(1,'initialize',{'protocolVersion':'2025-06-18'}),(2,'tools/list',{}),(3,'tools/call',{'name':'gsc_sitemaps','arguments':{'request':{}}})]:
 f.write(json.dumps({'jsonrpc':'2.0','id':i,'method':method,'params':params})+'\\n');f.flush()
 result=json.loads(f.readline())
 if i==2: assert all(t['name'].startswith('devtools_') for t in result['result']['tools'])
 if i==3: assert result['result']['isError']
print('BOUNDARY_VERIFIED')
''' % (repr(str(policy.root)),repr(str(Path.home()/'.codex/auth.json')),repr(str(endpoint)))
                raw = run_isolated(['/usr/bin/python3','-c',script], '', snapshot,
                                   runtime_paths=[str(endpoint)],provider='codex',timeout=15,network=False)
                self.assertEqual(raw['exit_code'],0,raw['stderr'])
                self.assertIn('BOUNDARY_VERIFIED',raw['stdout'])
                self.assertTrue(any(e['event']=='tools/list' for e in broker.events))
            finally:
                broker.close()


if __name__ == '__main__':
    unittest.main()
