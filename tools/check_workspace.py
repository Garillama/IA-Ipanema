#!/usr/bin/env python3
"""Compatibilidad V1: valida el repositorio y el tema activo si está disponible."""
import argparse
import json
import sys
from ipanema.core import Project, IpanemaError
from ipanema.validation import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project')
    parser.add_argument('--strict-source', action='store_true')
    args = parser.parse_args()
    try:
        result = validate(Project(project_id=args.project), strict_source=args.strict_source)
    except IpanemaError as exc:
        result = {'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get('errors') else 0


if __name__ == '__main__':
    sys.exit(main())
