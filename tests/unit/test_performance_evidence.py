"""Offline evidence contracts: missing timings never become invented attribution."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import unittest
from tests.support import ROOT


@unittest.skipUnless(shutil.which('node'), 'Node optional runtime unavailable')
class PerformanceEvidenceTests(unittest.TestCase):
    def run_node(self, body):
        module=(ROOT/'tools/performance_evidence.mjs').as_uri()
        result=subprocess.run(['node','--input-type=module','-e',
            f'import {{installPerformanceObservers,lighthouseEvidence,createNetworkRecorder}} from {json.dumps(module)};\n'+body],
            text=True,capture_output=True,timeout=20,check=True)
        return json.loads(result.stdout)

    def test_missing_lighthouse_insights_are_not_measured(self):
        result=self.run_node('console.log(JSON.stringify(lighthouseEvidence({audits:{}})));')
        self.assertEqual(result['audits'],{})
        self.assertIn('lcp-breakdown-insight',result['not_available'])
        self.assertIsNone(result['field_inp'])
        self.assertNotIn('percentages',result)

    def test_lighthouse_preserves_actual_breakdown_and_redacts_private_data(self):
        result=self.run_node('''
          console.log(JSON.stringify(lighthouseEvidence({audits:{
           'lcp-breakdown-insight':{score:0,details:{items:[{ttfb:250,resourceLoadDelay:100,resourceLoadDuration:500,elementRenderDelay:75}]}},
           'network-requests':{details:{items:[{url:'https://user:pass@fixture.test/img.png?token=private-token&width=500',snippet:'private-node-html'}]}}
          } })));''')
        item=result['audits']['lcp-breakdown-insight']['details']['items'][0]
        self.assertEqual(item['ttfb'],250)
        self.assertEqual(item['elementRenderDelay'],75)
        encoded=json.dumps(result)
        for private in ('private-token','private-node-html','user:pass'):
            self.assertNotIn(private,encoded)
        self.assertIn('width=500',encoded)

    def test_observer_preserves_image_identity_and_existing_longtasks(self):
        result=self.run_node('''
          globalThis.window={}; globalThis.location={href:'https://fixture.test/'};
          const callbacks={};globalThis.PerformanceObserver=class{
           constructor(callback){this.callback=callback;}observe(options){callbacks[options.type]=this.callback;}
          };
          installPerformanceObservers();
          const img={tagName:'IMG',id:'hero-image',currentSrc:'https://fixture.test/hero.webp?token=private',loading:'eager',fetchPriority:'high',
           getAttribute:key=>({sizes:'100vw',srcset:'https://fixture.test/hero.webp?token=private 640w'}[key]),
           closest:()=>({querySelectorAll:()=>[{media:'(max-width:767px)',type:'image/webp',sizes:'100vw',srcset:'https://fixture.test/mobile.webp 640w'}]})};
          callbacks['largest-contentful-paint']({getEntries:()=>[{startTime:800,duration:0,size:9000,url:img.currentSrc,renderTime:800,loadTime:650,element:img}]});
          callbacks.longtask({getEntries:()=>[{startTime:900,duration:75}]});
          console.log(JSON.stringify(window.__audit));''')
        row=result['lcp'][0]
        self.assertEqual((row['tag'],row['id'],row['loadTime'],row['renderTime']),('IMG','hero-image',650,800))
        self.assertEqual(row['sizes'],'100vw')
        self.assertEqual(row['sources'][0]['media'],'(max-width:767px)')
        self.assertNotIn('private',json.dumps(result))
        self.assertEqual(result['longTasks'][0]['duration'],75)

    def test_text_lcp_has_no_fabricated_resource_url(self):
        result=self.run_node('''
          globalThis.window={};globalThis.location={href:'https://fixture.test/'};
          let callback;globalThis.PerformanceObserver=class{
           constructor(cb){this.cb=cb;}observe(options){if(options.type==='largest-contentful-paint')callback=this.cb;}
          };installPerformanceObservers();callback({getEntries:()=>[{startTime:500,duration:0,size:100,element:{tagName:'H1',id:'heading'}}]});
          console.log(JSON.stringify(window.__audit.lcp[0]));''')
        self.assertIsNone(result['url'])
        self.assertIsNone(result['currentSrc'])
        self.assertEqual(result['tag'],'H1')

    def test_network_retains_every_redirect_hop_and_snapshot(self):
        result=self.run_node('''
          const network=createNetworkRecorder(value=>value.replace('private-token','[redacted]'));
          network.requestWillBeSent({requestId:'1',timestamp:1,type:'Image',request:{url:'https://fixture.test/start?token=private-token',method:'GET'}},'navigation');
          network.requestWillBeSent({requestId:'1',timestamp:2,type:'Image',request:{url:'https://fixture.test/step',method:'GET'},redirectResponse:{status:301,mimeType:'text/plain',encodedDataLength:100}},'navigation');
          const before=network.snapshot();
          network.requestWillBeSent({requestId:'1',timestamp:3,type:'Image',request:{url:'https://fixture.test/final',method:'GET'},redirectResponse:{status:302,mimeType:'text/plain',encodedDataLength:200}},'navigation');
          network.responseReceived({requestId:'1',timestamp:4,response:{status:200,mimeType:'image/png'}});
          network.loadingFinished({requestId:'1',timestamp:5,encodedDataLength:300});
          console.log(JSON.stringify({before,after:network.snapshot()}));''')
        rows=result['after']
        self.assertEqual([row['status'] for row in rows],[301,302,200])
        self.assertEqual([row['redirect_hop'] for row in rows],[0,1,2])
        self.assertEqual(sum(row['encoded_bytes'] for row in rows),600)
        self.assertNotIn('private-token',json.dumps(result))
        self.assertNotIn('status',result['before'][1])
        self.assertEqual(rows[0]['encoded_bytes_basis'],'redirectResponse.encodedDataLength')
        self.assertEqual(rows[2]['encoded_bytes_basis'],'loadingFinished.encodedDataLength')

    def test_redirect_without_byte_measurement_is_not_a_zero(self):
        result=self.run_node('''
          const network=createNetworkRecorder();
          network.requestWillBeSent({requestId:'1',timestamp:1,type:'Document',request:{url:'https://fixture.test/final',method:'GET'},redirectResponse:{url:'https://fixture.test/start',status:302,mimeType:'text/plain'}},'navigation');
          network.loadingFailed({requestId:'1',timestamp:2,errorText:'net::ERR_ABORTED'});
          console.log(JSON.stringify(network.snapshot()));''')
        self.assertTrue(result[0]['missing_request_event'])
        self.assertIsNone(result[0]['encoded_bytes'])
        self.assertFalse(result[1]['completed'])

    def test_browser_records_navigation_and_image_redirects(self):
        doctor=subprocess.run(['node',str(ROOT/'tools/browser_runtime.mjs'),'--doctor'],capture_output=True,text=True,timeout=20)
        if doctor.returncode or not json.loads(doctor.stdout).get('chrome'):
            self.skipTest('Optional browser runtime unavailable')
        from ipanema.compare import write_png
        with tempfile.TemporaryDirectory(prefix='ipanema-redirect-fixture-') as folder:
            root=Path(folder);write_png(root/'image.png',60,30,bytes([0,90,160,255])*60*30)
            picture=(root/'image.png').read_bytes()
            class Handler(BaseHTTPRequestHandler):
                def log_message(self,*args):pass
                def do_GET(self):
                    redirect={'/start':(301,'/step'),'/step':(302,'/page'),'/image-start':(301,'/image-step'),'/image-step':(302,'/image.png')}
                    if self.path in redirect:
                        status,destination=redirect[self.path];self.send_response(status);self.send_header('Location',destination);self.send_header('Content-Length','0');self.end_headers();return
                    body=picture if self.path=='/image.png' else b'<!doctype html><html lang="es"><head><title>Redirect fixture</title><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><h1>Fixture</h1><img src="/image-start" alt="Fixture" width="60" height="30"></body></html>'
                    self.send_response(200);self.send_header('Content-Type','image/png' if self.path=='/image.png' else 'text/html');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
            http=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
            try:
                base=f'http://127.0.0.1:{http.server_port}'
                job={'project':'fixture','output':str(root/'out'),'pages':[{'name':'home','url':base+'/start','expect_canonical':False}],'widths':[390],'mode':'quick','axe':False}
                (root/'job.json').write_text(json.dumps(job))
                env={k:v for k,v in os.environ.items() if not k.startswith('IPANEMA_') or k in ('IPANEMA_NODE_MODULE_ROOT','IPANEMA_CHROME_PATH')}
                env.update({'IPANEMA_PUBLIC_URL':base,'IPANEMA_EVIDENCE_DIR':str(root/'out'),'IPANEMA_ALLOW_NETWORK':'0'})
                run=subprocess.run(['node',str(ROOT/'tools/qa_browser.mjs'),str(root/'job.json')],env=env,capture_output=True,text=True,timeout=60)
                self.assertEqual(run.returncode,0,(run.stdout,run.stderr))
                record=json.loads((root/'out/home-390-rendered.json').read_text())
                rows=record['navigation_network']
                for kind,paths in [('Document',['/start','/step','/page']),('Image',['/image-start','/image-step','/image.png'])]:
                    hops=[row for row in rows if row['type']==kind]
                    self.assertEqual([row['url'].removeprefix(base) for row in hops],paths)
                    self.assertEqual([row['status'] for row in hops],[301,302,200])
                    self.assertEqual([row['redirect_hop'] for row in hops],[0,1,2])
                    self.assertTrue(all(row['completed'] for row in hops))
                    self.assertTrue(all(row['encoded_bytes'] is not None for row in hops))
                self.assertEqual(record['network_metrics']['image_bytes'],sum(row['encoded_bytes'] for row in rows if row['type']=='Image' and row['completed']))
                self.assertEqual(record['network_metrics']['requests'],len(rows))
            finally:
                http.shutdown();http.server_close();thread.join(timeout=3)
