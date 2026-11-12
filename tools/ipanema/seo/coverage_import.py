"""Importación offline de informes exportados; no existe inventario API exhaustivo."""
import csv
from datetime import datetime
import hashlib
import io

from ..core import IpanemaError, now
from .adapters import authorize_url, prepare

FIELDS = {'url', 'coverage_state', 'last_crawl', 'google_canonical', 'user_canonical'}


def _scope(project, site_url, observed_at):
    prepare(project, 'gsc', 'sitemaps', {'siteUrl': site_url})
    try:
        datetime.fromisoformat(observed_at.replace('Z', '+00:00'))
    except (ValueError, TypeError, AttributeError):
        raise IpanemaError('Fecha explícita de la exportación requerida; no usar la fecha del análisis como último rastreo.') from None


def import_csv(project, raw, *, site_url, observed_at, mapping, max_rows=10000):
    _scope(project, site_url, observed_at)
    if not isinstance(mapping, dict) or 'url' not in mapping or set(mapping) - FIELDS or not all(isinstance(v, str) for v in mapping.values()):
        raise IpanemaError('Mapping requiere url y solo campos de cobertura declarados.')
    if type(max_rows) is not int or not 1 <= max_rows <= 50000 or len(raw.encode()) > 10_000_000:
        raise IpanemaError('Presupuesto de exportación inválido o excedido.')
    reader = csv.DictReader(io.StringIO(raw.lstrip('\ufeff')))
    if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)) or not set(mapping.values()) <= set(reader.fieldnames):
        raise IpanemaError('Columnas CSV ausentes o ambiguas; se exige mapping explícito.')
    rows = []
    for index, row in enumerate(reader):
        if index >= max_rows:
            raise IpanemaError('Exportación supera el máximo de filas; no se trunca silenciosamente.')
        values = {key: row.get(column) or None for key, column in mapping.items()}
        authorize_url(project, values.get('url') or '')
        for key in ('google_canonical', 'user_canonical'):
            if values.get(key):
                # Un canonical de Google puede ser externo. Se conserva como dato,
                # sin seguirlo ni atribuirle permisos sobre el otro dominio.
                from ..core import safe_url
                safe_url(values[key], local=False)
        rows.append(values)
    return {'kind': 'gsc-coverage-export-v4', 'project': project.id, 'site_url': site_url,
            'observed_at': observed_at, 'at': now(), 'rows': rows,
            'source_sha256': hashlib.sha256(raw.encode()).hexdigest(), 'mapping': mapping,
            'live_connection_tested': False, 'exhaustive_index_inventory': False,
            'limitations': ['Archivo aportado con procedencia; no prueba consulta API actual.',
                            'Estado y último rastreo son declaraciones del export, no fechas inventadas.',
                            'Fechas por fila se conservan sin reinterpretar formatos locales ambiguos.']}


def validate_export(project, document):
    if document.get('kind') != 'gsc-coverage-export-v4' or document.get('project') != project.id:
        raise IpanemaError('Exportación de cobertura de otro proyecto o formato.')
    _scope(project, document.get('site_url'), document.get('observed_at'))
    rows = document.get('rows')
    if not isinstance(rows, list) or len(rows) > 50000:
        raise IpanemaError('Filas de cobertura inválidas.')
    for row in rows:
        if not isinstance(row, dict) or set(row) - FIELDS:
            raise IpanemaError('Campos de cobertura inválidos.')
        authorize_url(project, row.get('url', ''))
    return document
