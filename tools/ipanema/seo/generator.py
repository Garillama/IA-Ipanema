"""Generación propuesta desde evidencia del proyecto; nunca escribe en un tema."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, urldefrag

from ..core import IpanemaError, beneath, digest, now, reject_secrets, safe_url
from .extractor import extract, parse_json_ld, trailing_commas
from .schema_graph import build_graph, as_list, resolve_object
from .schema_validator import validate
from .vocabulary import amount, valid_date, http_url


def own_url(project,value):
    base,_=urldefrag(value)
    safe_url(base)
    expected=urlsplit(project.data.get('public_url') or project.data.get('qa_base_url') or '')
    target=urlsplit(base)
    if not expected.hostname or (target.scheme,target.netloc)!=(expected.scheme,expected.netloc):
        raise IpanemaError('URL ajena al dominio del proyecto; no copiar datos entre tiendas.')
    return value


def checked_facts(project,document,*,fixture=False):
    if not isinstance(document,dict) or document.get('project')!=project.id:
        raise IpanemaError('Los datos no pertenecen al proyecto activo.')
    own_url(project,document.get('url',''))
    source=document.get('source',{})
    if not isinstance(source,dict) or not source.get('observed_at') or not valid_date(source['observed_at']):
        raise IpanemaError('La fuente debe tener fecha real, tipo y referencia verificable.')
    kind=source.get('kind')
    if kind=='synthetic_fixture':
        if not fixture:raise IpanemaError('Los datos sintéticos solo se aceptan en pruebas explícitas.')
        data=document.get('data',{})
    else:
        if kind not in ('authorized_catalog_export','authorized_cms_export','official_api_export'):
            raise IpanemaError('Se necesita catálogo/CMS/API autorizado, no texto visual ni el schema que se audita.')
        relative=source.get('reference')
        if not isinstance(relative,str):raise IpanemaError('Falta referencia a evidencia comercial local revisada.')
        path=(project.root/relative).resolve()
        if not beneath(path,project.root/'reports') or not path.is_file() or path.stat().st_size>5_000_000:
            raise IpanemaError('La evidencia comercial debe ser un JSON de hasta 5 MB dentro de reports/.')
        if source.get('sha256')!=digest(path):raise IpanemaError('La evidencia comercial cambió o no tiene hash correcto.')
        evidence=json.loads(path.read_text(encoding='utf-8'))
        if evidence.get('project')!=project.id or evidence.get('url')!=document['url']:
            raise IpanemaError('La evidencia corresponde a otra tienda o URL.')
        data=evidence.get('data',{})
        if 'data' in document and document['data']!=data:raise IpanemaError('Los valores proporcionados contradicen la evidencia referenciada.')
    if not isinstance(data,dict):raise IpanemaError('data debe ser un objeto normalizado de catálogo/CMS.')
    reject_secrets(data)
    return deepcopy(data),{'kind':kind,'reference':source.get('reference'),'sha256':source.get('sha256'),
        'observed_at':source['observed_at'],'status':'synthetic_fixture' if kind=='synthetic_fixture' else 'referenced_artifact_checked_not_independent_business_verification'}


def validation_facts(data):
    product=data.get('product',{})
    return {**product,'variants':product.get('variants',[]),
            'reviews_source':data.get('reviews',{}).get('source'),
            'policies_source':data.get('policies',{}).get('source')}


def safe_json(value):
    return json.dumps(value,ensure_ascii=False,allow_nan=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')


def repair_trailing_json(raw):
    if parse_json_ld(raw)[1] is None:return {'status':'already_parseable','json':raw,'changed':False}
    positions=set(trailing_commas(raw))
    repaired=''.join(ch for i,ch in enumerate(raw) if i not in positions)
    if not positions or parse_json_ld(repaired)[1] is not None:
        raise IpanemaError('No es un caso reparable únicamente quitando comas finales; corregir la fuente.')
    return {'status':'repaired_artifact_only','json':repaired,'changed':True,
            'original_sha256':hashlib.sha256(raw.encode()).hexdigest(),'commas_removed':len(positions),
            'limitation':'Reparar la captura no corrige el generador nativo ni publica cambios.'}


def generate(project,document,target,*,snapshot=None,mode='missing',entity_id=None,fixture=False):
    if mode not in ('missing','update'):raise IpanemaError('Modo de propuesta no soportado.')
    data,provenance=checked_facts(project,document,fixture=fixture)
    page_type=document.get('page_type')
    allowed={'Product':{'product'},'ProductGroup':{'product'},'Organization':{'home'},'OnlineStore':{'home'},
             'WebSite':{'home'},'WebPage':{'home','category','product','blog','post','page'},'CollectionPage':{'category','blog'},
             'BreadcrumbList':{'category','product','post','page','blog'},'ItemList':{'home','category','blog','post'},
             'Blog':{'blog'},'BlogPosting':{'post'},'Article':{'post'}}
    if target not in allowed or page_type not in allowed[target]:raise IpanemaError('Schema no apropiado para este tipo de página o no soportado por generación segura.')
    graph=build_graph(snapshot or extract('',document['url']))
    if snapshot and any(b['error'] for b in snapshot['json_ld']):
        raise IpanemaError('Hay JSON-LD inválido: corregir el generador nativo antes de añadir marcado.')
    equivalents={target}
    if target in ('Organization','OnlineStore'):equivalents|={'Organization','OnlineStore'}
    if target in ('Article','BlogPosting'):equivalents|={'Article','BlogPosting'}
    if target in ('WebPage','CollectionPage'):equivalents|={'WebPage','CollectionPage'}
    candidates=[e for e in graph['raw_entities'] if set(e['types'])&equivalents and not e['ref_only']]
    unique={e['id'] or e['key']:e for e in candidates}
    existing=None
    if candidates:
        if mode!='update':raise IpanemaError('La entidad ya existe: reutilizar/corregir su fuente, no duplicarla.')
        if entity_id:
            existing=next((e for e in candidates if e['id']==entity_id or e['obj'].get('@id')==entity_id),None)
        elif len(unique)==1:existing=next(iter(unique.values()))
        if existing is None:raise IpanemaError('Selecciona explícitamente qué entidad existente corregir.')
        if graph['conflicts']:raise IpanemaError('Entidades contradictorias: resolver fuentes antes de elegir valores.')
    elif mode=='update':raise IpanemaError('No existe la entidad seleccionada; no simular una actualización.')
    ids=data.get('identifiers',{})
    for value in ids.values():own_url(project,value)
    def decorate(obj,key):
        ident=ids.get(key)
        if ident:obj['@id']=ident
        return obj
    def product(obj):
        if not obj.get('name') or amount(obj.get('price')) is None or not obj.get('currency') or not obj.get('image'):
            raise IpanemaError('Product requiere nombre, imagen, precio y moneda respaldados para esta generación comercial.')
        if amount(obj['price'])<=0 or not __import__('re').fullmatch('[A-Z]{3}',obj['currency']):raise IpanemaError('Precio/moneda comercial inválidos.')
        url=own_url(project,obj.get('url',document['url']))
        images=as_list(obj['image'])
        if any(not http_url(i) for i in images):raise IpanemaError('Imagen sin URL verificable.')
        result={'@type':'Product','name':obj['name'],'url':url,'image':images,
                'offers':{'@type':'Offer','url':url,'price':str(obj['price']),'priceCurrency':obj['currency']}}
        if obj.get('availability'):
            from .schema_validator import AVAILABILITY
            availability=obj['availability'].rsplit('/',1)[-1]
            if availability not in AVAILABILITY:raise IpanemaError('Disponibilidad no reconocida; no asumir InStock.')
            result['offers']['availability']='https://schema.org/'+availability
        for key in ('sku','gtin','gtin8','gtin12','gtin13','gtin14','mpn','description','color','size','material','pattern'):
            if obj.get(key) is not None:result[key]=obj[key]
        if obj.get('brand'):result['brand']={'@type':'Brand','name':obj['brand']}
        reviews=data.get('reviews',{})
        if reviews.get('aggregateRating') is not None or reviews.get('review') is not None:
            if not reviews.get('source') or reviews.get('verified') is not True or reviews.get('product_url')!=url:
                raise IpanemaError('Reseñas sin fuente real verificada para ese producto/variante.')
            for key in ('aggregateRating','review'):
                if reviews.get(key) is not None:result[key]=reviews[key]
        policies=data.get('policies',{})
        for key in ('shippingDetails','hasMerchantReturnPolicy'):
            if policies.get(key) is not None:
                if not policies.get('source') or policies.get('verified') is not True:raise IpanemaError('Políticas no verificadas; no generar envío gratuito/plazos/devoluciones.')
                result['offers'][key]=policies[key]
        return result
    if target=='Product':node=decorate(product(data.get('product',{})),'product')
    elif target=='ProductGroup':
        group=data.get('product',{});variants=group.get('variants',[])
        if not group.get('productGroupID') or not group.get('variesBy') or len(variants)<2 or not group.get('variant_urls_verified'):
            raise IpanemaError('El grupo requiere ID real, dimensiones, variantes y URLs de selección comprobadas.')
        node={'@type':'ProductGroup','name':group.get('name'),'productGroupID':group['productGroupID'],'variesBy':group['variesBy'],'hasVariant':[]}
        seen=set();seen_urls=set()
        for variant in variants:
            ident=variant.get('sku') or next((variant.get(k) for k in ('gtin','gtin13','gtin12','gtin14') if variant.get(k)),None)
            if not ident or ident in seen or not variant.get('url') or variant['url'] in seen_urls:raise IpanemaError('Cada variante necesita identificador único y URL real distinta.')
            seen_urls.add(variant['url'])
            seen.add(ident);node['hasVariant'].append(product(variant))
        decorate(node,'product_group')
    elif target in ('Organization','OnlineStore'):
        org=data.get('organization',{})
        if target=='OnlineStore' and org.get('business_type')!='OnlineStore':raise IpanemaError('OnlineStore requiere confirmar el tipo real de negocio en la fuente.')
        if not org.get('name') or not org.get('url'):raise IpanemaError('Identidad del negocio incompleta.')
        node={'@type':target,'name':org['name'],'url':own_url(project,org['url'])}
        for k in ('logo','sameAs','legalName','address','telephone'):
            if org.get(k) is not None:node[k]=org[k]
        decorate(node,'organization')
    elif target=='BreadcrumbList':
        crumbs=data.get('breadcrumbs',[])
        if len(crumbs)<2:raise IpanemaError('No emitir BreadcrumbList vacío o inventar niveles para completarlo.')
        node={'@type':target,'itemListElement':[]}
        for i,c in enumerate(crumbs):
            if not c.get('name') or not c.get('url'):raise IpanemaError('Breadcrumb sin nombre o destino respaldado.')
            node['itemListElement'].append({'@type':'ListItem','position':i+1,'name':c['name'],'item':own_url(project,c['url'])})
    elif target=='ItemList':
        items=data.get('items',[])
        if not items:raise IpanemaError('No hay una lista real para representar.')
        node={'@type':target,'itemListElement':[]};seen=set()
        for i,item in enumerate(items):
            url=own_url(project,item['url'])
            if url in seen:raise IpanemaError('Lista con duplicados/clones; resolver el conjunto real antes de generar.')
            seen.add(url);li={'@type':'ListItem','position':item.get('position',i+1),'url':url}
            if item.get('name'):li['name']=item['name']
            node['itemListElement'].append(li)
    elif target in ('BlogPosting','Article'):
        article=data.get('article',{})
        if not article.get('headline'):raise IpanemaError('Artículo sin título real.')
        node={'@type':target,'headline':article['headline'],'url':own_url(project,article.get('url',document['url']))}
        for key in ('description','image','inLanguage','articleSection','keywords','author','publisher','datePublished','dateModified','mainEntityOfPage'):
            if article.get(key) is not None:
                if key.startswith('date') and not valid_date(article[key]):raise IpanemaError('Fecha editorial inválida; no sustituir por hoy.')
                node[key]=article[key]
        decorate(node,'article')
    else:
        page=data.get('page',{})
        node={'@type':target,'url':document['url']}
        if page.get('name'):node['name']=page['name']
        if page.get('description'):node['description']=page['description']
        decorate(node,'website' if target=='WebSite' else 'webpage')
    if existing:
        preserved=resolve_object(existing['obj'],graph)
        def merge(old,new):
            result=deepcopy(old)
            for key,value in new.items():
                result[key]=merge(result[key],value) if isinstance(value,dict) and isinstance(result.get(key),dict) else deepcopy(value)
            return result
        node=merge(preserved,node)
        if preserved.get('@id'):node['@id']=preserved['@id']
    node={**node,'@context':'https://schema.org'}
    raw=safe_json(node)
    result=validate(extract('<script type="application/ld+json">'+raw+'</script>',document['url']),page_type,validation_facts(data))
    errors=[f for f in result['findings'] if f['severity']=='error']
    if errors:raise IpanemaError('La propuesta no supera las reglas locales: '+', '.join(sorted({f['rule'] for f in errors})))
    return {'kind':'schema-proposal','project':project.id,'url':document['url'],'at':now(),'target':target,
            'action':'replace_existing_at_source' if existing else 'add_only_if_still_missing',
            'source_entity':existing['key'] if existing else None,'data':node,'json_ld':raw,'validation':result,
            'provenance':provenance,'theme_modified':False,'published':False,'external_eligibility':'not_checked',
            'limitations':['Propuesta local; no insertarla junto a la entidad nativa que reemplaza.','La evidencia aportada no certifica verdad comercial independientemente.']}
