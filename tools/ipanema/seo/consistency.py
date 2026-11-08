"""Nivel D: coherencia entre datos estructurados, HTML visible y fuentes comerciales proporcionadas.

`facts` es opcional y debe venir de una fuente autorizada (catálogo/API/fixture), nunca deducirse del schema.
Sin una fuente, lo no verificable se informa como `not_verified`, no como error.
"""
from __future__ import annotations

import re
from urllib.parse import urlsplit

from .schema_graph import as_list
from .schema_graph import resolve_object
from .vocabulary import amount, offer_price

SUPPORTED_FACTS = ("canonical", "name", "price", "currency", "availability", "image", "sku", "has_variants",
                   "reviews_source", "policies_source", "store_currency")


def norm(text):
    return re.sub(r"\W+", " ", str(text or "").casefold()).strip()


def _same_url(a, b):
    if not a or not b:
        return True
    pa, pb = urlsplit(str(a)), urlsplit(str(b))
    return (pa.scheme,pa.netloc.lower(),pa.path.rstrip('/'),pa.query) == (pb.scheme,pb.netloc.lower(),pb.path.rstrip('/'),pb.query)


def _D(rule, severity, message, **kw):
    from .schema_validator import F
    return F(rule, "D", severity, message, **kw)


def check_consistency(snap, graph, page_type, facts):
    out = []
    products = [e for e in graph["raw_entities"] if "Product" in e["types"] and not e["ref_only"]]
    canonical = (snap.get("canonical") or [None])[0]
    if len(snap.get("canonical") or []) > 1 and len(set(snap["canonical"])) > 1:
        out.append(_D("D001", "error", "Varias URL canónicas contradictorias.", evidence=snap["canonical"]))
    expected_canonical = facts.get("canonical") or canonical
    h1s = [h["text"] for h in snap["headings"] if h["level"] == 1]
    meta = snap["meta"]
    meta_price = (meta.get("product:price:amount") or meta.get("og:price:amount") or [None])[0]
    meta_cur = (meta.get("product:price:currency") or meta.get("og:price:currency") or [None])[0]
    base_facts=facts
    for p in products:
        facts=base_facts
        if page_type != "product" and not facts.get("force_product_checks"):
            continue
        o, label = resolve_object(p['obj'],graph), f"Product@{p['component'] or p['block']}"
        is_variant=p.get('parent_prop')=='hasVariant' or bool(o.get('isVariantOf'))
        if is_variant:
            variants=base_facts.get('variants',[])
            match=next((v for v in variants if v.get('sku') and str(v['sku'])==str(o.get('sku')) or v.get('url') and o.get('url') and _same_url(v['url'],o.get('url'))),None)
            facts={k:v for k,v in base_facts.items() if k in ('store_currency','reviews_source','policies_source')}
            if match:facts.update(match)
        main = o.get("mainEntityOfPage")
        main_id = main.get("@id") if isinstance(main, dict) else main
        # An entity @id is not a canonical URL. Variant selection URLs may differ
        # from the single-page group's canonical; compare those only to own facts.
        checks = [("mainEntityOfPage", main_id, expected_canonical),
                  ("url", o.get("url"), facts.get('url') if is_variant else expected_canonical)]
        for key, val, expected_url in checks:
            if val and expected_url and not _same_url(val, expected_url):
                out.append(_D("D010", "error", f"`{key}` no coincide con la canonical de la página.", entity=label, evidence={"value": val, "canonical": expected_canonical}))
        for of in [x for x in as_list(o.get("offers")) if isinstance(x, dict)]:
            of=resolve_object(of,graph)
            if of.get("url") and expected_canonical and not _same_url(of["url"], expected_canonical):
                out.append(_D("D011", "warning", "Offer.url difiere de la canonical (¿variante con URL propia?).", entity=label, evidence={"offer_url": of["url"], "canonical": expected_canonical}))
            want_price = facts.get("price") if facts.get("price") is not None else None if is_variant else meta_price
            actual_price,actual_currency=offer_price(of)
            if want_price is not None and actual_price is not None:
                try:
                    if amount(actual_price) is None or amount(want_price) is None:
                        raise ValueError('Precio ambiguo')
                    if amount(actual_price) != amount(want_price):
                        out.append(_D("D020", "error", "Precio del schema distinto del precio de la fuente.", entity=label,
                                      evidence={"schema": actual_price, "source": want_price, "source_kind": "facts" if facts.get("price") is not None else "meta"}))
                except ValueError:
                    out.append(_D("D021", "warning", "No se pudo comparar el precio sin ambigüedad.", entity=label, evidence={"schema": actual_price, "source": want_price}))
            else:
                out.append(_D("D022", "optional", "Precio no verificado: no se proporcionó fuente comercial ni meta de precio.", entity=label))
            want_cur = facts.get("currency") or facts.get("store_currency") or meta_cur
            if want_cur and actual_currency and str(actual_currency).upper() != str(want_cur).upper():
                out.append(_D("D030", "error", "Moneda del schema distinta de la moneda de la tienda/fuente.", entity=label, evidence={"schema": actual_currency, "source": want_cur}))
            if facts.get("availability") and of.get("availability"):
                if str(of["availability"]).rsplit("/", 1)[-1] != str(facts["availability"]).rsplit("/", 1)[-1]:
                    out.append(_D("D040", "error", "Disponibilidad del schema distinta de la fuente.", entity=label, evidence={"schema": of["availability"], "source": facts["availability"]}))
            elif not of.get("availability"):
                out.append(_D("D041", "optional", "Sin availability: no se asume InStock por existir un botón de compra ni por stock ilimitado.", entity=label))
            if of.get("price") not in (None, "") and "inventoryLevel" in of:
                out.append(_D("D042", "optional", "inventoryLevel expone existencias numéricas; confirmar que es información que la tienda quiere publicar.", entity=label))
        if not is_variant and h1s and o.get("name") and norm(o["name"]) not in norm(h1s[0]) and norm(h1s[0]) not in norm(o["name"]):
            out.append(_D("D050", "warning", "Product.name no coincide con el H1 visible.", entity=label, evidence={"name": o["name"], "h1": h1s[0]}))
        if facts.get("name") and o.get("name") and norm(facts["name"]) != norm(o["name"]):
            out.append(_D("D051", "error", "Product.name distinto del nombre del catálogo.", entity=label, evidence={"schema": o["name"], "source": facts["name"]}))
        if facts.get("sku") and o.get("sku") and str(facts["sku"]) != str(o["sku"]):
            out.append(_D("D060", "error", "SKU del schema distinto del catálogo.", entity=label, evidence={"schema": o["sku"], "source": facts["sku"]}))
        imgs = [i if isinstance(i, str) else (i or {}).get("url") for i in as_list(o.get("image"))]
        visible = {i["src"] for i in snap["images"]} | set(meta.get("og:image", []))
        stems = {re.sub(r"-\d+x\d*|\?.*$", "", v.rsplit("/", 1)[-1]) for v in visible if v}
        if imgs and visible and not any(re.sub(r"-\d+x\d*|\?.*$", "", str(i).rsplit("/", 1)[-1]) in stems for i in imgs if i):
            out.append(_D("D070", "warning", "La imagen del schema no aparece (por nombre de archivo) entre las imágenes/og:image de la página.", entity=label, evidence=imgs[:2]))
        for key in ("review", "aggregateRating"):
            if o.get(key) is not None and not facts.get("reviews_source"):
                out.append(_D("D080", "warning", f"`{key}` presente sin una fuente verificable de reseñas reales indicada en `facts.reviews_source`. No convertir testimonios de la tienda en reseñas de producto.", entity=label))
        for of in [x for x in as_list(o.get("offers")) if isinstance(x, dict)]:
            for key in ("shippingDetails", "hasMerchantReturnPolicy"):
                if of.get(key) is not None and not facts.get("policies_source"):
                    out.append(_D("D090", "warning", f"`{key}` presente sin una fuente de políticas reales (`facts.policies_source`). No inventar envíos ni devoluciones; no asumir envío gratis.", entity=label))
    if page_type == "product" and len(h1s) == 0:
        out.append(_D("D100", "warning", "Página de producto sin H1 visible para contrastar con el schema."))
    return out
