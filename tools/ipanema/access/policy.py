"""Permisos locales emitidos por el operador; denegación predeterminada y cuota persistente."""
from __future__ import annotations

from contextlib import contextmanager
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import uuid

from ..core import IpanemaError, now, read_json, write_json

AGENTS = ('claude', 'codex', 'commandcode')
CAPABILITIES = {
    'devtools.read': ('devtools_open', 'devtools_snapshot', 'devtools_network', 'devtools_console'),
    'devtools.performance': ('devtools_trace', 'devtools_insight'),
    'gsc.read': ('gsc_search_analytics', 'gsc_inspect_url', 'gsc_sitemaps'),
    'analytics.read': ('analytics_run_report',),
    'merchant.read': ('merchant_products',),
}


def fingerprint(project):
    data = {k: project.data.get(k) for k in ('public_url', 'qa_base_url', 'google', 'browser')}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


class Policy:
    def __init__(self, project):
        self.project = project
        self.root = project.root / '.local/access'
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.root.chmod(0o700)

    @contextmanager
    def locked(self):
        with (self.root / 'controller.lock').open('a') as lock:
            os.chmod(lock.name, 0o600)
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield

    def path(self, grant_id):
        if not re.fullmatch('[a-f0-9]{32}', str(grant_id)):
            raise IpanemaError('Identificador de permiso inválido.')
        return self.root / (grant_id + '.json')

    def save(self, grant):
        path = self.path(grant['id'])
        write_json(path, grant, overwrite=True)
        path.chmod(0o600)

    def issue(self, agent, task, capabilities, *, minutes=60, max_calls=30,
              allow_network=False, allow_account_read=False, browser_profile='security'):
        if agent not in AGENTS or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}', task):
            raise IpanemaError('Agente o identificador de tarea inválido.')
        if not capabilities or set(capabilities) - set(CAPABILITIES):
            raise IpanemaError('Capacidad desconocida.')
        if browser_profile not in ('security', 'audit'):
            raise IpanemaError('Perfil de navegador desconocido.')
        if not 1 <= minutes <= 480 or not 1 <= max_calls <= 50:
            raise IpanemaError('Permiso: 1–480 minutos y 1–50 llamadas.')
        accounts = any(c in capabilities for c in ('gsc.read', 'analytics.read', 'merchant.read'))
        if not allow_network or accounts and not allow_account_read:
            raise IpanemaError('Requiere --allow-network y, para cuentas, --allow-account-read.')
        grant = {'id': uuid.uuid4().hex, 'project': self.project.id, 'agent': agent, 'task': task,
                 'capabilities': sorted(set(capabilities)), 'created_at': now(),
                 'expires_at': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=minutes)).isoformat(),
                 'max_calls': max_calls, 'calls': 0, 'revoked': False,
                 'browser_profile': browser_profile,
                 'configuration_sha256': fingerprint(self.project)}
        with self.locked():
            self.save(grant)
        return grant

    def load(self, grant_id, *, active=True):
        path = self.path(grant_id)
        if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o077:
            raise IpanemaError('Permiso ausente o con permisos de archivo inseguros.')
        grant = read_json(path)
        if grant.get('id') != grant_id or grant.get('project') != self.project.id:
            raise IpanemaError('Permiso de otro proyecto.')
        if active and (grant.get('revoked') or grant.get('expires_at', '') <= now()
                       or grant.get('configuration_sha256') != fingerprint(self.project)):
            raise IpanemaError('Permiso revocado, caducado o configuración modificada.')
        return grant

    def revoke(self, grant_id):
        with self.locked():
            grant = self.load(grant_id, active=False)
            grant['revoked'] = True
            self.save(grant)

    def tools(self, grant):
        return {name for cap in grant['capabilities'] for name in CAPABILITIES[cap]}

    def stop_path(self, provider):
        if provider not in ('gsc', 'analytics', 'merchant', 'devtools'):
            raise IpanemaError('Proveedor inválido.')
        return self.root / (self.project.id + '-' + provider + '-stop.json')

    def consume(self, grant_id, tool):
        # Caller holds lock across permission check, provider call and stop recording.
        grant = self.load(grant_id)
        if tool not in self.tools(grant) or grant['calls'] >= grant['max_calls']:
            raise IpanemaError('Operación no autorizada o cuota de tarea agotada.')
        provider = tool.split('_')[0]
        if self.stop_path(provider).exists():
            raise IpanemaError('Proveedor detenido para este proyecto; requiere revisión del operador.')
        grant['calls'] += 1
        self.save(grant)
        return grant

    def stop(self, provider, reason):
        path = self.stop_path(provider)
        write_json(path, {'project': self.project.id, 'provider': provider, 'at': now(), 'reason': reason}, overwrite=True)
        path.chmod(0o600)
