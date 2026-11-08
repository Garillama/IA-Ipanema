#!/usr/bin/env python3
"""Busca componentes existentes sin abrir ni escribir el tema."""
import argparse
import json
from pathlib import Path
import unicodedata

def normal(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s).lower()) if not unicodedata.combining(c))

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('query')
parser.add_argument('--limit', type=int, default=15)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
components = json.loads((root/'ipanema-discovery/13-evidence/measurements/source-baseline/components.json').read_text())
tokens = normal(args.query).split()
aliases = {'producto':'product','productos':'product','tarjeta':'product-item/item.tpl','tarjetas':'product-item/item.tpl','card':'product-item/item.tpl','pdp':'sections/main-product.tpl','carrito':'cart','imagen':'image','imagenes':'image','carrusel':'slider','menu':'navigation','busqueda':'search','pie':'footer','encabezado':'header','faq':'faq'}
terms = set(tokens + [aliases[t] for t in tokens if t in aliases])
hits=[]
for component in components:
    identity=normal(component['path']+' '+str(component['name']))
    context=normal(' '.join(component['js_hooks']+component['setting_refs']))
    score=sum(20 if term.endswith('.tpl') else 5 for term in terms if term in identity)+sum(1 for term in terms if term in context)
    if score:
        hits.append((score,component))
for score,c in sorted(hits,key=lambda x:(-x[0],x[1]['path']))[:args.limit]:
    sheet='ipanema-discovery/02-native-components/specifications/'+c['path'][:-4].replace('/','--')+'.md'
    print(f"{c['path']} | {c['name']} | {sheet}")
if not hits:
    print('Sin coincidencias en el inventario fechado. Buscar en el origen con rg antes de concluir que no existe.')
