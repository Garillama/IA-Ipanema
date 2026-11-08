"""Grafo de entidades a partir de JSON-LD y microdata de un snapshot.

Representa solo las entidades que existen en la página (no completa nada). Detecta referencias por `@id`,
entidades duplicadas entre scripts y valores contradictorios de una misma entidad.
"""
from __future__ import annotations

from collections import defaultdict
import json
from urllib.parse import urljoin

SINGLETON_TYPES = {"Organization", "OnlineStore", "WebSite", "WebPage", "CollectionPage", "Blog", "BreadcrumbList"}
COMPARE = ("name", "url", "description", "sku", "headline", "datePublished", "dateModified")
OFFER_COMPARE = ("price", "priceCurrency", "availability", "url")


def as_list(value):
    return value if isinstance(value, list) else [] if value is None else [value]


def types_of(obj: dict):
    return [str(t).rsplit("/", 1)[-1] for t in as_list(obj.get("@type"))]


def _scalar(value):
    return value if isinstance(value, (str, int, float, bool)) else None


def _walk(value, path, parent, prop, block, component, out):
    if isinstance(value, list):
        for i, item in enumerate(value):
            _walk(item, f"{path}[{i}]", parent, prop, block, component, out)
        return
    if not isinstance(value, dict):
        return
    if "@graph" in value:
        _walk(value["@graph"], path + ".@graph", parent, prop, block, component, out)
    t = types_of(value)
    only_ref = set(value) <= {"@id"} and "@id" in value
    if t or '@id' in value:
        ident=value.get('@id') if isinstance(value.get('@id'),str) else None
        key = ident or f"{block}:{path}"
        out.append({"key": key, "id": ident, "types": t, "obj": value, "source": "jsonld", "block": block,
                    "component": component, "path": path, "parent": parent, "parent_prop": prop, "ref_only": only_ref,
                    "nested": parent is not None})
        parent = out[-1]["key"] if not only_ref else parent
    for k, v in value.items():
        if k in ("@context", "@graph"):
            continue
        _walk(v, f"{path}.{k}", parent, k, block, component, out)


def entities_from_snapshot(snap: dict):
    out = []
    for block in snap["json_ld"]:
        if block["data"] is not None:
            _walk(block["data"], "$", None, None, block["index"], block.get("component"), out)
    for i, item in enumerate(snap.get("microdata", [])):
        if 'obj' in item:
            if item.get('depth',0):continue
            start=len(out);_walk(item['obj'],'$',None,None,f'md{i}',None,out)
            for ent in out[start:]:ent['source']='microdata'
            continue
        obj = {"@type": [t.rsplit('/',1)[-1] for t in as_list(item['type'])] if item['type'] else None}
        for p in item["props"]:
            obj.setdefault(p["name"], p["value"])
        if item["id"]:
            obj["@id"] = item["id"]
        out.append({"key": item["id"] or f"microdata:{i}", "id": item["id"] or None, "types": types_of(obj), "obj": obj,
                    "source": "microdata", "block": f"md{i}", "component": None, "path": "$", "parent": None,
                    "parent_prop": None, "ref_only": False, "nested": item["depth"] > 0})
    for i,obj in enumerate(snap.get('rdfa_entities',[])):
        start=len(out);_walk(obj,'$',None,None,f'rdfa{i}',None,out)
        for ent in out[start:]:ent['source']='rdfa'
    base=snap.get('url','')
    replacements={e['key']:urljoin(base,e['id']) for e in out if e['id'] and base}
    for ent in out:
        if ent['id']:
            ent['id']=urljoin(base,ent['id']) if base else ent['id']
        ent['key']=replacements.get(ent['key'],ent['key'])
        ent['parent']=replacements.get(ent['parent'],ent['parent'])
    return out


def identity(ent: dict):
    obj, t = ent["obj"], ent["types"]
    if ent["id"]:
        return ("id", ent["id"])
    primary = t[0] if t else "?"
    if primary in ("Product", "ProductGroup"):
        offers = as_list(obj.get("offers"))
        offer_url = offers[0].get("url") if offers and isinstance(offers[0], dict) else None
        main = obj.get("mainEntityOfPage")
        main_id = main.get("@id") if isinstance(main, dict) else main
        ident=obj.get('sku') or obj.get('productID') or obj.get('url') or offer_url or main_id or ent['key']
        return ("product", ident if isinstance(ident,(str,int,float)) else ent['key'])
    if primary == "ListItem":
        return None
    return (primary, obj.get('url') if isinstance(obj.get('url'),str) else ent['key'])


def _flat(ent):
    obj = ent["obj"]
    flat = {k: _scalar(obj.get(k)) for k in COMPARE if _scalar(obj.get(k)) is not None}
    if "Product" in ent["types"] or "ProductGroup" in ent["types"]:
        for offer in as_list(obj.get("offers")):
            if isinstance(offer, dict):
                for k in OFFER_COMPARE:
                    if _scalar(offer.get(k)) is not None:
                        flat["offers." + k] = str(offer[k]).rsplit("/", 1)[-1] if k == "availability" else offer[k]
                break
    return flat


def build_graph(snap: dict):
    ents = entities_from_snapshot(snap)
    by_id = {}
    for e in ents:
        if e['id'] and not e['ref_only']:
            by_id.setdefault(e['id'],[]).append(e)
    edges, dangling = [], []
    for e in ents:
        if e["ref_only"] and e["parent"] is not None:
            target = by_id.get(e["id"])
            edges.append({"from": e["parent"], "prop": e["parent_prop"], "to": e["id"], "resolved": target is not None})
            if target is None:
                dangling.append({"id": e["id"], "from": e["parent"], "prop": e["parent_prop"], "block": e["block"]})
        elif e["parent"] is not None:
            edges.append({"from": e["parent"], "prop": e["parent_prop"], "to": e["key"], "resolved": True, "inline": True})
    groups = defaultdict(list)
    for e in ents:
        if e["ref_only"]:
            continue
        ident = identity(e)
        if ident is not None and any(x is not None for x in ident[1:]):
            groups[ident].append(e)
    duplicates, conflicts = [], []
    for ident, members in groups.items():
        top = [m for m in members]
        blocks = {m["block"] for m in top}
        fingerprints=[json.dumps({k:v for k,v in m['obj'].items() if k!='@context'},sort_keys=True,ensure_ascii=False) for m in top]
        if len(top) > 1:
            exact=len(set(fingerprints))<len(fingerprints)
            # A single offer on two definitions of the same product is comparable.
            # Multiple offers/variants are not flattened into a fictitious price.
            flats=[]
            for m in top:
                flat={k:_scalar(m['obj'].get(k)) for k in (*COMPARE,*OFFER_COMPARE) if _scalar(m['obj'].get(k)) is not None}
                offers=as_list(m['obj'].get('offers'))
                if 'Product' in m['types'] and len(offers)==1 and isinstance(offers[0],dict):
                    flat.update({'offers.'+k:_scalar(offers[0].get(k)) for k in OFFER_COMPARE if _scalar(offers[0].get(k)) is not None})
                flats.append(flat)
            local_conflicts=[]
            for k in sorted({k for f in flats for k in f}):
                vals = {str(f[k]) for f in flats if k in f}
                if len(vals) > 1:
                    local_conflicts.append({"identity": list(ident), "property": k, "values": sorted(vals)})
            conflicts.extend(local_conflicts)
            if exact or ident[0]!='id' or local_conflicts:
                duplicates.append({"identity":list(ident),"types":top[0]['types'],"count":len(top),
                                   "kind":"exact_repetition" if exact else "conflicting_definition" if local_conflicts else "identity_candidate",
                                   "locations":[{"block":m['block'],"component":m['component'],"path":m['path'],"source":m['source']} for m in top]})
    singleton_multi = []
    for t in SINGLETON_TYPES:
        top = [e for e in ents if t in e["types"] and not e["nested"] and not e["ref_only"]]
        distinct = {identity(e) for e in top}
        if len(top) > 1:
            singleton_multi.append({"type": t, "count": len(top), "distinct_identities": len(distinct),
                                    "blocks": sorted({str(e["block"]) for e in top})})
    org_nested = [e for e in ents if "Organization" in e["types"] and e["nested"] and not e["id"] and not e["ref_only"]]
    org_top = [e for e in ents if ("Organization" in e["types"] or "OnlineStore" in e["types"]) and not e["nested"] and not e["ref_only"]]
    incompatible=[]
    for key,members in by_id.items():
        types={t for e in members for t in e['types']}
        if 'Product' in types and types.intersection({'WebPage','Organization','Person'}):incompatible.append({'id':key,'types':sorted(types)})
    return {'base_url':snap.get('url',''),"entities": [{**{k: e[k] for k in ("key", "id", "types", "source", "block", "component", "path", "parent", "parent_prop", "nested", "ref_only")},'properties':list(e['obj'])} for e in ents],
            "raw_entities": ents, "edges": edges, "dangling_references": dangling, "duplicates": duplicates, "conflicts": conflicts,
            "repeated_singletons": singleton_multi,
            "identity_split": {"global_organizations": len(org_top), "nested_unreferenced_organizations": len(org_nested),
                               "paths": [e["path"] for e in org_nested]},
            "incompatible_id_types":incompatible,
            "types": sorted({t for e in ents for t in e["types"]})}


def resolve_object(value,graph):
    """Unifica declaraciones complementarias por @id sin elegir valores contradictorios."""
    if not isinstance(value,dict):return value
    ident=value.get('@id')
    if not ident:return value
    ident=urljoin(graph.get('base_url',''),ident) if isinstance(ident,str) else None
    if not ident:return value
    matches=[e['obj'] for e in graph['raw_entities'] if not e['ref_only'] and (e['id']==ident or e['obj'].get('@id')==ident)]
    merged={}
    for obj in matches:
        for key,val in obj.items():
            if key not in merged:merged[key]=val
    return {**merged,**value}
