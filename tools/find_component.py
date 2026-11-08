#!/usr/bin/env python3
"""Busca componentes existentes, consumidores y settings en el proyecto activo."""
import argparse
import json
import sys
from ipanema.core import Project, IpanemaError
from ipanema.knowledge import Knowledge


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--limit', type=int, default=15)
    parser.add_argument('--project')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        if not 1 <= args.limit <= 50:
            raise IpanemaError('limit debe estar entre 1 y 50.')
        hits = Knowledge(Project(project_id=args.project)).search(args.query, args.limit)
        if args.json:
            print(json.dumps(hits, ensure_ascii=False, indent=2))
        else:
            for hit in hits:
                print(f'{hit["path"]} | {hit["name"]} | {hit["sheet"]}')
            if not hits:
                print('Sin coincidencias en el inventario fechado. Buscar en el origen antes de concluir que no existe.')
        return 0
    except IpanemaError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
