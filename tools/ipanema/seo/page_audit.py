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


SEO_FRAMEWORK_CANDIDATES = {
    'shopify-liquid': {
        'technical': ['layout/theme.liquid', 'templates/robots.txt.liquid'],
        'on-page': ['layout/theme.liquid', 'sections/main-product.liquid', 'sections/main-collection-banner.liquid'],
        'ecommerce': ['sections/main-collection-product-grid.liquid', 'snippets/pagination.liquid', 'sections/main-product.liquid'],
        'international': ['layout/theme.liquid', 'snippets/language-localization.liquid'],
    },
    'shopify-hydrogen': {
        'technical': ['app/root.tsx', 'app/routes/[robots.txt].tsx', 'app/routes/[sitemap.xml].tsx'],
        'on-page': ['app/root.tsx', 'app/routes/products.$handle.tsx', 'app/routes/collections.$handle.tsx'],
        'ecommerce': ['app/routes/collections.$handle.tsx', 'app/routes/products.$handle.tsx'],
        'international': ['app/root.tsx', 'app/lib/i18n.ts'],
    },
    'react-web': {
        'technical': ['index.html', 'src/main.tsx'],
        'on-page': ['index.html', 'src/App.tsx'],
        'ecommerce': ['src/pages/Catalog.tsx', 'src/pages/Product.tsx'],
        'international': ['index.html', 'src/i18n.ts'],
    },
    'tiendanube-ipanema': {
        'technical': ['layouts/layout.tpl', 'snippets/structured-data/structured-data.tpl'],
        'on-page': ['layouts/layout.tpl', 'templates/product.tpl', 'templates/category.tpl'],
        'ecommerce': ['templates/category.tpl', 'snippets/pagination.tpl', 'templates/product.tpl'],
        'international': ['layouts/layout.tpl'],
    },
}

FACET_PARAMETER_KEYS = frozenset({
    'sort_by', 'sort', 'order', 'color', 'size', 'talla', 'marca', 'brand',
    'price', 'precio', 'min_price', 'max_price', 'tag', 'filter', 'utm_source',
    'utm_medium', 'utm_campaign', 'session_id', 'phpsessid', 'sid',
})

GENERIC_ANCHOR_TEXTS = frozenset({
    'click here', 'read more', 'learn more', 'more', 'here', 'link',
    'clic aqui', 'clic aquí', 'leer mas', 'leer más', 'ver mas', 'ver más', 'aqui', 'aquí',
})

GENERIC_IMAGE_ALTS = frozenset({
    'image', 'imagen', 'photo', 'foto', 'picture', 'default', 'placeholder', 'banner', 'product', 'producto',
})

HREFLANG_CODE_RE = re.compile(r'^(?:x-default|[a-z]{2,3}(?:-[A-Z]{2})?)$')
INVALID_REGION_SUBTAGS = {'UK': 'GB'}


def comprehensive_seo_audit(
    project,
    html: str,
    url: str,
    page_type: str = 'page',
    *,
    status: int | None = 200,
    headers: dict | None = None,
    rendered_html: str | None = None,
    no_js_html: str | None = None,
    robots_text: str | None = None,
    sitemap_xml: str | None = None,
    redirect_chain: list[dict] | None = None,
    additional_pages: list[dict] | None = None,
    source_files: dict[str, str] | None = None,
    quality_audit_report: dict | None = None,
    framework: str | None = None,
) -> dict:
    """Auditoría especializada SEO Audit (Etapa 3): reutiliza el motor SEO existente y separa 3 niveles de evidencia."""
    from urllib.parse import parse_qsl
    from ..core import redact
    from ..performance.model import infer_framework
    from .indexability import Content, classify, pagination
    from .sitemaps import parse_sitemap

    detected_fw = infer_framework(framework, source_files)
    fw_candidates = SEO_FRAMEWORK_CANDIDATES.get(detected_fw, SEO_FRAMEWORK_CANDIDATES['tiendanube-ipanema'])

    # Reutilizar motor base de página e indexabilidad
    base_audit = audit_html(
        project,
        html,
        url,
        page_type,
        status=status,
        headers=headers,
        rendered_html=rendered_html,
        no_js_html=no_js_html,
        robots_text=robots_text,
    )
    snap = extract(html, url, status=status, headers=headers)
    content_ev = Content(html).evidence()

    robot_parser = None
    google_allowed = None
    if robots_text is not None:
        robot_parser = Robots()
        robot_parser.parse(robots_text.splitlines())
        if not robot_parser.errors:
            google_allowed = robot_parser.can_fetch('Googlebot', url)

    idx_info = classify(
        snap,
        googlebot_allowed=google_allowed,
        robots_known=bool(robot_parser and not robot_parser.errors),
        content=content_ev,
    )

    verified_by_tool = []
    code_hypothesis = []
    requires_external_verification = []

    def add_verified(rule_id, category, priority, severity, title, impact, evidence, fix, files=None):
        verified_by_tool.append({
            'id': rule_id,
            'category': category,
            'priority': priority,
            'severity': severity,
            'evidence_type': 'verified_by_tool',
            'title': title,
            'impact': impact,
            'evidence': redact(evidence),
            'candidate_files': files or fw_candidates.get(category, []),
            'fix': fix,
        })

    def add_hypothesis(rule_id, category, priority, severity, title, impact, evidence, fix, files):
        code_hypothesis.append({
            'id': rule_id,
            'category': category,
            'priority': priority,
            'severity': severity,
            'evidence_type': 'code_hypothesis',
            'title': title,
            'impact': impact,
            'evidence': redact(evidence),
            'candidate_files': files,
            'fix': fix,
        })

    def add_external(rule_id, category, title, reason, required_source, evidence=None):
        requires_external_verification.append({
            'id': rule_id,
            'category': category,
            'evidence_type': 'requires_external_verification',
            'title': title,
            'reason': reason,
            'required_source': required_source,
            'evidence': redact(evidence or {}),
        })

    # Incorporar hallazgos verificados del motor base (audit_snapshot)
    for f in base_audit.get('findings', []):
        # Si no hay DOM renderizado, no afirmar en verified_by_tool que falta una entidad Schema (C100, C221, etc.)
        if rendered_html is None and f['rule'].startswith('C') and not snap.get('json_ld') and not snap.get('microdata'):
            continue
        cat = 'ecommerce' if f['rule'] in ('SEO010', 'SEO011', 'B010') else 'technical' if f['rule'] in ('SEO004', 'SEO005', 'SEO006', 'SEO020', 'SEO021', 'SEO023') else 'on-page'
        add_verified(
            f['rule'],
            cat,
            f.get('priority', 'P2'),
            f['severity'],
            f['message'],
            'Detectado por el validador SEO base sobre el marcado capturado.',
            f.get('evidence'),
            f.get('fix') or 'Corregir en la plantilla correspondiente conservando contratos nativos.',
        )

    # 1. SEO TÉCNICO: Estados HTTP, Redirecciones, Robots.txt, Sitemaps, Canonical, Meta Robots, Soft 404
    if status is not None and status >= 400:
        add_verified(
            'SEO-TECH-HTTP-STATUS',
            'technical',
            'P1',
            'error',
            f'Respuesta HTTP no indexable ({status})',
            'Las páginas con estado 4xx/5xx no pueden indexarse y desperdician presupuesto de rastreo si reciben enlaces internos.',
            {'url': url, 'status': status},
            'Restaurar estado 200 si el recurso sigue vigente o actualizar enlaces internos hacia el destino canónico.',
        )
    if redirect_chain:
        hops = len(redirect_chain)
        seen_urls = [r.get('url') for r in redirect_chain if isinstance(r, dict) and r.get('url')]
        has_loop = len(seen_urls) != len(set(seen_urls))
        if has_loop or hops > 1:
            add_verified(
                'SEO-TECH-REDIRECT-CHAIN',
                'technical',
                'P1' if has_loop else 'P2',
                'error' if has_loop else 'warning',
                'Bucle de redirección detectado' if has_loop else f'Cadena de redirección de {hops} saltos',
                'Añade latencia al rastreo de Googlebot y diluye señales de enlace.',
                {'hops': hops, 'loop': has_loop, 'chain': redirect_chain},
                'Apuntar enlaces y redirecciones directamente al destino final 200 en un solo salto 301.',
            )

    if base_audit['robots_evidence']['noindex']:
        add_verified(
            'SEO-TECH-NOINDEX',
            'technical',
            'P1',
            'error',
            'Directiva noindex activa en la página',
            'Excluye explícitamente la URL del índice de búsqueda.',
            {'directives': base_audit['robots_directives']},
            'Si la URL debe posicionarse, eliminar noindex de meta robots o X-Robots-Tag.',
        )

    if content_ev.get('soft_404_candidate') and status == 200:
        add_verified(
            'SEO-TECH-SOFT-404',
            'technical',
            'P1',
            'error',
            'Posible Soft 404 (código 200 con mensaje de página/producto no encontrado)',
            'Engaña a los rastreadores devolviendo 200 OK en una página inexistente o vacía.',
            {'status': status, 'soft_404_candidate': True},
            'Devolver código HTTP 404/410 real o mostrar productos/contenido alternativo válido.',
        )

    if robot_parser is not None:
        if robot_parser.errors:
            add_verified(
                'SEO-TECH-ROBOTS-SYNTAX',
                'technical',
                'P2',
                'warning',
                'Errores de sintaxis en robots.txt',
                'Reglas ambiguas o inválidas según RFC 9309 pueden ser ignoradas o malinterpretadas.',
                {'errors': robot_parser.errors},
                'Corregir las directivas User-agent/Allow/Disallow en robots.txt.',
            )
        elif google_allowed is False:
            add_verified(
                'SEO-TECH-ROBOTS-BLOCKED',
                'technical',
                'P1',
                'error',
                'URL bloqueada para Googlebot en robots.txt',
                'Impide que Googlebot rastree el contenido de la URL.',
                {'url': url, 'googlebot_allowed': False},
                'Ajustar la regla Disallow en robots.txt si la página es pública e indexable.',
            )
        if not robot_parser.site_maps():
            add_verified(
                'SEO-TECH-ROBOTS-NO-SITEMAP',
                'technical',
                'P3',
                'recommendation',
                'robots.txt no declara directiva Sitemap:',
                'Dificulta el descubrimiento automático del sitemap XML por parte de buscadores.',
                {'sitemaps_declared': []},
                'Añadir Sitemap: https://<dominio>/sitemap.xml al final de robots.txt.',
            )

    if sitemap_xml is not None:
        sm = parse_sitemap(sitemap_xml, source='sitemap.xml')
        sm_urls = {page_key(e['url']) for e in sm['entries']}
        if sm['duplicates'] or sm['errors']:
            add_verified(
                'SEO-TECH-SITEMAP-ISSUES',
                'technical',
                'P2',
                'warning',
                'Sitemap XML presenta entradas duplicadas o con errores de formato',
                'Reduce la fiabilidad del inventario de URLs enviado a motores de búsqueda.',
                {'duplicates': sm['duplicates'], 'errors': sm['errors']},
                'Depurar el generador de sitemap para emitir únicamente URLs canónicas únicas y válidas.',
            )
        future_lastmods = [e['url'] for e in sm['entries'] if e['lastmod_state'] == 'future']
        if future_lastmods:
            add_verified(
                'SEO-TECH-SITEMAP-FUTURE-LASTMOD',
                'technical',
                'P3',
                'warning',
                'Sitemap XML contiene fechas <lastmod> en el futuro',
                'Desacredita la señal lastmod ante los motores de búsqueda.',
                {'urls': future_lastmods},
                'Emitir la fecha real de última modificación en UTC.',
            )
        if page_key(url) in sm_urls and (base_audit['robots_evidence']['noindex'] or (status and status != 200)):
            add_verified(
                'SEO-TECH-SITEMAP-NON-INDEXABLE-URL',
                'technical',
                'P1',
                'error',
                'URL no indexable (noindex o estado != 200) incluida en sitemap XML',
                'Envía señales contradictorias a Google (solicitar rastreo en sitemap y prohibir indexación).',
                {'url': url, 'in_sitemap': True, 'noindex': base_audit['robots_evidence']['noindex'], 'status': status},
                'Excluir del sitemap todas las URLs con noindex, redirecciones o errores.',
            )
        elif page_key(url) not in sm_urls and idx_info['state'] == 'indexable_candidate' and page_type in ('home', 'category', 'product', 'post'):
            add_verified(
                'SEO-TECH-SITEMAP-MISSING-URL',
                'technical',
                'P2',
                'recommendation',
                'URL indexable relevante no figura en el sitemap XML proporcionado',
                'Puede retrasar el descubrimiento de páginas comerciales o editoriales.',
                {'url': url, 'in_sitemap': False},
                'Incluir la URL canónica dentro del sitemap XML correspondiente.',
            )

    # Canonical checks (HTTP->HTTPS, host mismatch, pagination, faceted parameters)
    canonicals = snap.get('canonical', [])
    parsed_url = urlsplit(url)
    query_pairs = parse_qsl(parsed_url.query, keep_blank_values=True)
    query_keys = {k.lower() for k, _ in query_pairs}

    if canonicals:
        canon_url = canonicals[0]
        parsed_canon = urlsplit(canon_url)
        if parsed_url.scheme == 'https' and parsed_canon.scheme == 'http':
            add_verified(
                'SEO-TECH-CANONICAL-HTTP',
                'technical',
                'P1',
                'error',
                'Etiqueta canonical apunta a versión HTTP desde una página HTTPS',
                'Provoca señales graves de canonicalización hacia un protocolo inseguro.',
                {'url': url, 'canonical': canon_url},
                'Asegurar que canonical utilice siempre https://.',
            )
        # Paginación canonicalizada erróneamente a la raíz de la colección
        page_param = dict((k.lower(), v) for k, v in query_pairs).get('page')
        if page_param and page_param not in ('1', '') and 'page=' not in parsed_canon.query.lower() and parsed_canon.path.rstrip('/') == parsed_url.path.rstrip('/'):
            add_verified(
                'SEO-ECOM-PAGINATION-CANONICAL-TO-ROOT',
                'ecommerce',
                'P1',
                'error',
                f'Página paginada (?page={page_param}) apunta su canonical a la página 1',
                'Impide que los motores de búsqueda consoliden y descubran correctamente los enlaces de productos en páginas 2+.',
                {'url': url, 'canonical': canon_url, 'page': page_param},
                'Usar canonical autorreferencial en cada página paginada (ej. ?page=2 -> ?page=2).',
            )

    # 2. SEO INTERNACIONAL (Hreflang)
    hreflang_links = [l for l in snap.get('links_rel', []) if l.get('hreflang')]
    if hreflang_links:
        seen_langs = {}
        invalid_codes = []
        self_ref_present = False
        canon_target = page_key(canonicals[0]) if canonicals else page_key(url)
        for hl in hreflang_links:
            code = str(hl.get('hreflang') or '').strip()
            target = urljoin(url, hl.get('href') or '')
            norm_code = code if code == 'x-default' else '-'.join([code.split('-')[0].lower()] + [p.upper() for p in code.split('-')[1:]])
            if not HREFLANG_CODE_RE.match(norm_code) or (len(norm_code.split('-')) == 2 and norm_code.split('-')[1] in INVALID_REGION_SUBTAGS):
                invalid_codes.append({'code': code, 'suggested': norm_code.replace('-UK', '-GB') if '-UK' in norm_code else None})
            if norm_code in seen_langs and seen_langs[norm_code] != page_key(target):
                add_verified(
                    'SEO-INTL-DUPLICATE-HREFLANG',
                    'international',
                    'P2',
                    'warning',
                    f'Código hreflang duplicado ({code}) apuntando a URLs distintas',
                    'Los motores de búsqueda pueden ignorar las anotaciones conflictivas para ese idioma/región.',
                    {'code': code, 'urls': [seen_langs[norm_code], page_key(target)]},
                    'Mantener una única URL canónica por código de idioma-región.',
                )
            seen_langs[norm_code] = page_key(target)
            if page_key(target) == canon_target:
                self_ref_present = True
        if invalid_codes:
            add_verified(
                'SEO-INTL-INVALID-HREFLANG-CODE',
                'international',
                'P2',
                'warning',
                'Código de idioma/región inválido en hreflang (ISO 639-1 / ISO 3166-1)',
                'Google ignora etiquetas hreflang con códigos no estándar (ej. en-UK en vez de en-GB).',
                {'invalid_codes': invalid_codes},
                'Corregir los códigos hreflang al estándar ISO 639-1 e ISO 3166-1 Alpha-2.',
                fw_candidates.get('international', []),
            )
        if not self_ref_present:
            add_verified(
                'SEO-INTL-MISSING-SELF-HREFLANG',
                'international',
                'P2',
                'warning',
                'Conjunto hreflang no incluye entrada autorreferencial hacia la URL canónica actual',
                'Sin autorreferencia o cuando el canonical difiere del hreflang, el clúster internacional puede invalidarse.',
                {'canonical': canon_target, 'hreflang_targets': list(seen_langs.values())},
                'Incluir la propia URL canónica con su código de idioma dentro del bloque hreflang.',
                fw_candidates.get('international', []),
            )
        remote_alternates = [u for u in seen_langs.values() if u != canon_target]
        if remote_alternates:
            add_external(
                'SEO-EXT-HREFLANG-RECIPROCITY',
                'international',
                'Verificación de reciprocidad (return tags) en URLs alternas hreflang',
                'Para confirmar que las páginas alternas enlazan de vuelta (A <-> B) y responden 200 OK se requiere inspeccionar cada URL alterna.',
                'Rastreo de URLs alternas o exportación de corpus multi-idioma',
                {'alternate_urls': remote_alternates},
            )

    # 3. SEO ON-PAGE: Titles, Meta Descriptions, Headings, Imágenes, Enlaces, Thin/Duplicate Content
    title_text = (snap.get('title') or '').strip()
    if title_text:
        if len(title_text) < 15:
            add_verified(
                'SEO-ONPAGE-TITLE-SHORT',
                'on-page',
                'P3',
                'recommendation',
                f'Etiqueta <title> muy corta ({len(title_text)} caracteres)',
                'Desaprovecha espacio para describir la intención de búsqueda y propuesta de valor.',
                {'title': title_text, 'length': len(title_text)},
                'Ampliar el <title> a aproximadamente 50–60 caracteres con el término principal al inicio.',
            )
        elif len(title_text) > 60:
            add_verified(
                'SEO-ONPAGE-TITLE-LONG',
                'on-page',
                'P3',
                'recommendation',
                f'Etiqueta <title> extensa ({len(title_text)} caracteres; riesgo de truncamiento)',
                'Google puede truncar o reescribir títulos que exceden el ancho visible en resultados.',
                {'title': title_text, 'length': len(title_text)},
                'Acotar el <title> a 50–60 caracteres conservando la palabra clave principal cerca del inicio.',
            )

    descriptions = snap.get('meta', {}).get('description', [])
    desc_text = (descriptions[0] if descriptions else '').strip()
    if desc_text:
        if len(desc_text) < 50:
            add_verified(
                'SEO-ONPAGE-DESC-SHORT',
                'on-page',
                'P3',
                'recommendation',
                f'Meta description corta ({len(desc_text)} caracteres)',
                'Aporta poco contexto persuasivo para mejorar el CTR en resultados de búsqueda.',
                {'description': desc_text, 'length': len(desc_text)},
                'Redactar un resumen único de entre 120 y 160 caracteres con propuesta de valor clara.',
            )
        elif len(desc_text) > 160:
            add_verified(
                'SEO-ONPAGE-DESC-LONG',
                'on-page',
                'P3',
                'recommendation',
                f'Meta description extensa ({len(desc_text)} caracteres)',
                'Suele truncarse en los snippets de resultados de búsqueda.',
                {'description': desc_text, 'length': len(desc_text)},
                'Ajustar la meta description a 150–160 caracteres.',
            )

    headings = snap.get('headings', [])
    levels = [h['level'] for h in headings]
    skipped = []
    for prev_l, curr_l in zip(levels, levels[1:]):
        if curr_l > prev_l + 1:
            skipped.append(f'H{prev_l}->H{curr_l}')
    if skipped:
        add_verified(
            'SEO-ONPAGE-HEADING-SKIP',
            'on-page',
            'P3',
            'recommendation',
            'Saltos en la jerarquía de encabezados (' + ', '.join(skipped) + ')',
            'Debilita la estructura semántica del documento para lectores de pantalla y motores de búsqueda.',
            {'skipped_transitions': skipped, 'headings': headings},
            'Mantener una progresión jerárquica ordenada (H1 -> H2 -> H3).',
        )

    for img in snap.get('images', []):
        alt_val = (img.get('alt') or '').strip()
        if alt_val and (alt_val.lower() in GENERIC_IMAGE_ALTS or re.fullmatch(r'[\w-]+\.(?:jpg|jpeg|png|webp|avif|gif)', alt_val, re.I)):
            add_verified(
                'SEO-ONPAGE-IMG-GENERIC-ALT',
                'on-page',
                'P3',
                'recommendation',
                f'Imagen con atributo alt genérico o nombre de archivo ("{alt_val}")',
                'No describe el producto o contenido real para búsqueda de imágenes ni accesibilidad.',
                {'src': img.get('src'), 'alt': alt_val},
                'Usar un texto alt descriptivo del producto/variante.',
            )

    for link in snap.get('links', []):
        anchor = (link.get('text') or link.get('aria_label') or '').strip().lower()
        if anchor in GENERIC_ANCHOR_TEXTS:
            add_verified(
                'SEO-ONPAGE-GENERIC-ANCHOR',
                'on-page',
                'P3',
                'recommendation',
                f'Enlace interno con texto ancla genérico ("{anchor}")',
                'Pierde la oportunidad de transmitir contexto temático a la página enlazada.',
                {'href': link.get('href'), 'anchor': anchor},
                'Utilizar texto de ancla descriptivo del destino (ej. nombre de la categoría o producto).',
            )

    if page_type in ('product', 'category', 'post') and content_ev['main_text_characters'] < 150:
        add_verified(
            'SEO-ONPAGE-THIN-CONTENT',
            'on-page',
            'P2',
            'warning',
            f'Contenido principal escaso en <main> ({content_ev["main_text_characters"]} caracteres)',
            'Las páginas de producto, colección o artículo sin contenido descriptivo suficiente tienen menor capacidad para responder la intención de búsqueda.',
            {'page_type': page_type, 'main_text_characters': content_ev['main_text_characters']},
            'Incorporar descripciones útiles, especificaciones o preguntas frecuentes relevantes en la plantilla.',
        )

    # Contenido o títulos duplicados cuando se aportan páginas adicionales
    for other in (additional_pages or []):
        if not isinstance(other, dict) or not other.get('url') or page_key(other['url']) == page_key(url):
            continue
        other_html = other.get('html', '')
        other_snap = extract(other_html, other['url'])
        other_ev = Content(other_html).evidence()
        if title_text and other_snap.get('title') == title_text:
            add_verified(
                'SEO-ONPAGE-DUPLICATE-TITLE',
                'on-page',
                'P2',
                'warning',
                f'Etiqueta <title> duplicada con otra URL ({other["url"]})',
                'Genera competencia interna (canibalización) y dificulta distinguir qué página debe posicionar.',
                {'title': title_text, 'urls': [url, other['url']]},
                'Diferenciar el <title> de cada página según su entidad o intención específica.',
            )
        if content_ev.get('main_text_sha256') and content_ev['main_text_sha256'] == other_ev.get('main_text_sha256'):
            add_verified(
                'SEO-ONPAGE-DUPLICATE-CONTENT',
                'on-page',
                'P2',
                'warning',
                f'Contenido principal idéntico (hash SHA256 igual) entre {url} y {other["url"]}',
                'Puede provocar que Google elija un canonical distinto al esperado.',
                {'main_text_sha256': content_ev['main_text_sha256'], 'urls': [url, other['url']]},
                'Consolidar mediante canonical/301 o redactar contenido único para cada URL.',
            )

    # 4. SEO PARA COMERCIO ELECTRÓNICO: Filtros facetados, parámetros, variantes, paginación y Schema en DOM
    has_facet_params = bool(query_keys & FACET_PARAMETER_KEYS) or any(k.startswith('filter.') for k in query_keys)
    if has_facet_params:
        clean_base_url = urlunsplit((parsed_url.scheme, parsed_url.netloc.lower(), parsed_url.path or '/', '', ''))
        canon_points_to_clean = bool(canonicals) and page_key(canonicals[0]) == clean_base_url
        if not canon_points_to_clean and not base_audit['robots_evidence']['noindex']:
            add_verified(
                'SEO-ECOM-FACET-PARAMETER-DUPLICATE',
                'ecommerce',
                'P1',
                'warning',
                'URL con parámetros de filtro/ordenamiento/sesión sin canonical hacia la ruta limpia ni noindex',
                'La navegación por facetas no controlada multiplica URLs casi idénticas y agota el presupuesto de rastreo.',
                {'url': url, 'query_keys': sorted(query_keys), 'canonical': canonicals},
                f'Apuntar el <link rel="canonical"> a la colección base limpia ({clean_base_url}) o aplicar directivas de control de facetas.',
            )

    if 'variant' in query_keys and page_type == 'product':
        clean_product_url = urlunsplit((parsed_url.scheme, parsed_url.netloc.lower(), parsed_url.path or '/', '', ''))
        if not canonicals:
            add_verified(
                'SEO-ECOM-VARIANT-NO-CANONICAL',
                'ecommerce',
                'P2',
                'warning',
                'URL de variante de producto (?variant=) sin etiqueta canonical explícita',
                'Riesgo de duplicidad entre variantes del mismo producto si no tienen contenido ni búsqueda diferenciada.',
                {'url': url, 'clean_product_url': clean_product_url},
                'Definir canonical hacia el producto principal o configurar ProductGroup con URLs de variante diferenciadas.',
            )

    # Regla crítica de exactitud (Sección 5): No afirmar que falta Schema si solo se inspeccionó HTML estático
    if rendered_html is None and not snap.get('json_ld') and not snap.get('microdata'):
        add_external(
            'SEO-EXT-SCHEMA-RENDERED-DOM',
            'ecommerce' if page_type in ('product', 'category') else 'technical',
            'Comprobación de datos estructurados (JSON-LD) en DOM renderizado con JavaScript',
            'En el HTML estático no se observaron bloques JSON-LD, pero no se debe afirmar que falta Schema sin inspeccionar el DOM renderizado (apps o componentes cliente pueden inyectarlo).',
            'Captura de navegador renderizada (--rendered / qa_browser.mjs / Rich Results Test)',
            {'url': url, 'static_json_ld_count': 0, 'rendered_html_supplied': False},
        )

    # 5. Reutilización opcional de evidencia de Web Quality Audit sin duplicar análisis
    reused_wqa_findings = []
    if isinstance(quality_audit_report, dict) and quality_audit_report.get('skill') == 'web-quality-audit':
        for issue in quality_audit_report.get('verified_issues', []):
            if isinstance(issue, dict) and issue.get('category') in ('seo', 'performance'):
                reused_wqa_findings.append(issue['id'])

    # 6. Inspección de código fuente / plantillas -> code_hypothesis
    for path, source_text in sorted((source_files or {}).items()):
        if not isinstance(source_text, str):
            continue
        lower = source_text.lower()
        is_layout = path.endswith(('layout.tpl', 'theme.liquid', 'index.html', 'root.tsx'))
        if is_layout:
            if 'rel="canonical"' not in lower and "rel='canonical'" not in lower and 'canonical_url' not in lower:
                add_hypothesis(
                    'SEO-SRC-MISSING-CANONICAL',
                    'technical',
                    'P2',
                    'warning',
                    'Plantilla base no parece incluir etiqueta <link rel="canonical">',
                    'Si ninguna subplantilla o helper lo inyecta en runtime, las páginas carecerán de URL canónica.',
                    {'file': path},
                    'Añadir <link rel="canonical" href="..."> en el layout principal.',
                    [path],
                )
            if '<title' not in lower and 'meta:' not in lower and 'meta(' not in lower:
                add_hypothesis(
                    'SEO-SRC-MISSING-TITLE',
                    'on-page',
                    'P2',
                    'warning',
                    'Plantilla base no muestra etiqueta <title> explícita',
                    'Verificar en el DOM renderizado si el título es inyectado por un snippet o ruta.',
                    {'file': path},
                    'Asegurar la emisión de <title> dinámico en el layout.',
                    [path],
                )
        h1_matches = list(re.finditer(r'<h1\b[^>]*>', source_text, re.I))
        if len(h1_matches) > 1:
            add_hypothesis(
                'SEO-SRC-MULTIPLE-H1',
                'on-page',
                'P3',
                'recommendation',
                f'Archivo fuente contiene {len(h1_matches)} etiquetas <h1> en la misma plantilla',
                'Si las ramas condicionales se evalúan simultáneamente, la página renderizará múltiples H1.',
                {'file': path, 'h1_count_in_source': len(h1_matches)},
                'Verificar las condiciones de plantilla y usar <h2> para subtítulos o secciones secundarias.',
                [path],
            )
        for idx, line in enumerate(source_text.splitlines(), start=1):
            if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', line, re.I) and not re.search(r'\{%|if\b|\?', line):
                add_hypothesis(
                    'SEO-SRC-UNCONDITIONAL-NOINDEX',
                    'technical',
                    'P1',
                    'error',
                    'Etiqueta meta robots con noindex incondicional detectada en plantilla',
                    'Podría desindexar todas las páginas que utilicen esta plantilla.',
                    {'file': path, 'line': idx, 'snippet': redact(line.strip()[:120])},
                    'Acotar la directiva noindex mediante una condición explícita solo a plantillas no indexables.',
                    [path],
                )

    # 7. Verificaciones externas obligatorias (Search Console / Indexación real / Tráfico)
    add_external(
        'SEO-EXT-GOOGLE-INDEXATION-STATUS',
        'technical',
        'Estado real de indexación y cobertura en Google Search Console',
        'El análisis de HTML, cabeceras y robots.txt determina la indexabilidad técnica observable, nunca si Google ya indexó o desindexó la URL.',
        'Google Search Console URL Inspection / Coverage export autorizado',
        {'url': url, 'observable_state': idx_info['state'], 'indexation_verified': False},
    )
    add_external(
        'SEO-EXT-ORGANIC-PERFORMANCE',
        'on-page',
        'Datos reales de impresiones, clics, CTR y posición media',
        'Las métricas de tráfico y posicionamiento no se infieren ni inventan desde el código o el marcado.',
        'Google Search Console Search Analytics API / exportación fechada',
        {'url': url},
    )

    priority_order = {'P1': 0, 'P2': 1, 'P3': 2}
    verified_by_tool.sort(key=lambda x: (priority_order.get(x['priority'], 9), x['id']))
    code_hypothesis.sort(key=lambda x: (priority_order.get(x['priority'], 9), x['id']))

    return {
        'kind': 'seo-technical-audit',
        'skill': 'seo-audit',
        'reused_engines': ['ipanema-seo-expert'] + (['web-quality-audit'] if reused_wqa_findings else []),
        'reused_web_quality_findings': reused_wqa_findings,
        'project': project.id,
        'url': redact(url),
        'page_type': page_type,
        'framework': detected_fw,
        'at': now(),
        'http_status': status,
        'indexability': idx_info,
        'indexation_claimed': False,
        'ranking_improvement_promised': False,
        'traffic_fabricated': False,
        'untrusted_page_data_ignored': True,
        'verified_by_tool': verified_by_tool,
        'code_hypothesis': code_hypothesis,
        'requires_external_verification': requires_external_verification,
        'counts': {
            'verified_by_tool': len(verified_by_tool),
            'code_hypothesis': len(code_hypothesis),
            'requires_external_verification': len(requires_external_verification),
            'p1_critical': sum(1 for i in verified_by_tool if i['priority'] == 'P1'),
            'p2_high': sum(1 for i in verified_by_tool if i['priority'] == 'P2'),
            'p3_medium_low': sum(1 for i in verified_by_tool if i['priority'] == 'P3'),
        },
        'base_page_audit': redact(base_audit),
        'limitations': [
            'El HTML y las cabeceras prueban señales técnicas observables, nunca que Google haya indexado o posicionado la URL.',
            'No se afirma ausencia de Schema cuando solo se inspecciona HTML estático sin captura del DOM renderizado.',
            'Los hallazgos en código (code_hypothesis) requieren confirmación en la salida renderizada.',
        ],
    }
