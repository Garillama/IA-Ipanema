"""Comprobaciones semánticas acotadas al vocabulario oficial fechado y almacenado."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

VOCAB = json.loads(Path(__file__).with_name('vocabulary.json').read_text(encoding='utf-8'))


def ancestors(kind):
    result=set();pending=[kind]
    while pending:
        k=pending.pop()
        if k in result:continue
        result.add(k);pending.extend(VOCAB['types'].get(k,[]))
    return result


def amount(value):
    if isinstance(value,bool) or value is None:return None
    if not re.fullmatch(r'\d+(?:\.\d+)?',str(value)):return None
    try:
        number=Decimal(str(value))
        return number if number.is_finite() else None
    except InvalidOperation:return None


def offer_price(offer):
    if offer.get('price') is not None:return offer.get('price'),offer.get('priceCurrency')
    specs=offer.get('priceSpecification',[])
    specs=specs if isinstance(specs,list) else [specs]
    # No elegir un precio tachado o un miembro suscriptor como si fuera el precio activo.
    active=[s for s in specs if isinstance(s,dict) and not s.get('priceType') and not s.get('validForMemberTier')]
    return (active[0].get('price'),active[0].get('priceCurrency')) if len(active)==1 else (None,None)


def valid_date(value):
    try:
        datetime.fromisoformat(str(value).replace('Z','+00:00'));return True
    except (TypeError,ValueError):return False


def http_url(value):
    if not isinstance(value,str):return False
    u=urlsplit(value)
    return u.scheme in ('http','https') and bool(u.hostname) and not u.username and not u.password and not re.search(r'\s',value)


def check_properties(graph):
    problems=[];unchecked=set()
    for ent in graph['raw_entities']:
        if ent['ref_only']:continue
        types=ent['types'];known=set().union(*(ancestors(t) for t in types)) if types else set()
        obj=ent['obj']
        if '@id' in obj and not isinstance(obj['@id'],str):
            problems.append(('error',ent['key'],'@id','@id debe ser texto, no un objeto/lista.'))
        for prop,value in obj.items():
            if prop.startswith('@'):continue
            rule=VOCAB['properties'].get(prop)
            if not rule:unchecked.add(prop);continue
            if known and rule['domain'] and not known.intersection(rule['domain']):
                problems.append(('warning',ent['key'],prop,'Propiedad fuera de los dominios comprobados de esos tipos.'))
            values=value if isinstance(value,list) else [value]
            ranges=set(rule['range'])
            for val in values:
                if isinstance(val,dict):
                    child_types=val.get('@type',[])
                    child_types=child_types if isinstance(child_types,list) else [child_types]
                    child_anc=set().union(*(ancestors(str(t).rsplit('/',1)[-1]) for t in child_types)) if child_types else set()
                    if child_anc and ranges and not child_anc.intersection(ranges):
                        problems.append(('warning',ent['key'],prop,'El tipo del objeto no coincide con los rangos comprobados.'))
                elif isinstance(val,str) and ranges and ranges <= {'Number','Integer','Float'} and amount(val) is None:
                    problems.append(('error',ent['key'],prop,'Valor numérico no interpretable sin ambigüedad.'))
                elif prop in ('datePublished','dateModified','uploadDate','priceValidUntil','validFrom','validThrough') and not valid_date(val):
                    problems.append(('warning',ent['key'],prop,'Fecha no válida en ISO 8601; no reemplazarla por la fecha de auditoría.'))
                elif isinstance(val,str) and ranges and ranges <= {'Person','Organization','Brand'}:
                    problems.append(('warning',ent['key'],prop,'Se espera una entidad del vocabulario, no texto sin tipo.'))
    return problems,sorted(unchecked)
