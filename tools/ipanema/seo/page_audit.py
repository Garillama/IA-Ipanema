"""SEO por página, cambios HTML/DOM y arquitectura de enlaces, sin score único."""
from __future__ import annotations

from collections import deque
import hashlib
import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit
from .robots import Robots, google_directive_evidence

from ..core import now
from .extractor import extract
from .schema_validator import validate, F


PAGE_SCHEMAS={
 'home':['Organization/OnlineStore','WebSite','WebPage'],
 'category':['CollectionPage/WebPage','BreadcrumbList','ItemList si existe propósito'],
 'product':['Product/Offer','ProductGroup si existen variantes comprobables','BreadcrumbList'],
 'blog':['Blog/CollectionPage/WebPage','ItemList si describe la lista real'],
 'post':['BlogPosting/Article','WebPage','BreadcrumbList','Autor real'],
 'search':['WebPage','Listas solo si son pertinentes'],
 'page':['WebPage','Entidades descritas por su contenido real'],
 '404':[]}


def page_key(value):
    u=urlsplit(value)
    return urlunsplit((u.scheme,u.netloc.lower(),u.path or '/',u.query,''))


def crawlable(link):
    href=link.get('href')
    return isinstance(href,str) and bool(href.strip()) and not href.startswith('#') and urlsplit(link.get('absolute') or href).scheme in ('http','https')


def snapshot_delta(initial,rendered):
    a={page_key(l['absolute']) for l in initial['links'] if crawlable(l)}
    b={page_key(l['absolute']) for l in rendered['links'] if crawlable(l)}
    hash_block=lambda x:hashlib.sha256(json.dumps(x['data'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    sa={hash_block(s) for s in initial['json_ld'] if not s['error']};sb={hash_block(s) for s in rendered['json_ld'] if not s['error']}
    return {'links_only_after_js':sorted(b-a),'links_removed_after_js':sorted(a-b),
            'structured_data_added_after_js':len(sb-sa),'structured_data_removed_after_js':len(sa-sb),
            'attribution':'Cambio observado; no prueba qué app/script lo causó ni qué indexó Google.'}


def audit_snapshot(project,snap,page_type='page',*,facts=None,rendered=None,no_js=None,robots_text=None,source_map=None):
    if page_type not in PAGE_SCHEMAS:raise ValueError('Tipo de página SEO desconocido.')
    result=validate(snap,page_type,facts)
    findings=list(result['findings']);metadata=snap.get('meta',{})
    canonical=snap.get('canonical',[])
    robots_evidence=google_directive_evidence(metadata,snap.get('headers',{}).get('x-robots-tag',''))
    robots=','.join(robots_evidence['flags'])
    noindex=robots_evidence['noindex']
    if robots_evidence['relevant_errors']:
        findings.append(F('SEO023','D','warning','Directivas robots malformadas: conservar fuentes y evidencia insuficiente sin ignorar restricciones válidas.',evidence=robots_evidence['relevant_errors']))
    status=snap.get('status')
    if not snap.get('title'):findings.append(F('SEO001','D','warning','Title ausente; comprobar head-tags de plataforma.'))
    if not metadata.get('description'):findings.append(F('SEO002','D','recommendation','Meta description ausente; usar contenido útil y específico.'))
    h1=[h for h in snap['headings'] if h['level']==1]
    if len(h1)!=1:
        findings.append(F('SEO003','D','warning',f'Se observaron {len(h1)} H1; revisar jerarquía y origen, no penalización automática.',evidence=h1,
                          fix='Si está en user-content, revisar contenido editable; si proviene del tema, localizar consumidor.'))
    if len(canonical)>1:findings.append(F('SEO004','D','warning','Más de una etiqueta canonical.',evidence=canonical))
    if not canonical and page_type!='404':findings.append(F('SEO005','D','recommendation','Canonical no observado; comprobar componente de plataforma.'))
    if canonical and page_key(canonical[0])!=page_key(snap['url']):
        findings.append(F('SEO006','D','recommendation','Canonical distinto de la URL solicitada; revisar variante/parámetros/duplicación sin asumir error.',evidence=canonical))
    links=[l for l in snap['links'] if crawlable(l)]
    carousels=[l for l in snap['links'] if l.get('context',{}).get('carousel')]
    bad_carousels=[l for l in carousels if not crawlable(l) and not l.get('action_hint')]
    if bad_carousels:findings.append(F('SEO010','D','warning','Controles de carrusel sin destino rastreable; distinguir acciones de enlaces a productos/categorías.',evidence=bad_carousels))
    more=[l for l in snap['links'] if not l.get('action_hint') and not l.get('disabled') and (l.get('context',{}).get('pagination') or re.search(r'load.more|pagination',str(l.get('class','')),re.I) or l.get('context',{}).get('main') and re.search(r'mostrar m[aá]s (productos|art[ií]culos)|load more',str(l.get('text','')),re.I))]
    if page_type in ('category','blog') and any(not crawlable(l) for l in more):
        findings.append(F('SEO011','D','error','La carga posterior no conserva href real en su control. No inventar parámetros de paginación.',evidence=more))
    for image in snap['images']:
        if image.get('alt') is None:findings.append(F('SEO012','D','recommendation','Imagen sin atributo alt; revisar contexto/decoración.',evidence={'src':image['src']}))
    hreflang=[l for l in snap.get('links_rel',[]) if l.get('hreflang')]
    for link in hreflang:
        if not link.get('href'):findings.append(F('SEO013','D','warning','hreflang sin URL real.',evidence=link))
    permission='not_checked_robots_txt'
    if robots_text is not None:
        parser=Robots();parser.parse(robots_text.splitlines());permission='unknown_rules' if parser.errors else 'allowed' if parser.can_fetch('Googlebot',snap['url']) else 'disallowed'
    signals='http_unknown' if status is None else 'non_200' if status!=200 else 'noindex_observed' if noindex else 'insufficient_evidence' if robots_evidence['relevant_errors'] else 'no_observable_noindex_not_index_proof'
    delta=snapshot_delta(snap,rendered) if rendered is not None else None
    if delta and delta['links_only_after_js']:
        findings.append(F('SEO020','D','warning','Hay enlaces presentes solo tras JavaScript; comprobar navegación/fallback y descubrimiento.',evidence=delta['links_only_after_js']))
    if no_js is not None:
        absent={l['absolute'] for l in links}-{l['absolute'] for l in no_js['links'] if crawlable(l)}
        if absent:findings.append(F('SEO021','D','warning','Enlaces iniciales no observados en captura sin JS; revisar contexto de captura.',evidence=sorted(absent)))
    components=[]
    for block in snap['json_ld']:
        marker=block.get('component')
        sources=(source_map or {}).get(marker,[])
        components.append({'block':block['index'],'marker':marker,'source_candidates':sources,
                           'attribution':'native_source_match_candidate' if sources else 'unknown_theme_or_app','confirmed_runtime_initiator':False})
    for f in findings:
        f['priority']='P1' if f['severity']=='error' else 'P2' if f['severity']=='warning' else 'P3'
    return {'kind':'seo-page-audit','project':project.id,'domain':urlsplit(snap['url']).hostname,'url':snap['url'],
            'page_type':page_type,'at':now(),'theme_observation':project.data.get('remote_observation'),
            'http_status':status,'canonical':canonical,'indexability_observable':signals,'indexation_verified':False,
            'crawl_permission_observed':permission,'robots_directives':robots,'robots_evidence':robots_evidence,'schema_matrix':PAGE_SCHEMAS[page_type],
            'structured_data':result,'schema_sources':components,'findings':findings,
            'content':{k:snap.get(k) for k in ('title','meta','headings','lang','images')},
            'crawl':{'links':links,'carousel_links':carousels,'pagination_controls':more,'hreflang':hreflang,
                     'non_navigation_carousel_controls':[l for l in carousels if l.get('action_hint')],
                     'unlinked_products':'not_evaluated_without_catalog','depth':'requires_corpus','orphans':'not_evaluated_without_complete_url_set'},
            'html_dom_comparison':delta,'no_js_captured':no_js is not None,
            'google':{'connection':'not_connected','url_inspection':'not_consulted','merchant_center':'not_consulted','analytics':'not_consulted'},
            'limitations':['HTML/JSON no prueban indexación o resultados enriquecidos.','RDFa/microdata y vocabulario se comprueban en un subconjunto explícito.',
                           'La captura HTML no permite conocer CSS computado, descarga/decodificación ni comportamiento de todos los estados.']+snap.get('markup_limits',[])}


def audit_html(project,html,url,page_type='page',*,status=None,headers=None,rendered_html=None,no_js_html=None,facts=None,**kwargs):
    snap=extract(html,url,status=status,headers=headers)
    return audit_snapshot(project,snap,page_type,facts=facts,rendered=extract(rendered_html,url) if rendered_html is not None else None,
                          no_js=extract(no_js_html,url) if no_js_html is not None else None,**kwargs)


def internal_architecture(reports,roots=None,sitemap_urls=None):
    by={page_key(r['url']):r for r in reports};roots=roots or [r['url'] for r in reports if r['page_type']=='home']
    depth={page_key(r):0 for r in roots if page_key(r) in by};todo=deque(depth)
    incoming={u:set() for u in by}
    while todo:
        u=todo.popleft()
        for link in by[u]['crawl']['links']:
            v=page_key(link['absolute'])
            if v in by:
                incoming[v].add(u)
                if v not in depth:depth[v]=depth[u]+1;todo.append(v)
    # Inlinks también desde páginas fuera de la componente alcanzable.
    for u,r in by.items():
        for l in r['crawl']['links']:
            v=page_key(l['absolute'])
            if v in incoming:incoming[v].add(u)
    titles={};duplicates=[]
    for u,r in by.items():
        title=r['content'].get('title')
        if title:titles.setdefault(title,[]).append(u)
    duplicates=[{'title':t,'urls':us} for t,us in titles.items() if len(us)>1]
    site={page_key(u) for u in sitemap_urls or []}
    return {'scope_urls':len(by),'roots':roots,'depth_in_observed_corpus':depth,
            'not_reached_in_corpus':sorted(set(by)-set(depth)),'without_inlinks_in_corpus':[u for u,inc in incoming.items() if not inc],
            'duplicate_titles':duplicates,'sitemap_not_observed':sorted(site-set(by)),
            'sitemap_comparison_performed':sitemap_urls is not None,
            'limitations':['No declarar huérfana una URL por no verla en un corpus parcial.','Títulos iguales son candidatos editoriales, no prueba de canibalización ni contenido duplicado completo.']}
