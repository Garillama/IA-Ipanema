"""Access tokens de corta vida ligados a proyecto/propiedad, fuera de Git y del worker."""
import datetime as dt
import json
import os
from pathlib import Path
import tempfile

from ..core import IpanemaError
from ..seo.adapters import SCOPES


def credential_path(project):
    return project.root / '.local/access/credentials' / (project.id + '-gsc.json')


def store_token(project, token, expires_in):
    if not isinstance(token, str) or not token or type(expires_in) is not int or not 1 <= expires_in <= 86400:
        raise IpanemaError('Credencial OAuth sin expiración válida.')
    path = credential_path(project)
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != project.root):
        raise IpanemaError('El almacén privado no admite enlaces simbólicos.')
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.parent.chmod(0o700)
    payload = {'project': project.id, 'property': project.data.get('google', {}).get('gsc', {}).get('site_url'),
               'scope': SCOPES['gsc'], 'access_token': token,
               'expires_at': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=expires_in)).isoformat()}
    descriptor, name = tempfile.mkstemp(prefix='.oauth-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w') as stream:
            json.dump(payload, stream)
        os.replace(name, path)
        path.chmod(0o600)
    finally:
        Path(name).unlink(missing_ok=True)


def load_token(project):
    path = credential_path(project)
    if not path.is_file():
        return None
    if path.is_symlink() or path.stat().st_mode & 0o077 or path.parent.stat().st_mode & 0o077:
        raise IpanemaError('Almacén OAuth con permisos inseguros.')
    try:
        data = json.loads(path.read_text())
        expires = dt.datetime.fromisoformat(data['expires_at'])
    except (OSError, ValueError, KeyError, TypeError):
        raise IpanemaError('Credencial privada no válida; no se muestra su contenido.') from None
    if (data.get('project') != project.id or data.get('property') != project.data.get('google', {}).get('gsc', {}).get('site_url')
            or data.get('scope') != SCOPES['gsc']):
        raise IpanemaError('Credencial de otro proyecto, propiedad o scope.')
    if expires <= dt.datetime.now(dt.timezone.utc):
        return None
    return data.get('access_token')
