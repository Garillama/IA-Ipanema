"""Interfaces verificadas de CLIs; salida no confiable, sin herramientas de edición."""
import json
import re
import shutil
from pathlib import Path

from ..core import IpanemaError, read_json

NAMES={'claude':'claude','codex':'codex','commandcode':'commandcode'}


def agent_policy(root=None):
    """One existing registry owns participation; local runtime overrides cannot enable agents."""
    path=(Path(root)/'tools/ipanema/orchestration/models.json') if root else Path(__file__).with_name('models.json')
    if not path.is_file():path=Path(__file__).with_name('models.json')
    value=read_json(path).get('council')
    if not isinstance(value,dict) or value.get('mode') not in ('dual-agent','multi-agent') or value.get('enabled') is not True:
        raise IpanemaError('Política del consejo ausente/inválida en models.json.')
    members=value.get('members');disabled=value.get('disabled')
    if (not isinstance(members,list) or not isinstance(disabled,list) or any(not isinstance(a,str)for a in members+disabled)
        or len(set(members))!=len(members)
        or set(members)&set(disabled) or set(members)|set(disabled)!=set(NAMES)
        or not {'claude','codex'}<=set(members) or value.get('max_deliberation_rounds')!=2):
        raise IpanemaError('Participantes/deshabilitados inválidos; Claude y Codex son obligatorios.')
    if value['mode']=='dual-agent' and (set(members)!={'claude','codex'} or set(disabled)!={'commandcode'}):
        raise IpanemaError('El modo dual no permite CommandCode.')
    for key in ('require_both_for_major_decisions','independent_proposals','cross_examination',
                'require_defense','evidence_based_decisions','production_requires_human_authorization'):
        if value.get(key) is not True:raise IpanemaError('Control obligatorio del consejo deshabilitado: '+key)
    return value


def enabled_agents(root=None):return tuple(agent_policy(root)['members'])


def require_agent(agent,root=None):
    if agent not in enabled_agents(root):raise IpanemaError('Agente deshabilitado por política: '+str(agent))


def required_reviewers(level):
    # Dual: one provider independent from the implementer, never two fabricated votes.
    return 2 if level=='L4' and len(enabled_agents())>2 else 1


class ResponseContractError(IpanemaError):
    """Only controller-defined diagnostics; never logs rejected model contents."""
    def __init__(self, category, path='$', **details):
        self.diagnostic={'category':category,'path':path,**details}
        super().__init__('Contrato rechazado: '+category+' en '+path)


def validate_schema(value, schema, path='$'):
    kind=schema.get('type')
    valid={'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),
           'number':type(value) in (int,float),'boolean':type(value) is bool,'null':value is None}
    if kind and not valid.get(kind,False):raise ResponseContractError('schema_type',path,expected_type=kind)
    if 'enum' in schema and value not in schema['enum']:raise ResponseContractError('schema_enum',path)
    if kind=='object':
        for key in schema.get('required',[]):
            if key not in value:raise ResponseContractError('missing_field',path+'.'+key)
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False and set(value)-set(props):
            raise ResponseContractError('additional_fields',path)
        for key,sub in props.items():
            if key in value:validate_schema(value[key],sub,path+'.'+key)
    if kind=='array':
        if not schema.get('minItems',0)<=len(value)<=schema.get('maxItems',100):raise ResponseContractError('schema_length',path)
        for index,item in enumerate(value):validate_schema(item,schema.get('items',{}),path+'['+str(index)+']')
    if kind=='string' and not schema.get('minLength',0)<=len(value)<=schema.get('maxLength',12000):
        raise ResponseContractError('schema_length',path)
    if kind=='string' and 'pattern' in schema and not re.fullmatch(schema['pattern'],value):
        raise ResponseContractError('schema_pattern',path)
    if kind=='number' and not schema.get('minimum',float('-inf'))<=value<=schema.get('maximum',float('inf')):
        raise ResponseContractError('schema_range',path)
    return value


def argv(agent,model,effort=None,*,response_schema=None):
    require_agent(agent)
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
    if response_schema is not None:
        if agent=='codex':args+=['--output-schema','/workspace/council-response.schema.json']
        elif agent=='claude':
            args[args.index('--output-format')+1]='stream-json'
            args+=['--verbose','--include-partial-messages','--json-schema',json.dumps(response_schema,separators=(',',':'))]
        else:args[args.index('--output-format')+1]='json'
    return args


def parse_response(agent,stdout,*,strict=False):
    def unique_object(pairs):
        obj={}
        for key,value in pairs:
            if key in obj:raise ResponseContractError('json_duplicate_key')
            obj[key]=value
        return obj
    def invalid_constant(value):raise ResponseContractError('json_syntax')
    def decode(text):
        return json.loads(text,**({'object_pairs_hook':unique_object,'parse_constant':invalid_constant} if strict else {}))
    candidates=[]
    try:
        value=decode(stdout)
        candidates.append(value)
    except ValueError:
        for line in stdout.splitlines():
            try:candidates.append(decode(line))
            except ValueError:continue
    texts=[];direct=[]
    for value in candidates:
        if not isinstance(value,dict):continue
        if value.get('stop_reason') in ('max_tokens','length') or value.get('finish_reason')=='length':raise ResponseContractError('output_truncation')
        if value.get('subtype')=='max_turns' or value.get('stopReason')=='max_turns':raise ResponseContractError('incomplete_response')
        if 'decision' in value and 'changes' in value:direct.append(value)
        if value.get('is_error'):raise ResponseContractError('provider_error')
        if isinstance(value.get('structured_output'),dict):direct.append(value['structured_output'])
        if value.get('type')=='result' and value.get('subtype') not in (None,'success'):
            raise ResponseContractError('provider_error')
        if value.get('type')=='item.completed' and value.get('item',{}).get('type') in ('command_execution','mcp_tool_call'):
            raise ResponseContractError('unexpected_tool_execution')
        if value.get('type')=='event' and isinstance(value.get('event'),dict) and 'tool' in str(value['event'].get('type','')).lower():
            raise ResponseContractError('unexpected_tool_execution')
        for key in ('result','text','output','finalText'):
            if isinstance(value.get(key),str):texts.append(value[key])
        item=value.get('item',{})
        if isinstance(item,dict) and item.get('type')=='agent_message':texts.append(item.get('text',''))
    if direct:return direct[-1]
    last_error=None
    for text in reversed(texts):
        text=text.strip()
        if text.startswith('```') and not strict:
            text='\n'.join(text.splitlines()[1:-1])
        try:
            value=decode(text)
            if isinstance(value,dict):return value
            raise ResponseContractError('schema_type',expected_type='object')
        except json.JSONDecodeError as exc:last_error=exc
    if last_error:raise ResponseContractError('json_syntax',line=last_error.lineno,column=last_error.colno)
    raise ResponseContractError('missing_final_response' if candidates else 'adapter_envelope')


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
