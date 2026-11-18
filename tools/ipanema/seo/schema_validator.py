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


SCHEMA_FRAMEWORK_CANDIDATES = {
    "shopify-liquid": [
        "sections/main-product.liquid",
        "snippets/product-schema.liquid",
        "layout/theme.liquid",
        "templates/product.json",
    ],
    "shopify-hydrogen": [
        "app/routes/products.$handle.tsx",
        "app/root.tsx",
        "app/lib/seo.server.ts",
    ],
    "react-web": [
        "src/pages/Product.tsx",
        "src/components/JsonLd.tsx",
        "index.html",
    ],
    "tiendanube-ipanema": [
        "snippets/structured-data/structured-data.tpl",
        "layouts/layout.tpl",
        "templates/product.tpl",
    ],
}

EXTERNAL_APP_MARKERS = re.compile(
    r"(judge\.?me|jdgm|loox|yotpo|stamped|smart.?seo|json-?ld.?for.?seo|sherpas|booster.?seo|yoast|avada|okendo|reviews\.io)",
    re.I,
)

PLACEHOLDER_VALUE_RE = re.compile(r"^(?:tbd|n/a|todo|null|undefined|none|\{\{.*\}\}|\{%.*%\})$", re.I)

RETIRED_GOOGLE_FEATURES = {
    "FAQPage": "FAQ rich results fueron retirados de forma general por Google el 2026-05-07; válido en Schema.org si refleja FAQs visibles, pero no promete rich result.",
    "HowTo": "HowTo rich results fueron retirados por Google en septiembre de 2023; válido en Schema.org, sin elegibilidad de rich result.",
    "SearchAction": "Sitelinks search box fue retirado por Google en noviembre de 2024; WebSite sigue siendo válido para site name.",
}


def _scan_unbacked_or_placeholder_values(obj, path="$"):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "@context":
                continue
            found.extend(_scan_unbacked_or_placeholder_values(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            found.extend(_scan_unbacked_or_placeholder_values(item, f"{path}[{idx}]"))
    elif isinstance(obj, str) and PLACEHOLDER_VALUE_RE.match(obj.strip()):
        found.append({"path": path, "value": obj.strip()})
    return found


def audit_and_propose_schema(
    project,
    html: str,
    url: str,
    page_type: str = "product",
    *,
    rendered_html: str | None = None,
    facts_doc: dict | None = None,
    source_files: dict[str, str] | None = None,
    propose_target: str | None = None,
    propose_mode: str = "missing",
    framework: str | None = None,
    fixture: bool = False,
) -> dict:
    """Auditoría y propuesta especializada Schema Markup (Etapa 4): reutiliza motor SEO y separa 5 estados y 3 niveles de evidencia."""
    from ..core import redact
    from ..performance.model import infer_framework
    from .extractor import extract
    from .generator import checked_facts, generate, repair_trailing_json, validation_facts

    detected_fw = infer_framework(framework, source_files)
    candidate_files = SCHEMA_FRAMEWORK_CANDIDATES.get(detected_fw, SCHEMA_FRAMEWORK_CANDIDATES["tiendanube-ipanema"])

    facts_data = None
    val_facts = {}
    if facts_doc is not None:
        checked, _ = checked_facts(project, facts_doc, fixture=fixture)
        facts_data = checked
        val_facts = validation_facts(checked)

    effective_html = rendered_html if rendered_html is not None else html
    initial_snap = extract(html, url)
    snap = extract(effective_html, url)
    val_report = validate(snap, page_type, val_facts if val_facts else None)
    graph = build_graph(snap)

    verified_by_tool = []
    code_hypothesis = []
    requires_external_verification = []

    def add_verified(rule_id, severity, title, impact, evidence, fix, files=None):
        verified_by_tool.append({
            "id": rule_id,
            "severity": severity,
            "evidence_type": "verified_by_tool",
            "title": title,
            "impact": impact,
            "evidence": redact(evidence),
            "candidate_files": files or candidate_files,
            "fix": fix,
        })

    def add_hypothesis(rule_id, severity, title, impact, evidence, fix, files):
        code_hypothesis.append({
            "id": rule_id,
            "severity": severity,
            "evidence_type": "code_hypothesis",
            "title": title,
            "impact": impact,
            "evidence": redact(evidence),
            "candidate_files": files,
            "fix": fix,
        })

    def add_external(rule_id, title, reason, required_source, evidence=None):
        requires_external_verification.append({
            "id": rule_id,
            "evidence_type": "requires_external_verification",
            "title": title,
            "reason": reason,
            "required_source": required_source,
            "evidence": redact(evidence or {}),
        })

    # 1. Inventario de bloques JSON-LD y detección de procedencia (tema, snippet, metafield, Hydrogen o app externa)
    initial_raws = {b["raw"].strip() for b in initial_snap.get("json_ld", []) if b.get("raw")}
    blocks_inventory = []
    external_app_blocks = []
    for block in snap.get("json_ld", []):
        comp = str(block.get("component") or "")
        raw_text = str(block.get("raw") or "")
        app_match = EXTERNAL_APP_MARKERS.search(comp) or EXTERNAL_APP_MARKERS.search(raw_text[:400])
        is_js_injected = rendered_html is not None and raw_text.strip() not in initial_raws
        if app_match:
            origin_kind = "external_seo_app"
            app_name = app_match.group(0)
            external_app_blocks.append({"block": block["index"], "app": app_name})
        elif is_js_injected:
            origin_kind = "client_js_injected"
            app_name = None
        else:
            origin_kind = "theme_or_template"
            app_name = None
        blocks_inventory.append({
            "index": block["index"],
            "component": block.get("component"),
            "line": block.get("line"),
            "bytes": block.get("bytes"),
            "syntax_valid": block.get("error") is None,
            "error": block.get("error"),
            "origin_kind": origin_kind,
            "external_app": app_name,
            "auto_modify_allowed": origin_kind == "theme_or_template",
        })

    if external_app_blocks:
        add_external(
            "SCHEMA-EXT-APP-OWNERSHIP",
            "Marcado JSON-LD generado por aplicación SEO/reseñas externa",
            "No se deben eliminar ni modificar automáticamente bloques inyectados por apps externas sin autorización explícita; revisar la configuración de la app o enlazar por @id.",
            "Configuración de la app en el panel de la tienda (Shopify/Tiendanube)",
            {"external_app_blocks": external_app_blocks},
        )

    # 2. Incorporar hallazgos del validador A–D (respetando la regla de no afirmar falta de Schema en HTML estático sin DOM renderizado)
    for f in val_report["findings"]:
        if rendered_html is None and f["rule"] in ("C100", "C221", "C300") and not snap.get("json_ld") and not snap.get("microdata"):
            continue
        add_verified(
            f["rule"],
            f["severity"],
            f["message"],
            f"Nivel {f['level']} de validación de datos estructurados.",
            {"entity": f.get("entity"), "path": f.get("path"), "details": f.get("evidence")},
            f.get("fix") or "Ajustar la propiedad en el generador o plantilla correspondiente con datos reales.",
        )

    # 3. Validaciones adicionales de tipos prioritarios: AggregateOffer, LocalBusiness, Review y Placeholders sin respaldo real
    for ent in graph["raw_entities"]:
        if ent["ref_only"]:
            continue
        obj, types = ent["obj"], ent["types"]
        label = f"{'/'.join(types) or '?'}@{ent['component'] or ent['block']}"

        # Placeholders o plantillas sin resolver en JSON-LD
        placeholders = _scan_unbacked_or_placeholder_values(obj)
        if placeholders:
            add_verified(
                "SCHEMA-UNBACKED-PLACEHOLDER",
                "error",
                "Propiedad JSON-LD con valor placeholder o variable de plantilla sin resolver",
                "Publica datos ficticios o expresiones Liquid/Twig crudas en el marcado estructurado.",
                {"entity": label, "placeholders": placeholders},
                "Condicionar la emisión de la propiedad a que exista un valor real en el objeto del catálogo.",
            )

        if "AggregateOffer" in types:
            low = amount(obj.get("lowPrice"))
            high = amount(obj.get("highPrice"))
            if low is None or low <= 0:
                add_verified(
                    "SCHEMA-AGGOFFER-LOWPRICE",
                    "error",
                    "AggregateOffer sin lowPrice numérico positivo",
                    "Google requiere lowPrice y priceCurrency válidos para evaluar rangos de precios.",
                    {"entity": label, "lowPrice": obj.get("lowPrice")},
                    "Asignar el precio mínimo real de las variantes activas (ej. product.price_min).",
                )
            if low is not None and high is not None and high < low:
                add_verified(
                    "SCHEMA-AGGOFFER-RANGE-INVALID",
                    "error",
                    f"AggregateOffer con highPrice ({high}) menor que lowPrice ({low})",
                    "Contradicción numérica en el rango de ofertas del producto.",
                    {"entity": label, "lowPrice": low, "highPrice": high},
                    "Asegurar que lowPrice corresponda al mínimo y highPrice al máximo.",
                )

        if "LocalBusiness" in types:
            if not present(obj, "name") or not present(obj, "address"):
                add_verified(
                    "SCHEMA-LOCALBUSINESS-REQUIRED",
                    "error",
                    "LocalBusiness sin name o address requeridos",
                    "Las entidades de negocio local requieren nombre y dirección postal verificable.",
                    {"entity": label, "has_name": present(obj, "name"), "has_address": present(obj, "address")},
                    "Incluir name y PostalAddress real del negocio sin inventar datos de ubicación.",
                )

        if "Review" in types:
            if not present(obj, "author") or not present(obj, "reviewRating"):
                add_verified(
                    "SCHEMA-REVIEW-INCOMPLETE",
                    "error",
                    "Entidad Review sin author o reviewRating",
                    "Una reseña estructurada requiere autor real y calificación.",
                    {"entity": label},
                    "Emitir Review solo cuando provenga de reseñas reales con autor y puntuación.",
                )

    # 4. Tipos retirados en Google Rich Results (FAQPage, HowTo, SearchAction)
    retired_present = {
        t: note for t, note in RETIRED_GOOGLE_FEATURES.items() if t in graph["types"]
    }

    # 5. Inspección de archivos fuente (Shopify Liquid, Hydrogen, React, Tiendanube) -> code_hypothesis
    source_architecture = []
    for path, content in sorted((source_files or {}).items()):
        if not isinstance(content, str):
            continue
        lower = content.lower()
        uses_structured_data_filter = "structured_data" in lower and "{{" in content
        uses_metafields = "metafields." in lower
        uses_liquid_product = "product." in lower or "selected_or_first_available_variant" in lower
        uses_hydrogen_seo = "<seo" in lower or "getseometa" in lower or "storefront.query" in lower
        has_manual_product_ld = bool(re.search(r'"@type"\s*:\s*"Product"', content))

        source_architecture.append({
            "file": path,
            "uses_shopify_structured_data_filter": uses_structured_data_filter,
            "uses_metafields": uses_metafields,
            "uses_liquid_objects": uses_liquid_product,
            "uses_hydrogen_storefront": uses_hydrogen_seo,
            "has_manual_product_jsonld": has_manual_product_ld,
        })

        if uses_structured_data_filter and has_manual_product_ld:
            add_hypothesis(
                "SCHEMA-SRC-DUPLICATE-PRODUCT-FILTER",
                "warning",
                "La plantilla combina `{{ product | structured_data }}` con un bloque JSON-LD `Product` manual",
                "Generará entidades Product duplicadas en el HTML final si ambos bloques se renderizan sin unificar @id.",
                {"file": path},
                "Conservar una única fuente de Product o referenciar mediante @id.",
                [path],
            )
        if re.search(r'"ratingValue"\s*:\s*"?[45](?:\.\d+)?"?', content) and "metafield" not in lower and "review" not in lower.split("ratingvalue")[0][-120:]:
            add_hypothesis(
                "SCHEMA-SRC-HARDCODED-RATING",
                "error",
                "Posible calificación aggregateRating hardcodeada en plantilla",
                "Inventar o fijar valoraciones estáticas en el código infringe las directrices de calidad de datos estructurados.",
                {"file": path},
                "Eliminar calificaciones estáticas y emitir aggregateRating solo desde datos reales verificados.",
                [path],
            )
        if re.search(r'"availability"\s*:\s*"https?://schema\.org/InStock"', content) and "available" not in lower and "outofstock" not in lower:
            add_hypothesis(
                "SCHEMA-SRC-HARDCODED-INSTOCK",
                "warning",
                "Disponibilidad `InStock` fija en plantilla sin comprobar inventario real (`available`)",
                "Puede declarar en stock productos agotados, causando discrepancias con el contenido visible y Merchant Center.",
                {"file": path},
                "Condicionar availability al estado real de la variante o producto (`product.selected_or_first_available_variant.available`).",
                [path],
            )
        if re.search(r'"(?:name|description)"\s*:\s*"\{\{(?![^}]*\|\s*json\b)[^}]+\}\}"', content):
            add_hypothesis(
                "SCHEMA-SRC-UNESCAPED-LIQUID-JSON",
                "warning",
                "Interpolación Liquid dentro de comillas JSON sin filtro `| json`",
                "Si el título o descripción contiene comillas o saltos de línea, romperá la sintaxis del bloque JSON-LD.",
                {"file": path},
                "Usar el filtro `| json` de Liquid (sin comillas externas duplicadas) o `structured_data`.",
                [path],
            )

    # 6. Verificaciones externas obligatorias
    if rendered_html is None and not snap.get("json_ld") and not snap.get("microdata"):
        add_external(
            "SCHEMA-EXT-RENDERED-DOM-REQUIRED",
            "Inspección de datos estructurados en el DOM renderizado con JavaScript",
            "No se observaron bloques JSON-LD en el HTML estático; no se afirma que falte Schema hasta verificar el DOM renderizado.",
            "Captura de navegador renderizada (--rendered / qa_browser.mjs)",
            {"url": url, "static_json_ld_count": 0},
        )
    add_external(
        "SCHEMA-EXT-GOOGLE-RRT-AND-GSC",
        "Confirmación en Google Rich Results Test y reportes de Search Console",
        "La validez local de sintaxis, vocabulario y consistencia no garantiza la aparición de resultados enriquecidos en Google.",
        "Google Rich Results Test / Search Console Enhancements",
        {"url": url},
    )

    # 7. Propuesta segura de corrección JSON-LD (cuando hay facts autorizados + propose_target, o reparación de coma final)
    proposal = None
    if propose_target and facts_doc is not None:
        # Si el único error de sintaxis es una coma final, reparamos el snapshot temporalmente para poder proponer actualización segura
        clean_snap = snap
        if any(b["error"] and b["error"].get("hint") == "trailing_comma" for b in snap.get("json_ld", [])):
            repaired_blocks = []
            for b in snap["json_ld"]:
                if b["error"] and b["error"].get("hint") == "trailing_comma":
                    rep = repair_trailing_json(b["raw"])
                    repaired_blocks.append(f'<script type="application/ld+json">{rep["json"]}</script>')
                elif not b["error"]:
                    repaired_blocks.append(f'<script type="application/ld+json">{b["raw"]}</script>')
            clean_snap = extract("".join(repaired_blocks), url)
        # Resolver modo automáticamente si la entidad ya existe
        target_exists = any(propose_target in e["types"] and not e["ref_only"] for e in build_graph(clean_snap)["raw_entities"])
        effective_mode = "update" if target_exists and propose_mode == "missing" else propose_mode
        # Si hay duplicados conflictivos en el HTML actual, construir propuesta limpia sobre un snapshot de referencia para reemplazar la fuente
        if build_graph(clean_snap)["conflicts"]:
            clean_snap = extract("", url)
            effective_mode = "missing"
        proposal = generate(project, facts_doc, propose_target, snapshot=clean_snap, mode=effective_mode, fixture=fixture)
    elif any(b["error"] and b["error"].get("hint") == "trailing_comma" for b in snap.get("json_ld", [])):
        for b in snap["json_ld"]:
            if b["error"] and b["error"].get("hint") == "trailing_comma":
                proposal = {
                    "kind": "schema-syntax-repair-proposal",
                    "action": "repair_trailing_comma_at_source",
                    "block": b["index"],
                    **repair_trailing_json(b["raw"]),
                }
                break

    validation_dimensions = {
        "syntactic_validity": val_report["states"]["syntax_valid"],
        "semantic_validity": val_report["states"]["semantic_valid_for_checked_rules"],
        "visible_and_fact_consistency": val_report["states"]["consistency"],
        "documented_google_eligibility": {
            "features": val_report["states"]["google_requirements_met_by_feature"],
            "retired_google_features_present": retired_present,
            "note": "Validez en Schema.org no equivale a elegibilidad para rich results en Google.",
        },
        "search_console_real_result": "requires_external_verification",
    }

    return redact({
        "kind": "schema-skill-audit",
        "skill": "schema",
        "reused_engines": ["ipanema-seo-expert", "seo-audit"],
        "project": project.id,
        "url": url,
        "page_type": page_type,
        "framework": detected_fw,
        "inventory": {
            "json_ld_blocks": blocks_inventory,
            "microdata_count": len(snap.get("microdata", [])),
            "rdfa_entities_count": len(snap.get("rdfa_entities", [])),
            "detected_types": graph["types"],
            "duplicates": graph["duplicates"],
            "conflicts": graph["conflicts"],
            "source_architecture": source_architecture,
        },
        "validation_dimensions": validation_dimensions,
        "json_parse_alone_sufficient": False,
        "rich_results_promised": False,
        "untrusted_page_data_ignored": True,
        "verified_by_tool": verified_by_tool,
        "code_hypothesis": code_hypothesis,
        "requires_external_verification": requires_external_verification,
        "proposal": proposal,
        "counts": {
            "verified_by_tool": len(verified_by_tool),
            "code_hypothesis": len(code_hypothesis),
            "requires_external_verification": len(requires_external_verification),
            "errors": sum(1 for i in verified_by_tool if i["severity"] == "error"),
            "warnings": sum(1 for i in verified_by_tool if i["severity"] == "warning"),
        },
        "limitations": [
            "Que un bloque sea JSON válido no demuestra validez semántica ni coincidencia con el contenido visible.",
            "No se eliminan ni sobrescriben automáticamente bloques generados por aplicaciones externas.",
            "No se prometen resultados enriquecidos ni mejoras de posicionamiento.",
        ],
    })
