import argparse
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from tests.support import ROOT,make_project
from tests.unit.test_seo_crawler_v4 import HOME,doc
from ipanema.core import Project,IpanemaError
from ipanema.seo.crawl_policy import Limits
from ipanema.seo.engineering import execute,_pilot_manifest,_supervise_pilot


def sleeping_worker(project,args):
    # No sockets or HTTP. Fake a durable started event, then exercise process
    # group cleanup for a TERM-resistant worker and descendant.
    signal.signal(signal.SIGTERM,signal.SIG_IGN)
    args._closed_checkpoint({'event':'started','ordinal':1,'url':HOME+'robots.txt'})
    run=args._closed_checkpoint_path.parent
    child=subprocess.Popen([sys.executable,'-c',"import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(180)"])
    (run/'descendant.pid').write_text(str(child.pid))
    while True:time.sleep(.05)


def parsing_stall(project,args):
    signal.signal(signal.SIGTERM,signal.SIG_IGN)
    while True:sum(range(10000))


def export_stall(project,args):
    from unittest.mock import patch
    from ipanema.seo import engineering
    def stalled(*a,**k):
        signal.signal(signal.SIGTERM,signal.SIG_IGN)
        while True:time.sleep(.01)
    with patch.object(engineering,'export',stalled):return engineering._execute(project,args)


class PilotCLI(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.project=Project(make_project(self.root,theme=False))
        self.targets=[HOME+'target-'+str(i) for i in range(5)]
        self.manifest=self.root/'targets.json';self.manifest.write_text(json.dumps({'project':self.project.id,'origin':HOME.rstrip('/'),'targets':[{'url':u} for u in self.targets]}))
        pages={HOME+'robots.txt':{'status':200,'body':'User-agent: *'}};pages.update({u:{'status':200,'body':doc('/'+u.rsplit('/',1)[1])} for u in self.targets})
        self.responses=self.root/'responses.json';self.responses.write_text(json.dumps({'project':self.project.id,'home':HOME,'responses':pages}))

    def tearDown(self):self.tmp.cleanup()

    def args(self,seconds=20):
        return argparse.Namespace(seo_command='crawl',allow_network=False,responses=self.responses,targets_manifest=self.manifest,
                targets_sha256=hashlib.sha256(self.manifest.read_bytes()).hexdigest(),**(dataclasses.asdict(Limits())|{'max_seconds':seconds}))

    def test_closed_offline_execute_supervised_and_exported(self):
        result,code=execute(self.project,self.args());self.assertEqual(code,0,result)
        data=json.loads(Path(result['report']).read_text());self.assertEqual(data['selected_scope'],self.targets)
        self.assertEqual([r['url'] for r in data['provenance']['request_log']],[HOME+'robots.txt',*self.targets])
        checkpoint=json.loads(Path(data['checkpoint']).read_text());self.assertEqual(len(checkpoint['requests']),6)
        self.assertTrue(all(r['state']=='completed' for r in checkpoint['requests']))

    def test_real_cli_parses_closed_flags_without_network(self):
        shutil.copytree(ROOT/'tools',self.root/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_')}
        z=subprocess.run([sys.executable,str(self.root/'tools/ia.py'),'seo','crawl','--targets-manifest',str(self.manifest),
              '--targets-sha256',self.args().targets_sha256,'--responses',str(self.responses),'--max-seconds','20'],
              cwd=self.root,env=env,capture_output=True,text=True,timeout=25)
        self.assertEqual(z.returncode,0,z.stderr);data=json.loads(z.stdout)
        report=json.loads(Path(data['report']).read_text());self.assertEqual(report['selected_scope'],self.targets)
        self.assertEqual(len(report['provenance']['request_log']),6)

    def test_hash_and_project_rejected_without_requests(self):
        args=self.args();args.targets_sha256='0'*64
        with self.assertRaises(IpanemaError):_pilot_manifest(self.project,args)
        data=json.loads(self.manifest.read_text());data['project']='wrong';self.manifest.write_text(json.dumps(data))
        with self.assertRaises(IpanemaError):_pilot_manifest(self.project,self.args())

    def test_invalid_manifest_cli_returns_stopped(self):
        args=self.args();args.targets_sha256='0'*64
        result,code=execute(self.project,args);self.assertEqual(code,2);self.assertEqual(result['reason'],'worker_failed')
        path=Path(result['checkpoint']);self.assertFalse(path.exists())

    def test_missing_paired_flag_rejected(self):
        args=self.args();args.targets_manifest=None
        with self.assertRaises(IpanemaError):execute(self.project,args)

    def assert_cancel(self,work,seconds):
        start=time.monotonic();result,code=_supervise_pilot(self.project,self.args(seconds),work=work);elapsed=time.monotonic()-start
        self.assertEqual(code,2);self.assertEqual(result['reason'],'absolute_deadline');self.assertLess(elapsed,seconds+1)
        receipt=json.loads(Path(result['supervision']).read_text());self.assertTrue(receipt['worker_reaped'])
        return result,elapsed

    def test_real_short_process_group_cancellation(self):
        result,elapsed=self.assert_cancel(sleeping_worker,1)
        checkpoint=json.loads(Path(result['checkpoint']).read_text());self.assertEqual(checkpoint['requests'][0]['state'],'started_without_confirmed_result')
        self.assertEqual(sum(v=='pending' for v in checkpoint['planned'].values()),5)
        pid=int((Path(result['checkpoint']).parent/'descendant.pid').read_text());time.sleep(.1)
        status=Path('/proc')/str(pid)/'stat'
        self.assertTrue(not status.exists() or status.read_text().split()[2]=='Z','descendant still active')

    def test_interrupting_supervisor_cancels_worker_and_descendant(self):
        import multiprocessing
        result_path=self.root/'interrupted.json'
        def run():
            result,code=_supervise_pilot(self.project,self.args(10),work=sleeping_worker)
            result_path.write_text(json.dumps({'result':result,'code':code}))
        driver=multiprocessing.get_context('fork').Process(target=run);driver.start()
        try:
            deadline=time.monotonic()+4
            files=[]
            while time.monotonic()<deadline:
                files=list(self.project.evidence_root.glob('pilot-checkpoint-*/descendant.pid'))
                if files:break
                time.sleep(.01)
            self.assertTrue(files)
            os.kill(driver.pid,signal.SIGTERM);driver.join(3);self.assertFalse(driver.is_alive())
            z=json.loads(result_path.read_text());self.assertEqual(z['code'],2)
            receipt=json.loads(Path(z['result']['supervision']).read_text());self.assertTrue(receipt['worker_reaped'])
            pid=int(files[0].read_text());status=Path('/proc')/str(pid)/'stat'
            self.assertTrue(not status.exists() or status.read_text().split()[2]=='Z')
        finally:
            if driver.is_alive():driver.kill();driver.join()

    def test_deadline_covers_parsing(self):self.assert_cancel(parsing_stall,1)
    def test_deadline_covers_export(self):self.assert_cancel(export_stall,1)

    @unittest.skipUnless(os.environ.get('IPANEMA_PILOT_FULL_120_TEST')=='1','explicit real 120-second fixture only')
    def test_real_120_second_process_group_cancellation(self):
        result,elapsed=self.assert_cancel(sleeping_worker,120)
        checkpoint=json.loads(Path(result['checkpoint']).read_text());self.assertEqual(checkpoint['requests'][0]['state'],'started_without_confirmed_result')
        pid=int((Path(result['checkpoint']).parent/'descendant.pid').read_text());time.sleep(.1)
        status=Path('/proc')/str(pid)/'stat';self.assertTrue(not status.exists() or status.read_text().split()[2]=='Z')
        proof={'elapsed_seconds':elapsed,'limit_seconds':120,'worker_reaped':True,'descendant_pid':pid,'descendant_active':False,'HTTP_requests':0,'checkpoint_states':[x['state'] for x in checkpoint['requests']]}
        destination=os.environ.get('IPANEMA_PILOT_120_RECEIPT')
        if destination:Path(destination).write_text(json.dumps(proof,indent=2))
