#!/usr/bin/env python3
"""Entrada MCP stdio compartida por Claude, Codex y CommandCode."""
import argparse
import sys

from ipanema.core import IpanemaError, Project
from ipanema.access.gateway import Gateway, serve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--grant', required=True)
    args = parser.parse_args()
    try:
        gateway = Gateway(Project(project_id=args.project), args.grant)
        serve(gateway, sys.stdin, sys.stdout)
        return 0
    except (IpanemaError, OSError, ValueError):
        print('Acceso no iniciado: permiso o configuración no disponible.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
