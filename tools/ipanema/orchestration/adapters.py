"""Interfaces verificadas de CLIs; salida no confiable, sin herramientas de edición."""
import json
import shutil
from pathlib import Path

from ..core import IpanemaError, read_json

NAMES={'claude':'claude','codex':'codex','commandcode':'commandcode'}


def argv(agent,model,effort=None):
    binary=shutil.which(NAMES[agent])
    if not binary:raise IpanemaError('Runtime no instalado: '+agent)
    if agent=='claude':
        args=[binary,'-p','--model',model,'--output-format','json','--tools','','--restricted','--permission-mode','dontAsk',
              '--permission-prompts','none','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--setting-sources','','--no-session-persistence']
        if effort:args+=['--effort',effort]
    elif agent=='codex':
        args=[binary,'-a','never','exec','-','--model',model,'--json','--ephemeral','--ignore-user-config','--ignore-rules','--sandbox','read-only','--skip-git-repo-check']
        if effort:args+=['-c','model_reasoning_effort='+json.dumps(effort)]
    else:
        args=[binary,'-p','--model',model,'--output-format','text','--max-turns','2','--no-session','--safe-mode','--no-skills',
              '--skip-onboarding','--no-auto-update','--permission-mode','plan']
        if effort:args+=['--effort',effort]
    return args


def parse_response(agent,stdout):
    candidates=[]
    try:
        value=json.loads(stdout)
        candidates.append(value)
    except ValueError:
        for line in stdout.splitlines():
            try:candidates.append(json.loads(line))
            except ValueError:continue
    texts=[]
    for value in candidates:
        if not isinstance(value,dict):continue
        if 'decision' in value and 'changes' in value:return value
        if value.get('is_error'):raise IpanemaError('El proveedor informó error; no se acepta la respuesta.')
        if isinstance(value.get('structured_output'),dict):return value['structured_output']
        if value.get('type')=='result' and value.get('subtype') not in (None,'success'):
            raise IpanemaError('CommandCode no terminó con éxito.')
        if value.get('type')=='item.completed' and value.get('item',{}).get('type') in ('command_execution','mcp_tool_call'):
            raise IpanemaError('Worker invocó herramientas; se requiere revisión.')
        for key in ('result','text','output','finalText'):
            if isinstance(value.get(key),str):texts.append(value[key])
        item=value.get('item',{})
        if isinstance(item,dict) and item.get('type')=='agent_message':texts.append(item.get('text',''))
    for text in reversed(texts):
        text=text.strip()
        if text.startswith('```'):
            text='\n'.join(text.splitlines()[1:-1])
        try:
            value=json.loads(text)
            if isinstance(value,dict):return value
        except ValueError:continue
    raise IpanemaError('Respuesta sin contrato JSON; no se aplica ni se simula aprobación.')


def model_for(root,agent,tier):
    catalog=read_json(root/'tools/ipanema/orchestration/models.json')
    selected=catalog['profiles'][agent][tier]
    return {**selected,'reason':tier+' según complejidad/riesgo; sin escalado automático por fallo de autenticación.',
            'verified_at':catalog['verified_at']}


def usage_metrics(stdout):
    """Only numeric counters actually emitted, no inferred prices or token estimates."""
    observed={}
    for line in stdout.splitlines():
        try:value=json.loads(line)
        except ValueError:continue
        if not isinstance(value,dict):continue
        for key in ('total_cost_usd','duration_ms','durationMs'):
            if type(value.get(key)) in (int,float):observed[key]=value[key]
        usage=value.get('usage',{})
        if isinstance(usage,dict):
            for key,number in usage.items():
                if type(number) in (int,float) and ('token' in key.lower() or 'cost' in key.lower()):observed[key]=number
    return {'provider_reported':observed,'measured_cost_available':any('cost' in key for key in observed),'estimated_cost':None}
