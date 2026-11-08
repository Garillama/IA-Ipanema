"""Validación de datos estructurados en cuatro niveles (A sintaxis, B semántica, C Google, D consistencia).

Las reglas de Google provienen de `google_requirements.json` (fechado). Un hallazgo nunca afirma elegibilidad:
`states` separa lo comprobado de lo no comprobado y nunca marca confirmación externa.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

from .consistency import check_consistency
from .schema_graph import as_list, build_graph, resolve_object, types_of
from .vocabulary import VOCAB, check_properties, offer_price, amount

REQ = json.loads((Path(__file__).with_name("google_requirements.json")).read_text(encoding="utf-8"))
FEATURES = REQ["features"]
KNOWN_TYPES = set(REQ["schema_org"]["known_types_checked"]) | set(VOCAB['types'])
AVAILABILITY = set(FEATURES["product_snippet"]["availability_values"])
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")
HAS_TZ = re.compile(r"(Z|[+-]\d{2}:?\d{2})$")
NUMBER = re.compile(r"^\d+(\.\d+)?$")
SEVERITIES = ("error", "warning", "recommendation", "optional")


def F(rule, level, severity, message, *, entity=None, path=None, evidence=None, source=None, fix=None, scope=None):
    assert severity in SEVERITIES
    return {"rule": rule, "level": level, "severity": severity, "message": message, "entity": entity, "path": path,
            "evidence": evidence, "source": source, "fix": fix, "scope": scope}


def val(obj, key):
    v = obj.get(key)
    return v[0] if isinstance(v, list) and v else v


def present(obj, key):
    v = obj.get(key)
    return v not in (None, "", [], {})


def abs_url(u):
    return isinstance(u, str) and bool(re.match(r"^https?://[^\s/]+", u))


def offers_of(obj):
    return [o for o in as_list(obj.get("offers")) if isinstance(o, dict)]


def level_a(snap):
    out = []
    for b in snap["json_ld"]:
        label = b.get("component") or f"script #{b['index']}"
        if b["error"]:
            e = b["error"]
            fix = {"trailing_comma": "Eliminar la coma previa a un cierre de lista/objeto: no emitir separadores condicionados a que un bucle tenga elementos; corregir en el snippet nativo, sin añadir otro script.",
                   "unescaped_control_character": "Serializar con json_encode (o equivalente) en vez de interpolar texto.",
                   "empty": "No emitir el script cuando no haya contenido."}.get(e["hint"], "Revisar la serialización del snippet que genera este script.")
            out.append(F("A001", "A", "error", f"JSON-LD no parseable ({e['message']}; causa probable: {e['hint']}).", entity=label,
                         path=f"línea {e['line']}, columna {e['column']} del script", evidence=e, fix=fix))
        elif b["data"] in (None, {}, []):
            out.append(F("A002", "A", "warning", "Script JSON-LD vacío.", entity=label))
    return out


def _check_url(out, ent, key, value, rule="B020"):
    if value is None:
        return
    if isinstance(value, str) and value.strip() in ("https:", "http:", "//", ""):
        out.append(F(rule, "B", "error", f"URL vacía o truncada en `{key}` ({value!r}).", entity=ent, path=key, evidence=value,
                     fix="Emitir la propiedad solo cuando la fuente tenga valor."))
    elif isinstance(value, str) and value.startswith("//"):
        out.append(F(rule, "B", "warning", f"URL relativa al protocolo en `{key}`.", entity=ent, path=key, evidence=value))
    elif isinstance(value, str) and not abs_url(value):
        out.append(F(rule, "B", "warning", f"`{key}` no es una URL absoluta http(s).", entity=ent, path=key, evidence=value))


def level_b(snap, graph):
    out = []
    for b in snap["json_ld"]:
        if b['error'] is None and b['data'] is not None and not isinstance(b['data'],(dict,list)):
            out.append(F('B000','B','error','La raíz JSON-LD debe ser objeto o lista de objetos.'))
        if isinstance(b["data"], (dict, list)):
            roots = [b["data"]] if isinstance(b["data"], dict) else [x for x in b["data"] if isinstance(x, dict)]
            for r in roots:
                if "@context" not in r:
                    out.append(F("B001", "B", "warning", "El script no declara @context.", entity=b.get("component") or f"script #{b['index']}"))
                ctx = r.get("@context")
                if isinstance(ctx, str) and ctx.startswith("http://"):
                    out.append(F("B002", "B", "optional", "@context usa http://; schema.org acepta ambos, https es la forma preferida.",
                                 entity=b.get("component") or f"script #{b['index']}", evidence=ctx))
    for e in graph["raw_entities"]:
        if e["ref_only"]:
            continue
        o, types = e["obj"], e["types"]
        label = f"{'/'.join(types) or '?'}@{e['component'] or e['block']}"
        for t in types:
            if t not in KNOWN_TYPES:
                out.append(F("B003", "B", "optional", f"Tipo `{t}` fuera del vocabulario que este motor verifica; no se evalúa.", entity=label))
        if "Offer" in types or "AggregateOffer" in types:
            if "Offer" in types and present(o, "price"):
                if not NUMBER.match(str(o["price"]).strip()):
                    out.append(F("B010", "B", "error", f"`price` no es un número sin formato ({o['price']!r}).", entity=label, path="price",
                                 fix="Usar punto decimal, sin símbolo ni separador de miles."))
            if present(o, "priceCurrency") and not re.fullmatch(r"[A-Z]{3}", str(o["priceCurrency"])):
                out.append(F("B011", "B", "error", f"`priceCurrency` no es un código ISO 4217 de 3 letras mayúsculas ({o['priceCurrency']!r}).", entity=label, path="priceCurrency"))
            av = o.get("availability")
            if present(o, "availability"):
                short = str(av).rsplit("/", 1)[-1]
                if short not in AVAILABILITY:
                    out.append(F("B012", "B", "warning", f"`availability` ({av!r}) no está entre los valores documentados por Google.", entity=label, path="availability"))
                elif str(av).startswith("http://"):
                    out.append(F("B013", "B", "optional", "`availability` con prefijo http://schema.org/; Google documenta https://schema.org/ o el nombre corto.", entity=label, evidence=av))
            _check_url(out, label, "url", o.get("url"))
        if "Product" in types or "ProductGroup" in types:
            br = o.get("brand")
            if isinstance(br, dict) and "Thing" in [str(t) for t in as_list(br.get("@type"))]:
                out.append(F("B020b", "B", "warning", "`brand` se declara como `Thing`; Google documenta `Brand` (u Organization).", entity=label, path="brand",
                             fix="Cambiar @type a Brand sin cambiar el nombre."))
            elif isinstance(br, str):
                out.append(F("B020c", "B", "recommendation", "`brand` es texto plano; un objeto Brand es más preciso.", entity=label, path="brand"))
            for img in as_list(o.get("image")):
                _check_url(out, label, "image", img if isinstance(img, str) else (img.get("url") if isinstance(img, dict) else None), "B021")
        if "BlogPosting" in types or "Article" in types or "NewsArticle" in types:
            au = o.get("author")
            if isinstance(au, str):
                out.append(F("B030", "B", "warning", "`author` es texto plano; Google y schema.org esperan Person u Organization.", entity=label, path="author",
                             fix="Emitir {\"@type\":\"Person\",\"name\":…} solo con el autor real del artículo."))
            for key in ("datePublished", "dateModified"):
                if present(o, key):
                    s = str(o[key])
                    if not ISO_DATE.match(s):
                        out.append(F("B031", "B", "warning", f"`{key}` no es ISO 8601 estricto ({s!r}).", entity=label, path=key,
                                     fix="Formatear con date('c') o equivalente; no reescribir el valor real."))
                    elif "T" in s and not HAS_TZ.search(s):
                        out.append(F("B032", "B", "recommendation", f"`{key}` sin zona horaria ({s!r}); Google la recomienda.", entity=label, path=key))
            _check_url(out, label, "url", o.get("url"))
        if "BreadcrumbList" in types:
            items = [i for i in as_list(o.get("itemListElement")) if isinstance(i, dict)]
            pos = [i.get("position") for i in items]
            if pos != list(range(1, len(pos) + 1)):
                out.append(F("B040", "B", "error", f"Posiciones de BreadcrumbList no consecutivas desde 1: {pos}.", entity=label, path="itemListElement"))
            for i, it in enumerate(items):
                if not present(it, "name") and not (isinstance(it.get("item"), dict) and present(it["item"], "name")):
                    out.append(F("B041", "B", "error", f"ListItem {i + 1} sin `name`.", entity=label))
                last = i == len(items) - 1
                if not present(it, "item") and not last:
                    out.append(F("B042", "B", "error", f"ListItem {i + 1} sin `item` (solo el último puede omitirlo).", entity=label))
                elif present(it, "item") and isinstance(it["item"], str):
                    _check_url(out, label, f"itemListElement[{i}].item", it["item"], "B043")
        if "ItemList" in types:
            items = [i for i in as_list(o.get("itemListElement")) if isinstance(i, dict)]
            pos = [i.get("position") for i in items]
            if not items:
                out.append(F("B050", "B", "warning", "ItemList sin itemListElement.", entity=label))
            elif any(p is not None and (type(p) is not int or p<1) for p in pos) or len({p for p in pos if p is not None})!=len([p for p in pos if p is not None]):
                out.append(F("B051", "B", "error", f"Posiciones de ItemList deben ser enteros positivos únicos: {pos}.", entity=label))
            urls = [(i.get("url") or (i.get("item") or {}).get("url") if isinstance(i.get("item"), dict) else i.get("url")) for i in items]
            dup = {u for u in urls if u and urls.count(u) > 1}
            if dup:
                out.append(F("B052", "B", "warning", "ItemList con URLs repetidas (¿slides clonados?).", entity=label, evidence=sorted(dup)))
        if "Organization" in types or "OnlineStore" in types:
            if isinstance(o.get("logo"), str):
                _check_url(out, label, "logo", o["logo"], "B060")
            for s in as_list(o.get("sameAs")):
                if not abs_url(s):
                    out.append(F("B061", "B", "warning", "`sameAs` contiene un valor que no es URL absoluta.", entity=label, evidence=s))
    return out


def _entities(graph, t, nested=None):
    result=[];seen=set()
    for e in graph['raw_entities']:
        if t not in e['types'] or e['ref_only'] or nested is not None and e['nested']!=nested:continue
        key=e['id'] or e['key']
        if key not in seen:result.append({**e,'obj':resolve_object(e['obj'],graph)});seen.add(key)
    return result


def level_c(snap, graph, page_type, facts):
    out = []
    ms, ps, mv = FEATURES["merchant_listing"], FEATURES["product_snippet"], FEATURES["product_variants"]
    products = _entities(graph, "Product")
    groups = _entities(graph, "ProductGroup")
    if page_type == "product":
        main = [p for p in products if not p["nested"] or p["parent_prop"] == "mainEntity"] or products
        if not main and not groups:
            out.append(F("C100", "C", "error", "Página de producto sin entidad Product/ProductGroup.", source=ms["source"], scope="merchant_listing"))
        for p in main:
            o, label = p["obj"], f"Product@{p['component'] or p['block']}"
            for req in ms["Product"]["required"]:
                if not present(o, req):
                    out.append(F("C101", "C", "error", f"Falta `{req}` (requerido para merchant listing).", entity=label, source=ms["source"], scope="merchant_listing"))
            if not (present(o, "review") or present(o, "aggregateRating") or present(o, "offers")):
                out.append(F("C102", "C", "error", "Product sin review, aggregateRating ni offers (requisito de product snippet).", entity=label, source=ps["source"], scope="product_snippet"))
            offers = [resolve_object(of,graph) for of in offers_of(o)]
            if present(o, "offers") and not offers:
                out.append(F("C103", "C", "warning", "`offers` es una referencia o valor no objeto; no se pudo evaluar la oferta.", entity=label))
            for of in offers:
                for req in ms["Offer"]["required"]:
                    price,currency=offer_price(of)
                    found=price is not None if req.startswith('price|') else currency is not None if req.startswith('priceCurrency|') else present(of,req)
                    if not found:
                        out.append(F("C110", "C", "error", f"Offer sin `{req}` (requerido).", entity=label, source=ms["source"], scope="merchant_listing"))
                if amount(offer_price(of)[0]) is not None and amount(offer_price(of)[0]) <= 0:
                    out.append(F("C111", "C", "error", "El precio activo debe ser mayor que cero.", entity=label, evidence=offer_price(of)[0], source=ms["source"], scope="merchant_listing"))
                for rec in ms["Offer"]["recommended"]:
                    if not present(of, rec):
                        sev = "warning" if rec == "availability" else "optional" if rec in ("shippingDetails", "hasMerchantReturnPolicy") else "recommendation"
                        note = " No se genera sin una fuente verificable de políticas." if rec in ("shippingDetails", "hasMerchantReturnPolicy") else ""
                        out.append(F("C112", "C", sev, f"Offer sin `{rec}` (recomendado).{note}", entity=label, source=ms["source"], scope="merchant_listing"))
                sd = of.get("shippingDetails")
                for s in as_list(sd):
                    if isinstance(s, dict):
                        for req in ([] if isinstance(s.get('hasShippingService'),dict) and s['hasShippingService'].get('@id') else ms["OfferShippingDetails"]["required_if_used"]):
                            if not present(s, req):
                                out.append(F("C113", "C", "error", f"OfferShippingDetails sin `{req}`.", entity=label, source=ms["source"]))
                rp = of.get("hasMerchantReturnPolicy")
                for r in as_list(rp):
                    if isinstance(r, dict):
                        for req in ms["MerchantReturnPolicy"]["required"]:
                            if not present(r, req):
                                out.append(F("C114", "C", "error", f"MerchantReturnPolicy sin `{req}`.", entity=label, source=ms["source"]))
                        if str(r.get('returnPolicyCategory','')).endswith('MerchantReturnFiniteReturnWindow') and not present(r,'merchantReturnDays'):
                            out.append(F('C115','C','error','La política de ventana finita requiere merchantReturnDays real.',source=ms['source'],scope='merchant_listing'))
            if not any(present(o, g) for g in ms["Product"]["gtin_alternatives"]):
                out.append(F("C120", "C", "recommendation", "Sin GTIN/ISBN (recomendado). No se deduce de SKU: solo si el catálogo lo contiene.", entity=label, source=ms["source"]))
            for rec in ("brand", "sku", "description"):
                if not present(o, rec):
                    out.append(F("C121", "C", "recommendation" if rec != "sku" else "recommendation", f"Product sin `{rec}` (recomendado).", entity=label, source=ms["source"]))
            if present(o, "aggregateRating"):
                ar = o["aggregateRating"] if isinstance(o["aggregateRating"], dict) else {}
                if not present(ar, "ratingValue") or not (present(ar, "reviewCount") or present(ar, "ratingCount")):
                    out.append(F("C130", "C", "error", "aggregateRating sin ratingValue o reviewCount/ratingCount.", entity=label, source=ps["source"]))
        if facts and facts.get("has_variants") and not groups:
            out.append(F("C140", "C", "recommendation", "El producto tiene variantes (según `facts`) pero no hay ProductGroup. Evaluar si el modelo de datos permite representarlas con URL por variante.",
                         source=mv["source"], scope="product_variants"))
        for g in groups:
            o, label = g["obj"], f"ProductGroup@{g['component'] or g['block']}"
            if not present(o, "name"):
                out.append(F("C141", "C", "error", "ProductGroup sin `name`.", entity=label, source=mv["source"]))
            if not present(o,'productGroupID') and not any(isinstance(v,dict) and present(resolve_object(v,graph),'inProductGroupWithID') for v in as_list(o.get('hasVariant'))):
                out.append(F('C146','C','error','El grupo requiere productGroupID o inProductGroupWithID en variantes.',entity=label,source=mv['source'],scope='product_variants'))
            for rec in ("variesBy", "hasVariant"):
                if not present(o, rec):
                    out.append(F("C142", "C", "warning", f"ProductGroup sin `{rec}`.", entity=label, source=mv["source"]))
            for vb in as_list(o.get("variesBy")):
                if str(vb).rsplit("/", 1)[-1] not in mv["ProductGroup"]["variesBy_values"]:
                    out.append(F("C143", "C", "warning", f"variesBy `{vb}` fuera de los valores documentados.", entity=label, source=mv["source"]))
            skus = []
            for v in as_list(o.get("hasVariant")):
                if isinstance(v, dict):
                    v=resolve_object(v,graph)
                    if set(v)<= {'url'}:continue
                    ident = v.get("sku") or v.get("gtin") or v.get("gtin13")
                    if not ident:
                        out.append(F("C144", "C", "error", "Variante sin identificador único (sku/gtin).", entity=label, source=mv["source"]))
                    skus.append(ident)
            dup = {s for s in skus if s and skus.count(s) > 1}
            if dup:
                out.append(F("C145", "C", "error", "Variantes con identificador repetido.", entity=label, evidence=sorted(dup), source=mv["source"]))
    else:
        offered = [p for p in products if offers_of(p["obj"])]
        if page_type in ("category", "home", "search", "blog", "post", "page") and offered:
            out.append(F("C200", "C", "warning",
                         f"{len(offered)} entidad(es) Product con Offer en una página `{page_type}`. No son merchant listings de PDP. Revisar finalidad semántica y posible beta regional separada, sin retirar marcado válido automáticamente.",
                         source=ms["source"], scope="merchant_listing",
                         evidence=[p["component"] or p["block"] for p in offered][:5],
                         fix="No añadir duplicados por tarjeta; revisar finalidad y coherencia de las entidades nativas. ItemList de URLs puede ser alternativa semántica, sin promesa de resultado enriquecido."))
    for t in _entities(graph, "ItemList"):
        n = len([i for i in as_list(t["obj"].get("itemListElement")) if isinstance(i, dict)])
        out.append(F("C210", "C", "optional", f"ItemList con {n} elemento(s): no concede un carrusel enriquecido. La modalidad tradicional y la beta regional tienen requisitos separados.",
                     entity=f"ItemList@{t['component'] or t['block']}", source=FEATURES["carousel"]["source"], scope="carousel"))
        if (facts or {}).get('google_experience')=='carousel_beta':
            beta=FEATURES['carousel_beta'];items=as_list(t['obj'].get('itemListElement'))
            if n<beta['min_items']:
                out.append(F('C211','C','error','La beta requiere al menos 3 elementos reales.',scope='carousel_beta',source=beta['source']))
            for i,item in enumerate(items):
                item=resolve_object(item,graph) if isinstance(item,dict) else {}
                detail=resolve_object(item.get('item',{}),graph) if isinstance(item.get('item'),dict) else {}
                if not detail or any(not present(detail,k) for k in beta['required_item_properties']) or item.get('position')!=i+1:
                    out.append(F('C212','C','error','Elemento beta sin entidad name/image/url y posición requerida.',scope='carousel_beta',source=beta['source']))
            if (facts or {}).get('market') in beta['excluded_product_markets'] and any('Product' in types_of(resolve_object(i.get('item',{}),graph)) for i in items if isinstance(i,dict)):
                out.append(F('C213','C','warning','La beta de productos no está documentada como disponible para México.',scope='carousel_beta',source=beta['source']))
    bcs = _entities(graph, "BreadcrumbList")
    for bc in bcs:
        n = len([i for i in as_list(bc["obj"].get("itemListElement")) if isinstance(i, dict)])
        if n < FEATURES["breadcrumb"]["BreadcrumbList"]["min_items"]:
            out.append(F("C220", "C", "warning" if page_type != "home" else "optional",
                         f"BreadcrumbList con {n} elemento(s); Google requiere al menos 2 para esta función.", entity=f"BreadcrumbList@{bc['component'] or bc['block']}",
                         source=FEATURES["breadcrumb"]["source"], scope="breadcrumb"))
    if not bcs and page_type in ("category", "product", "post", "page"):
        out.append(F("C221", "C", "recommendation", f"Sin BreadcrumbList en página `{page_type}`.", source=FEATURES["breadcrumb"]["source"], scope="breadcrumb"))
    if page_type == "post":
        posts = _entities(graph, "BlogPosting") + _entities(graph, "Article")
        main = [p for p in posts if not p["nested"]] or posts
        if not main:
            out.append(F("C300", "C", "recommendation", "Artículo sin BlogPosting/Article.", source=FEATURES["article"]["source"], scope="article"))
        for p in main[:1]:
            for rec in ("author", "headline", "image", "datePublished", "dateModified"):
                if not present(p["obj"], rec):
                    out.append(F("C301", "C", "recommendation", f"Artículo sin `{rec}` (recomendado). No inventar valores: omitir si el CMS no los tiene.",
                                 entity=f"{p['types'][0]}@{p['component'] or p['block']}", source=FEATURES["article"]["source"], scope="article"))
    for t in _entities(graph, "FAQPage"):
        out.append(F("C400", "C", "optional", "FAQPage describe preguntas, pero el resultado enriquecido FAQ de Google está retirado (2026-05-07). No es un beneficio de presentación.",
                     entity=f"FAQPage@{t['component'] or t['block']}", source=FEATURES["faq"]["source"], scope="faq"))
    for t in _entities(graph, "SearchAction"):
        out.append(F("C410", "C", "optional", "SearchAction: la función de sitelinks searchbox fue retirada; solo mantener si refleja una búsqueda real y por semántica.",
                     source=FEATURES["sitelinks_searchbox"]["source"], scope="sitelinks_searchbox"))
    return out


def level_graph(graph):
    out = []
    for d in graph["duplicates"]:
        out.append(F("G001", "D", "warning", f"Entidad duplicada ({'/'.join(d['types'])}, {d['count']} apariciones).", evidence=d["locations"],
                     fix="Unificar la fuente: un solo script por entidad; referenciar con @id en lugar de repetir."))
    for c in graph["conflicts"]:
        out.append(F("G002", "D", "error", f"Valores contradictorios para `{c['property']}` de la misma entidad.", evidence=c))
    for s in graph["repeated_singletons"]:
        if s["distinct_identities"] > 1:
            out.append(F("G003", "D", "warning", f"{s['count']} entidades {s['type']} distintas en una misma página.", evidence=s))
    for r in graph["dangling_references"]:
        out.append(F("G004", "B", "recommendation", f"Referencia @id no resuelta en esta página; puede ser externa y válida: {r['id']}", evidence=r))
    for issue in graph.get('incompatible_id_types',[]):
        out.append(F('G006','B','warning','Un @id mezcla entidades de tipos incompatibles; comprobar identidad de página y producto.',evidence=issue))
    sp = graph["identity_split"]
    if sp["nested_unreferenced_organizations"] and sp["global_organizations"]:
        out.append(F("G005", "D", "optional",
                     f"{sp['nested_unreferenced_organizations']} Organization anidada(s) sin @id junto a una Organization global: la identidad del negocio está dividida.",
                     evidence=sp["paths"], fix="Asignar @id estable a la Organization global y referenciarla (seller/publisher/author)."))
    return out


def validate(snap: dict, page_type: str, facts: dict | None = None):
    graph = build_graph(snap)
    findings = level_a(snap) + level_b(snap, graph) + level_c(snap, graph, page_type, facts) + level_graph(graph) \
        + check_consistency(snap, graph, page_type, facts or {})
    problems,unchecked=check_properties(graph)
    findings += [F('B100','B',severity,message,entity=entity,path=prop,source=VOCAB['source']['url']) for severity,entity,prop,message in problems]
    by_sev = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITIES}
    scopes = {}
    for f in findings:
        if f["scope"]:
            scopes.setdefault(f["scope"], []).append(f["severity"])
    applicable = [k for k, v in FEATURES.items() if page_type in v.get("applies_to_page_types", [])]
    product_nodes=_entities(graph,'Product')
    for product in product_nodes if page_type=='product' else []:
        o=product['obj']
        if not present(o,'name'):
            findings.append(F('C150','C','error','Product sin name para product snippet.',scope='product_snippet',source=FEATURES['product_snippet']['source']))
        if not any(present(o,k) for k in ('offers','review','aggregateRating')):
            findings.append(F('C151','C','error','Product snippet requiere offers, review o aggregateRating.',scope='product_snippet',source=FEATURES['product_snippet']['source']))
        for offer in [resolve_object(v,graph) for v in offers_of(o)]:
            if 'AggregateOffer' in as_list(offer.get('@type')):
                missing=any(not present(offer,k) for k in ('lowPrice','priceCurrency'))
            else:missing=offer_price(offer)[0] is None
            if missing:findings.append(F('C152','C','error','Oferta sin precio requerido para product snippet.',scope='product_snippet',source=FEATURES['product_snippet']['source']))
    by_sev={s:sum(f['severity']==s for f in findings) for s in SEVERITIES}
    present_by_feature={'merchant_listing':bool(product_nodes or _entities(graph,'ProductGroup')),
        'product_snippet':bool(product_nodes),'product_variants':bool(_entities(graph,'ProductGroup')),
        'breadcrumb':bool(_entities(graph,'BreadcrumbList')),'article':bool(_entities(graph,'Article')+_entities(graph,'BlogPosting')),
        'organization':bool(_entities(graph,'Organization')+_entities(graph,'OnlineStore')),'carousel_beta':bool(_entities(graph,'ItemList'))}
    feature_states={}
    for feature in applicable:
        if not present_by_feature.get(feature):feature_states[feature]='not_present'
        elif feature=='carousel_beta':feature_states[feature]='regional_program_and_content_requirements_not_verified'
        elif any(f['scope']==feature and f['severity']=='error' for f in findings):feature_states[feature]='missing_requirements'
        else:feature_states[feature]='checked_subset_no_missing'
    states = {
        "syntax_valid": not any(f["rule"] == "A001" for f in findings) if snap['json_ld'] else None,
        "semantic_valid_for_checked_rules": (not any(f["level"] == "B" and f["severity"] == "error" for f in findings)) if graph['entities'] else None,
        "google_requirements_met_by_feature": feature_states,
        "consistency": ("contradictions" if any(f["level"] == "D" and f["severity"] == "error" for f in findings)
                        else "partially_compared_with_provided_facts" if facts else "not_verified_no_facts"),
        "potentially_eligible": "unconfirmed — cumplir propiedades no garantiza resultados enriquecidos",
        "confirmed_by_external_tool": "not_checked",
        "observed_in_google": "not_checked",
    }
    return {"findings": findings, "counts": by_sev, "states": states,
            'unchecked_properties':unchecked,'semantic_scope':'Vocabulario acotado; no expansión JSON-LD ni RDFa completa.',
            "graph": {k: graph[k] for k in ("entities", "edges", "duplicates", "conflicts", "dangling_references", "repeated_singletons", "identity_split", "types")},
            "requirements": {"retrieved_at": REQ["retrieved_at"], "file": "tools/ipanema/seo/google_requirements.json"}}
