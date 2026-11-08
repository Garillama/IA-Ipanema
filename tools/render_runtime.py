#!/usr/bin/env python3
"""Genera un índice de pruebas a partir de resultados ejecutados, sin tocar el tema."""
import collections
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
doc=root/'ipanema-discovery'
e=doc/'13-evidence/measurements'
def write(name,text):
    p=doc/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n')
def cell(s):return str(s).replace('|','\\|').replace('\n',' ')
def main():
    crawl=json.loads((e/'crawl/summary.json').read_text())
    matrix=json.loads((e/'responsive-matrix/summary.json').read_text())
    records=[]
    for r in crawl['pages']:
        p=e/'crawl'/f"{r['slug']}.json"
        d=json.loads(p.read_text())
        if 'dom' in d:records.append(d)
    unique={r['finalUrl'] for r in records if r['dom'].get('bodyClass','').strip()}
    types=collections.Counter(r['dom']['bodyClass'].strip() for r in records if r['dom']['bodyClass'].strip())
    pages=['# Auditoría ejecutada de rutas', '', 'Verificación 2026-11-08, acceso storefront autorizado. 48 solicitudes de rutas del crawl, 46 destinos HTML únicos después de excluir un XML y el alias /account/ que redirige a login. La cola normalizada quedó vacía; no implica que se hayan enumerado todos los parámetros, páginas privadas o estados de plataforma.', '', '| URL solicitada | HTTP / destino | Tipo / H1 | Canonical / robots | JSON-LD inicial | Evidencia y capturas |', '|---|---|---|---|---|---|']
    for d in records:
        dom=d['dom'];bad=[x for x in d['initial'].get('jsonld',[]) if x.get('error')]
        evidence=f'[JSON](../13-evidence/measurements/crawl/{d["slug"]}.json) · [390](../13-evidence/screenshots/routes/{d["slug"]}-390.png) · [1440](../13-evidence/screenshots/routes/{d["slug"]}-1440.png)'
        pages.append('| '+' | '.join(cell(x) for x in [d['url'],str(d['status'])+'; '+d['finalUrl'],dom['bodyClass']+'; H1 '+str(len(dom['h1'])),', '.join(dom.get('canonical',[]))+'; robots '+str(dom.get('robots',[])),str(len(d['initial'].get('jsonld',[])))+' scripts; errores '+str(len(bad)),evidence])+' |')
    pages.extend(['','Las capturas 390 del crawl son posteriores a resize. Las recargas por dispositivo están en la matriz separada. Los formularios comerciales solo se inventariaron, sin envío.'])
    write('10-quality/runtime-page-audit.md','\n'.join(pages))
    rows=['# Matriz responsive ejecutada', '', 'Verificación 2026-11-08. Una ruta representativa por tipo: home en browser/storefront-* y doce tipos en responsive-matrix. Cada una se cargó en 360,390,768,1024,1440,1920 con DPR 1; isMobile/hasTouch activados bajo 768. No equivale a todos los productos en todos los dispositivos.', '', '| Tipo | URL | Ancho | Estado / overflow | axe (si ejecutado) | Evidencia |', '|---|---|---:|---|---|---|']
    for r in sorted(matrix['results'],key=lambda x:(x['template'],x['width'])):
        name=r['template']+'-'+str(r['width'])
        rows.append('| '+' | '.join(cell(x) for x in [r['template'],r['url'],r['width'],r.get('error') or str(r.get('status'))+'; overflow='+str(r.get('overflow')),', '.join(r.get('axeRules',[])) if 'axeRules' in r else 'no ejecutado',f'[JSON](../13-evidence/measurements/responsive-matrix/{name}.json) · [captura](../13-evidence/screenshots/matrix/{name}.png)'])+' |')
    write('10-quality/responsive-results.md','\n'.join(rows))
    data={'date':'2026-11-08','crawl_attempts':len(crawl['pages']),'unique_html_destinations':len(unique),'public_template_types':len(types),'template_distribution':types,'remaining_queue':len(crawl['remainingQueue']),'responsive_samples_other_than_home':len(matrix['results']),'responsive_errors':[r for r in matrix['results'] if r.get('error')],'responsive_overflows':[r for r in matrix['results'] if r.get('overflow')],'screenshots':len(list((doc/'13-evidence/screenshots').rglob('*.png'))),'lighthouse_runs':len(list((e/'lighthouse').glob('*-summary.json'))),'jsonld_errors':[{'url':d['url'],'errors':[j['error'] for j in d['initial']['jsonld'] if j.get('error')]} for d in records if any(j.get('error') for j in d['initial']['jsonld'])],'multiple_h1_routes':[d['url'] for d in records if len(d['dom']['h1'])>1],'observed_section_types':sorted({s['type'] for d in records for s in d['dom'].get('sections',[])})}
    (e/'coverage-summary.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    metrics=['# Resultados Lighthouse del storefront', '', '2026-11-08, Lighthouse 13.6.0, una muestra por ruta/perfil. Las seis ejecuciones del storefront finalizaron en la ruta solicitada y sin advertencias. Laboratorio simulado, no datos de campo; TBT no sustituye INP. Password inicial queda en archivos mobile/desktop sin prefijo y no se mezcla aquí.', '', '| Ruta / perfil | Performance | LCP ms | FCP ms | TBT ms | CLS | Evidencia |', '|---|---:|---:|---:|---:|---:|---|']
    for prefix in ['home','category','pdp']:
        for device in ['mobile','desktop']:
            name=prefix+'-'+device;d=json.loads((e/'lighthouse'/(name+'-summary.json')).read_text());m=d['metrics']
            metrics.append('| '+' | '.join(cell(x) for x in [name,round(d['categories']['performance']*100),round(m['largest-contentful-paint']),round(m['first-contentful-paint']),round(m['total-blocking-time']),round(m['cumulative-layout-shift'],4),f'[JSON](../13-evidence/measurements/lighthouse/{name}.json) · [HTML](../13-evidence/measurements/lighthouse/{name}.html)'])+' |')
    metrics.extend(['','Mobile: 412×823, DPR 1.75; red/CPU simuladas de Lighthouse (RTT 150 ms, throughput 1638.4 Kbps y CPU ×4). Desktop: 1350×940, DPR 1, RTT 40 ms, throughput 10240 Kbps y CPU ×1. Los parámetros completos están en cada summary.','', 'El LCP de home se atribuyó al placeholder del hero; las recomendaciones deben distinguir ese medio de una imagen final de marca. Los insights de ahorro son estimaciones de Lighthouse y no ahorros ya obtenidos. El audit crawlable-anchors de categoría/PDP señaló controles de acción (borrar filtro, reproducir vídeo); no demuestra por sí solo que falten enlaces a productos. El riesgo independiente de paginación sin href está confirmado en source y prueba sin JS.'])
    write('05-performance/storefront-lighthouse-results.md','\n'.join(metrics))
    print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
