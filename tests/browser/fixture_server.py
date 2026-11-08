"""Storefront sintético propio para pruebas locales; no simula APIs privadas."""
import contextlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
from urllib.parse import urlsplit

from tests.support import ROOT
from ipanema.compare import write_png


def html(bad=False, probe=False):
    canonical = '' if bad else '<link rel="canonical" href="/">'
    extra_h1 = '<div class="user-content"><h1>Otro encabezado</h1></div>' if bad else ''
    carousel_url = 'javascript:void(0)' if bad else '/category/'
    wide = 'width:2000px;' if bad else 'max-width:960px;'
    schema = '{invalid}' if bad else '{"@context":"https://schema.org","@type":"WebSite","name":"Fixture"}'
    escape = '' if bad else "document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.hidden=true;toggle.setAttribute('aria-expanded','false');toggle.focus();}});"
    post = "fetch('/commercial-probe',{method:'POST',body:'synthetic'}).catch(()=>{});" if probe else ''
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Fixture Ipanema QA</title><meta name="viewport" content="width=device-width, initial-scale=1">{canonical}<style>
*{{box-sizing:border-box}}body{{margin:0;color:#111;background:#fff;font:16px Arial,sans-serif}}header,footer,main{{padding:20px}}main{{{wide}margin:auto}}button,a{{min-height:44px;display:inline-flex;align-items:center;padding:12px;color:#111;background:#fff}}button{{border:1px solid #111}}a:focus,button:focus{{outline:3px solid #005fcc;outline-offset:2px}}[hidden]{{display:none!important}}#menu{{position:relative;padding:12px;border:1px solid}}img{{display:block;max-width:100%;height:auto}}.cards{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}@media(min-width:768px){{.cards{{grid-template-columns:repeat(4,minmax(0,1fr))}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none;transition:none}}}}
</style><script type="application/ld+json">{schema}</script></head><body><header><button id="menu-toggle" type="button" aria-expanded="false" aria-controls="menu">Abrir menú</button><nav id="menu" aria-label="Menú principal" hidden><a href="/category/">Categorías</a><a href="/product/">Producto</a></nav></header><main><h1>Fixture de tienda</h1>{extra_h1}<section aria-labelledby="hero-title"><h2 id="hero-title">Hero nativo de prueba</h2><picture><source media="(max-width:767px)" srcset="/mobile.png"><img src="/desktop.png" width="600" height="300" alt="Imagen de prueba" fetchpriority="high"></picture></section><section data-qa-carousel aria-labelledby="categories-title"><h2 id="categories-title">Categorías</h2><div class="cards"><a href="{carousel_url}" data-qa-order="category">Ver categoría</a><a href="/product/" data-product-id="fixture" data-qa-order="product">Ver producto</a></div></section></main><footer>Pruebas locales</footer><script>const toggle=document.querySelector('#menu-toggle'),menu=document.querySelector('#menu');toggle.addEventListener('click',()=>{{menu.hidden=!menu.hidden;toggle.setAttribute('aria-expanded',String(!menu.hidden));if(!menu.hidden)menu.querySelector('a').focus();}});{escape}{post}</script></body></html>'''


@contextlib.contextmanager
def server():
    with tempfile.TemporaryDirectory(prefix='ipanema-fixture-images-') as folder:
        image = Path(folder)/'image.png'
        write_png(image, 60, 30, bytes([0, 90, 160, 255])*60*30)
        picture = image.read_bytes()
        state = {'gets': [], 'posts': 0}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                route = urlsplit(self.path).path
                state['gets'].append(route)
                if route == '/rate-limited/':
                    self.send_response(429);self.end_headers();return
                self.send_response(200)
                if route.endswith('.png'):
                    self.send_header('Content-Type', 'image/png');body=picture
                elif route == '/favicon.ico':
                    self.send_header('Content-Type', 'image/x-icon');body=b''
                else:
                    self.send_header('Content-Type','text/html; charset=utf-8')
                    body=html(bad=route=='/broken/',probe='probe=post' in self.path).encode()
                self.send_header('Content-Length',str(len(body)));self.end_headers()
                try:self.wfile.write(body)
                except (BrokenPipeError,ConnectionResetError):pass

            def do_POST(self):
                state['posts'] += 1
                self.send_response(400);self.end_headers()

        http = ThreadingHTTPServer(('127.0.0.1',0), Handler)
        thread = threading.Thread(target=http.serve_forever,daemon=True);thread.start()
        try:
            yield f'http://127.0.0.1:{http.server_port}',state
        finally:
            http.shutdown();http.server_close();thread.join(timeout=3)
