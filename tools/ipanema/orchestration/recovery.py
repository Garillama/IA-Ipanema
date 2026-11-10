"""Supervisión acotada: diagnósticos por códigos, sin conservar salida privada."""
from __future__ import annotations

import re
import shutil
import subprocess
import threading
import time

from ..core import IpanemaError, now


class WorkerFailure(IpanemaError):
    def __init__(self, category, *, reaped=True):
        self.category = category
        self.reaped = reaped
        super().__init__('Worker falló: ' + category + '; salida privada no registrada.')


def execution_limits(task,settings):
    """Bounds are proportional; silent reasoning is not proof of a hung process."""
    tier=task.get('tier','balanced')
    total={'fast':120,'balanced':240,'strong':360,'critical':600}[tier]
    provider=task.get('agent')
    first={'claude':120,'codex':150,'commandcode':180}.get(provider,120)
    if tier in ('strong','critical'):first=min(total,first*2)
    cfg=settings.get('time_limits',{}).get(provider,{})
    values={'timeout':settings.get('timeout_seconds',cfg.get('total',total)),
            'idle_timeout':settings.get('idle_timeout_seconds',cfg.get('idle',90)),
            'startup_timeout':cfg.get('startup',30),
            'first_response_timeout':cfg.get('first_response',first)}
    if any(type(v) not in (int,float) or not 0<=v<=1800 for v in values.values()) or not values['timeout']:
        raise IpanemaError('Límites temporales de worker inválidos.')
    return values


def classify_failure(raw):
    """Solo se llama ante fallo; nunca exporta mensajes, URLs o credenciales."""
    text = (raw.get('stderr', '') + '\n' + raw.get('stdout', '')).lower()
    # Access/rate limits stop the run; do not retry or evade via another provider.
    patterns = [
        ('rate_limit', r'\b429\b|rate[_ -]?limit|too many requests|quota exceeded'),
        ('permission_denied', r'\b403\b|permission denied|access denied|forbidden'),
        ('authentication', r'\b401\b|authentication[_ -]?error|unauthorized|invalid.{0,20}(api.key|token)|token.{0,20}expired|not logged in|please.{0,10}log.?in|oauth.{0,20}(expired|invalid)'),
        ('model_unavailable', r'model.{0,70}(not found|not available|unavailable|does not exist|not supported)|no access.{0,30}model'),
        ('cli_incompatible', r'unknown (option|argument)|unrecognized (option|argument)|invalid option|unexpected argument'),
        ('transient_network', r'econnreset|etimedout|eai_again|connection reset|temporary failure|temporarily unavailable|\b50[234]\b|overloaded_error'),
    ]
    for category, pattern in patterns:
        if category in ('rate_limit','permission_denied') and re.search(pattern,text): return category
    if raw.get('cancelled'): return 'run_cancelled'
    if raw.get('timed_out'): return 'timeout'
    if raw.get('idle_timed_out'): return 'inactivity'
    if raw.get('output_limited'): return 'output_limit'
    for category,pattern in patterns[2:]:
        if re.search(pattern,text): return category
    return 'unknown_provider_error'


def health_check(agent):
    """Local version/help only: installed/authenticated/model-available are distinct."""
    from .adapters import enabled_agents
    if agent not in enabled_agents():return {'enabled':False,'installed':shutil.which(agent)is not None,'reason':'disabled_by_policy','inference_tested':False}
    binary = shutil.which(agent)
    if not binary:
        return {'installed': False, 'cli_compatible': False, 'reason': 'runtime_missing', 'inference_tested': False}
    try:
        v = subprocess.run([binary, '--version'], capture_output=True, text=True, timeout=5)
        h = subprocess.run([binary, '--help'], capture_output=True, text=True, timeout=5)
        version = re.search(r'\b\d+\.\d+\.\d+\b', v.stdout)
        required = {'claude': ['--tools', '--restricted', '--permission-prompts', '--strict-mcp-config', '--no-session-persistence'],
                    'codex': ['exec', '--sandbox'], 'commandcode': ['--safe-mode', '--no-skills', '--permission-mode']}[agent]
        missing = [flag for flag in required if flag not in h.stdout]
        return {'installed': True, 'version': version.group() if version else None,
                'cli_compatible': h.returncode == 0 and not missing, 'missing_flags': missing,
                'inference_tested': False, 'authentication': 'not_checked', 'model_access': 'not_checked'}
    except (OSError, subprocess.TimeoutExpired):
        return {'installed': True, 'cli_compatible': False, 'reason': 'local_health_failed', 'inference_tested': False}


def policy(settings):
    value = settings.get('recovery', {})
    retries = value.get('max_retries', 1)
    threshold = value.get('circuit_failures', 2)
    if type(retries) is not int or not 0 <= retries <= 2 or type(threshold) is not int or not 1 <= threshold <= 3:
        raise IpanemaError('Límites de recuperación inválidos: retries 0–2, circuit_failures 1–3.')
    fallback = value.get('fallback', True)
    if type(fallback) is not bool: raise IpanemaError('fallback debe ser booleano.')
    return {'max_retries': retries, 'circuit_failures': threshold, 'fallback': fallback}


def candidates(plan, task):
    """Preserve independent reviewer providers, including pending L4 reviews."""
    from .adapters import enabled_agents,require_agent,required_reviewers
    require_agent(task['agent'])
    order=[a for a in enabled_agents() if a!=task['agent']]
    tasks = plan.get('tasks', [])
    if task.get('role') == 'review':
        forbidden = {t['agent'] for t in tasks if t is not task and
                     (t.get('role') == 'implementation' and t['id'] in task.get('dependencies', []) or
                      t.get('role') == 'review' and set(t.get('dependencies', [])) & set(task.get('dependencies', [])))}
        order = [agent for agent in order if agent not in forbidden]
    elif task.get('role') == 'implementation':
        count = required_reviewers(plan.get('classification',{}).get('level'))
        reviewers = {t['agent'] for t in tasks if t.get('role') == 'review' and task['id'] in t.get('dependencies', [])}
        if not plan.get('read_only') and (reviewers or int(plan.get('classification', {}).get('level', 'L1')[1]) >= 3):
            order = [agent for agent in order if len(reviewers - {agent}) >= count]
    return order


class Supervisor:
    """Run-scoped circuit, shared safely by independent DAG workers."""
    def __init__(self, settings):
        self.policy = policy(settings)
        self.failures = {}
        self.open = set()
        self.lock = threading.RLock()
        self.cancel_event = threading.Event()

    def state(self):
        with self.lock:
            return {'scope':'current_run_only', 'observed_at':now(), 'open_circuits':sorted(self.open),
                    'failure_counts':dict(self.failures), 'cancelled':self.cancel_event.is_set()}

    def failed(self, agent, category):
        with self.lock:
            if category in ('rate_limit','permission_denied'): self.cancel_event.set()
            self.failures[agent] = self.failures.get(agent, 0) + 1
            if category not in ('transient_network', 'timeout', 'inactivity') or self.failures[agent] >= self.policy['circuit_failures']:
                self.open.add(agent)

    def run(self, plan, task, invoke, checkpoint=None):
        from .adapters import require_agent
        require_agent(task['agent'])
        task.setdefault('assigned_agent', task['agent'])
        attempts = task.setdefault('recovery_attempts', [])
        providers = [task['agent']] + (candidates(plan, task) if self.policy['fallback'] and not task.get('role','').startswith('council_') else [])
        for agent in providers:
            require_agent(agent)
            with self.lock:
                if self.cancel_event.is_set():
                    raise IpanemaError('Ejecución cancelada por denegación; no se lanzan más workers.')
                opened = agent in self.open
            if opened or not shutil.which(agent):
                attempts.append({'agent': agent, 'status': 'not_started', 'category': 'circuit_open' if opened else 'runtime_missing'})
                if checkpoint: checkpoint()
                continue
            for retry in range(self.policy['max_retries'] + 1):
                # Recheck after backoff/other workers, immediately before invocation.
                with self.lock:
                    if self.cancel_event.is_set():
                        raise IpanemaError('Ejecución cancelada; no se reintenta ni reasigna.')
                    if agent in self.open: break
                    previous = task['agent']; prior_execution = dict(task.get('execution', {}))
                    task['agent'] = agent
                    substitution = None
                    if previous != agent:
                        substitution = {'from': previous, 'to': agent, 'context_preserved': None,
                                        'prior_prompt_sha256':prior_execution.get('prompt_sha256'),
                                        'previous_process_reaped':prior_execution.get('process_reaped',True)}
                        task.setdefault('substitutions', []).append(substitution)
                if checkpoint: checkpoint()
                try:
                    response = invoke()
                    if self.cancel_event.is_set(): raise WorkerFailure('run_cancelled',reaped=task.get('execution',{}).get('process_reaped',True))
                    self._context_proof(task,substitution)
                    attempts.append({'agent': agent, 'retry': retry, 'status': 'completed', 'execution': dict(task.get('execution', {}))})
                    if checkpoint: checkpoint()
                    return response
                except WorkerFailure as exc:
                    self._context_proof(task,substitution)
                    if not exc.reaped: self.cancel_event.set()
                    self.failed(agent, exc.category)
                    attempts.append({'agent': agent, 'retry': retry, 'status': 'failed', 'category': exc.category,
                                     'process_reaped': exc.reaped, 'execution': dict(task.get('execution', {}))})
                    if checkpoint: checkpoint()
                    if not exc.reaped:
                        self.cancel_event.set()
                        raise IpanemaError('No se acreditó cancelación del worker; reasignación prohibida.') from None
                    if exc.category in ('rate_limit', 'permission_denied', 'run_cancelled') or self.cancel_event.is_set():
                        raise IpanemaError('Proveedor denegó acceso/cuota o run cancelado; sin reintentos ni evasión.') from None
                    with self.lock: opened = agent in self.open
                    if exc.category not in ('transient_network', 'timeout', 'inactivity') or retry == self.policy['max_retries'] or opened:
                        break
                    time.sleep(.25)
        raise IpanemaError('No queda proveedor compatible disponible; no se omiten revisiones independientes.')

    def _context_proof(self,task,substitution):
        if substitution is not None:
            current=task.get('execution',{}).get('prompt_sha256')
            prior=substitution.get('prior_prompt_sha256')
            substitution['current_prompt_sha256']=current
            substitution['context_preserved']=(current==prior) if current and prior else None
