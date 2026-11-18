"""Linux Bubblewrap boundary for tool-disabled inference workers.

Only a sanitized snapshot is visible; provider authentication is explicitly scoped
by the controller. Network access is optional, not a destination firewall. Never
fall back to an unsandboxed worker when namespaces are unavailable.
"""
from __future__ import annotations

import os
import json
from pathlib import Path
import re
import selectors
import shutil
import signal
import subprocess
import time

from ..core import IpanemaError, beneath


HOME = '/worker-home'
_PRIVATE = {'.git', '.local', '.nuvem', '.env', '.ssh', 'node_modules', '.claude', '.codex', '.commandcode', '.command-code'}
_ENV_PREFIX = {'claude': ('ANTHROPIC_', 'CLAUDE_'), 'codex': ('OPENAI_', 'CODEX_'),
               'commandcode': ('COMMANDCODE_', 'CMD_'), 'qa': ()}


def _commandcode_frame(line):
    """Discard progress snapshots, retain results/errors and every tool signal."""
    try:frame=json.loads(line)
    except (ValueError,UnicodeDecodeError):return line+b'\n'
    if isinstance(frame,dict) and frame.get('type')=='event':
        event=frame.get('event',{})
        kind=event.get('type','') if isinstance(event,dict) else ''
        if isinstance(kind,str) and not any(x in kind.lower() for x in ('tool','error','denied','limit')):
            return b''
    return line+b'\n'


def _base_mounts():
    args = []
    for name in ('/usr', '/bin', '/lib', '/lib64'):
        if Path(name).exists():
            args += ['--ro-bind', name, name]
    for name in ('/etc/ssl', '/etc/resolv.conf', '/etc/hosts', '/etc/nsswitch.conf', '/etc/ld.so.cache', '/etc/localtime'):
        if Path(name).exists():
            args += ['--ro-bind', name, name]
    return args


def probe():
    executable = shutil.which('bwrap')
    if not executable:
        return {'available': False, 'reason': 'bwrap_not_installed', 'fallback': False}
    try:
        result = subprocess.run([executable, '--unshare-user', '--unshare-pid', '--die-with-parent',
            *_base_mounts(), '--proc', '/proc', '--dev', '/dev', '--', '/bin/true'],
            env={'PATH': '/usr/bin:/bin'}, capture_output=True, timeout=5)
        return {'available': result.returncode == 0, 'reason': 'namespace_probe_passed' if result.returncode == 0 else 'namespace_probe_failed',
                'exit_code': result.returncode, 'fallback': False}
    except (OSError, subprocess.TimeoutExpired):
        return {'available': False, 'reason': 'namespace_probe_failed', 'fallback': False}


def _snapshot(path):
    supplied = Path(path)
    if supplied.is_symlink() or not supplied.is_dir():
        raise IpanemaError('El snapshot debe ser un directorio real, sin enlaces.')
    root = supplied.resolve()
    for count, entry in enumerate(root.rglob('*')):
        if count > 20000:
            raise IpanemaError('Snapshot demasiado grande; recuperar solo contexto necesario.')
        if entry.is_symlink() or entry.name in _PRIVATE or entry.name.startswith('.env') or entry.name.endswith('.local.json'):
            raise IpanemaError('El snapshot contiene enlaces, Git, configuración privada o dependencias.')
        if not entry.is_file() and not entry.is_dir():
            raise IpanemaError('El snapshot contiene archivos especiales.')
    return root


def command(argv, snapshot, *, runtime_paths=(), auth_files=None, provider, auth_env=None, network=True):
    """Construct a safe argv/environment pair. This never reads credential contents."""
    if provider!='qa':
        from .adapters import require_agent
        require_agent(provider)
    if provider not in _ENV_PREFIX or not isinstance(argv, (tuple, list)) or not argv or any(not isinstance(a, str) or '\0' in a for a in argv):
        raise IpanemaError('Proveedor o comando de worker inválido.')
    if provider == 'qa' and (network or auth_files or auth_env):
        raise IpanemaError('El QA central no admite red ni credenciales de proveedores.')
    root = _snapshot(snapshot)
    executable = shutil.which('bwrap')
    if not executable:
        raise IpanemaError('bwrap no disponible; ejecución denegada sin fallback.')
    env = {'PATH': '/usr/local/bin:/usr/bin:/bin', 'HOME': HOME, 'TMPDIR': '/tmp',
           'XDG_CONFIG_HOME': HOME + '/.config', 'XDG_CACHE_HOME': HOME + '/.cache',
           'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TERM': 'dumb'}
    for key, value in (auth_env or {}).items():
        # These prefixes define an allowed namespace, not a promise that a CLI
        # supports any particular credential variable. No ambient env is copied.
        if not isinstance(key, str) or not key.startswith(_ENV_PREFIX[provider]) or not re.fullmatch('[A-Z][A-Z0-9_]*', key) or not isinstance(value, str) or '\0' in value:
            raise IpanemaError('Variable de autenticación ajena al proveedor o inválida.')
        env[key] = value
    args = [executable, '--unshare-user', '--unshare-pid', '--unshare-ipc', '--unshare-uts',
            '--die-with-parent', '--new-session', *_base_mounts(), '--proc', '/proc', '--dev', '/dev',
            '--tmpfs', '/tmp', '--tmpfs', HOME]
    if not network:
        args += ['--unshare-net']
    for value in runtime_paths:
        source = Path(value).resolve()
        home_like = source == Path.home() or str(source).startswith('/home/') and len(source.parts) <= 3
        if not source.exists() or str(source) in ('/', '/home', '/root', '/etc', '/tmp') or home_like or source.name in _PRIVATE or beneath(root, source) or beneath(source, root):
            raise IpanemaError('Mount del runtime demasiado amplio o relacionado con el snapshot.')
        if str(source).startswith(('/usr/', '/bin/', '/lib/', '/lib64/')):
            continue
        args += ['--ro-bind', str(source), str(source)]
    destinations = set()
    for value, destination in (auth_files or {}).items():
        source = Path(value)
        relative = Path(destination)
        if source.is_symlink() or not source.is_file() or source.name.startswith('.env') or '.nuvem' in source.parts:
            raise IpanemaError('Auth requiere archivo propio explícito, sin symlink ni configuración de tienda.')
        if relative.is_absolute() or '..' in relative.parts or not relative.parts or str(relative) in destinations:
            raise IpanemaError('Destino auth inválido o repetido.')
        destinations.add(str(relative))
        # Do not allow an authentication source from the commercial snapshot.
        if beneath(source, root):
            raise IpanemaError('La autenticación del worker no pertenece al snapshot comercial.')
        args += ['--ro-bind', str(source.resolve()), HOME + '/' + str(relative)]
    args += ['--ro-bind', str(root), '/workspace', '--chdir', '/workspace', '--remount-ro', '/', '--', *argv]
    return args, env


def _stop(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_isolated(argv, prompt, snapshot, *, runtime_paths=(), auth_files=None, provider,
                 auth_env=None, timeout=120, network=True, max_output_bytes=2_000_000, idle_timeout=0, cancel_event=None,
                 startup_timeout=0,first_response_timeout=0):
    if provider!='qa':
        from .adapters import require_agent
        require_agent(provider)
    if not probe()['available']:
        raise IpanemaError('Aislamiento Bubblewrap no operativo; no se ejecutó el worker.')
    if not isinstance(prompt, str) or len(prompt.encode()) > 1_000_000 or not 1 <= timeout <= 1800 or not 1024 <= max_output_bytes <= 10_000_000:
        raise IpanemaError('Límites de entrada/salida/tiempo inválidos.')
    if type(idle_timeout) not in (int, float) or not 0 <= idle_timeout <= 1800:
        raise IpanemaError('Inactividad permitida: 0 (desactivada) a 1800 segundos.')
    if any(type(v) not in (int,float) or not 0<=v<=1800 for v in (startup_timeout,first_response_timeout)):
        raise IpanemaError('Límites de inicio/primera respuesta inválidos.')
    args, env = command(argv, snapshot, runtime_paths=runtime_paths, auth_files=auth_files,
                        provider=provider, auth_env=auth_env, network=network)
    started = time.monotonic()
    if cancel_event is not None and cancel_event.is_set():
        return {'exit_code':None,'stdout':'','stderr':'','cancelled':True,'process_reaped':True,
                'process_started':False,'context_complete':False,'stdin_bytes_written':0,'duration_s':0}
    try:
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env=env, start_new_session=True)
    except OSError:
        raise IpanemaError('No se pudo iniciar el worker aislado.') from None
    output = {'stdout': bytearray(), 'stderr': bytearray()}
    payload = memoryview(prompt.encode()); sent = 0; total = 0
    timed_out = limited = idle_timed_out = cancelled = False; stopped_at = None
    last_activity = started; written = 0; input_closed_early = False
    spawned=time.monotonic();input_at=spawned if not payload else None;first_stdout=None;first_stderr=None;timeout_phase=None
    event_counts={};event_buffer=bytearray();transport_bytes=0;discarded_bytes=0
    with selectors.DefaultSelector() as selector:
        for pipe, name in ((process.stdout, 'stdout'), (process.stderr, 'stderr')):
            os.set_blocking(pipe.fileno(), False); selector.register(pipe, selectors.EVENT_READ, name)
        if payload:
            os.set_blocking(process.stdin.fileno(), False); selector.register(process.stdin, selectors.EVENT_WRITE, 'stdin')
        else:
            process.stdin.close()
        try:
            while selector.get_map():
                if stopped_at is None and cancel_event is not None and cancel_event.is_set():
                    cancelled = True; stopped_at = time.monotonic(); _stop(process)
                if stopped_at is None and time.monotonic() - started > timeout:
                    timed_out = True;timeout_phase='total'; stopped_at = time.monotonic(); _stop(process)
                if stopped_at is None and startup_timeout and input_at is None and time.monotonic()-spawned>startup_timeout:
                    timed_out=True;timeout_phase='startup_input';stopped_at=time.monotonic();_stop(process)
                if stopped_at is None and first_response_timeout and input_at is not None and first_stdout is None and time.monotonic()-input_at>first_response_timeout:
                    timed_out=True;timeout_phase='first_response';stopped_at=time.monotonic();_stop(process)
                if stopped_at is None and (first_stdout is not None or not first_response_timeout) and idle_timeout and time.monotonic() - last_activity > idle_timeout:
                    idle_timed_out = True; stopped_at = time.monotonic(); _stop(process)
                if stopped_at is not None and time.monotonic() - stopped_at > 2:
                    break
                for key, event in selector.select(.1):
                    pipe, name = key.fileobj, key.data
                    if name == 'stdin':
                        try:
                            n = os.write(pipe.fileno(), payload[sent:sent + 16384]); sent += n; written += n
                            last_activity = time.monotonic()
                        except BlockingIOError:
                            continue
                        except BrokenPipeError:
                            input_closed_early = True; sent = len(payload)
                        if sent == len(payload):
                            input_at=time.monotonic()
                            selector.unregister(pipe); pipe.close()
                    else:
                        try:
                            chunk = os.read(pipe.fileno(), 16384)
                        except BlockingIOError:
                            continue
                        if not chunk:
                            selector.unregister(pipe); pipe.close(); continue
                        last_activity = time.monotonic()
                        transport_bytes+=len(chunk)
                        retained=chunk
                        if name=='stdout':
                            if first_stdout is None:first_stdout=last_activity
                            event_buffer.extend(chunk)
                            kept=bytearray()
                            while b'\n' in event_buffer:
                                line,_,rest=event_buffer.partition(b'\n');event_buffer=bytearray(rest)
                                try:
                                    frame=json.loads(line);kind=frame.get('type') if isinstance(frame,dict) else None
                                    if isinstance(kind,str) and re.fullmatch('[a-zA-Z0-9_.-]{1,64}',kind):event_counts[kind]=event_counts.get(kind,0)+1
                                    nested=frame.get('event',{}) if isinstance(frame,dict) else {}
                                    sub=nested.get('type') if isinstance(nested,dict) else None
                                    if isinstance(sub,str) and re.fullmatch('[a-zA-Z0-9_.-]{1,64}',sub):
                                        event_counts['event:'+sub]=event_counts.get('event:'+sub,0)+1
                                except (ValueError,UnicodeDecodeError):pass
                                if provider=='commandcode':
                                    filtered=_commandcode_frame(line);kept.extend(filtered)
                                    discarded_bytes+=len(line)+1-len(filtered)
                            if provider=='commandcode':retained=bytes(kept)
                            if len(event_buffer)>max_output_bytes:
                                limited=True;stopped_at=time.monotonic();_stop(process);event_buffer.clear()
                        elif first_stderr is None:first_stderr=last_activity
                        available = max(0, max_output_bytes - total)
                        output[name].extend(retained[:available]); total += len(retained)
                        if (total > max_output_bytes or transport_bytes>max_output_bytes*10) and stopped_at is None:
                            limited = True; stopped_at = time.monotonic(); _stop(process)
        finally:
            if process.poll() is None:
                _stop(process)
            process.wait(timeout=5)
            for pipe in (process.stdin, process.stdout, process.stderr):
                if not pipe.closed:
                    pipe.close()
    if provider=='commandcode' and event_buffer and not limited:
        output['stdout'].extend(_commandcode_frame(bytes(event_buffer))[:max(0,max_output_bytes-total)])
    return {'exit_code': process.returncode, 'stdout': output['stdout'].decode('utf-8', errors='replace'),
            'stderr': output['stderr'].decode('utf-8', errors='replace'), 'timed_out': timed_out,
            'output_limited': limited, 'idle_timed_out': idle_timed_out, 'cancelled':cancelled, 'process_started':True, 'process_reaped': process.poll() is not None,
            'stdin_bytes_written': written, 'context_complete': written == len(payload) and not input_closed_early, 'duration_s': round(time.monotonic() - started, 3),
            'timing':{'spawn_s':round(spawned-started,6),'input_complete_s':round(input_at-started,6) if input_at else None,
                      'first_stdout_s':round(first_stdout-started,6) if first_stdout else None,
                      'first_stderr_s':round(first_stderr-started,6) if first_stderr else None,'timeout_phase':timeout_phase,
                      'event_counts':event_counts,'inference_vs_initialization':'not_separable_without_provider_events'},
            'output_accounting':{'transport_bytes':transport_bytes,'retained_bytes':sum(len(b)for b in output.values()),
                                 'discarded_progress_bytes':discarded_bytes,'transport_limit_bytes':max_output_bytes*10,
                                 'retained_limit_bytes':max_output_bytes},
            'isolation': {'backend': 'bubblewrap', 'snapshot_read_only': True, 'host_home_mounted': False,
                          'network': 'enabled_no_destination_firewall' if network else 'disabled',
                          'limitation': 'Provider CLI must disable tools/hooks/MCP. Inference network is not API-only egress enforcement.'}}
