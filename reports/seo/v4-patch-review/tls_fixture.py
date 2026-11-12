"""TLS real solo en loopback. El reenvío de socket existe únicamente en este fixture.

No reduce la política DNS del motor, ni hace tráfico al dominio de la tienda.
"""
import http.server
import ssl
import socket
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from ipanema.seo.crawl_policy import _https_get_once
from ipanema.core import IpanemaError

class LocalTLS(unittest.TestCase):
    def test_local_tls_get_headers_hostname_and_rejection(self):
        with tempfile.TemporaryDirectory(prefix='seo-v4-local-tls-') as folder:
            base=Path(folder);key=base/'key.pem';cert=base/'cert.pem'
            subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','1','-subj','/CN=example.invalid',
                '-addext','subjectAltName=DNS:example.invalid','-keyout',str(key),'-out',str(cert)],check=True,capture_output=True,timeout=15)
            requests=[]
            class Handler(http.server.BaseHTTPRequestHandler):
                def log_message(self,*args):pass
                def do_GET(self):
                    requests.append({'method':self.command,'path':self.path,'host':self.headers.get('Host'),'cookie':self.headers.get('Cookie'),'auth':self.headers.get('Authorization')})
                    body=b'<main>Local TLS fixture</main>'
                    self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(body)))
                    self.send_header('X-Robots-Tag','otherbot: noindex');self.send_header('X-Robots-Tag','max-image-preview:none')
                    self.end_headers();self.wfile.write(body)
            server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
            server_context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);server_context.load_cert_chain(cert,key)
            sni=[];server_context.set_servername_callback(lambda sock,name,ctx:sni.append(name))
            server.socket=server_context.wrap_socket(server.socket,server_side=True)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            real_connect=socket.create_connection;real_context=ssl.create_default_context;pinned=[]
            def connect(address,timeout=None,*args,**kwargs):
                pinned.append(address);self.assertEqual(address,('8.8.8.8',443))
                return real_connect(('127.0.0.1',server.server_port),timeout)
            def context():return real_context(cafile=str(cert))
            try:
                with patch('ipanema.seo.crawl_policy.public_addresses',return_value=['8.8.8.8']),patch('socket.create_connection',side_effect=connect),patch('ssl.create_default_context',side_effect=context):
                    row=_https_get_once('https://example.invalid/a?page=2',timeout=2,max_bytes=1000)
                    self.assertEqual(row['status'],200);self.assertIn(b'Local TLS',row['body'])
                    self.assertEqual(row['headers']['x-robots-tag'],['otherbot: noindex','max-image-preview:none'])
                    with self.assertRaises(IpanemaError):_https_get_once('https://wrong.invalid/',timeout=2,max_bytes=1000)
                self.assertEqual(len(requests),1)
                self.assertEqual(requests[0],{'method':'GET','path':'/a?page=2','host':'example.invalid','cookie':None,'auth':None})
                self.assertEqual(sni,['example.invalid','wrong.invalid'])
                self.assertEqual(len(pinned),2)
            finally:
                server.shutdown();server.server_close();thread.join(timeout=5)

if __name__=='__main__':unittest.main(verbosity=2)
