"""Interfaces verificadas de CLIs; salida no confiable, sin herramientas de edición."""
import json
import math
import re
import shutil
from pathlib import Path

from ..core import IpanemaError, read_json

NAMES={'claude':'claude','codex':'codex','commandcode':'commandcode','antigravity':'agy'}
ANTIGRAVITY_MAX_PROMPT_BYTES=96_000
ANTIGRAVITY_SCHEMA_ROLES=frozenset(('council_proposal','council_objection','council_defense'))


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
    if value['mode']=='dual-agent' and (set(members)!={'claude','codex'} or set(disabled)!=(set(NAMES)-{'claude','codex'})):
        raise IpanemaError('El modo dual no permite CommandCode.')
    if value['mode']=='multi-agent' and len(members)<3:
        raise IpanemaError('El modo multi-agent requiere al menos tres participantes explícitos.')
    for key in ('require_both_for_major_decisions','independent_proposals','cross_examination',
                'require_defense','evidence_based_decisions','production_requires_human_authorization'):
        if value.get(key) is not True:raise IpanemaError('Control obligatorio del consejo deshabilitado: '+key)
    return value


def enabled_agents(root=None):return tuple(agent_policy(root)['members'])


def require_agent(agent,root=None):
    if agent not in enabled_agents(root):raise IpanemaError('Agente deshabilitado por política: '+str(agent))


def required_reviewers(level):
    # Critical work with three or more active identities requires two distinct reviewers.
    return 2 if level=='L4' and len(enabled_agents())>2 else 1


def runtime_binary(agent):
    require_agent(agent)
    return shutil.which(NAMES[agent])


def execution_policy(agent,root=None):
    """Operational readiness is separate from council membership/capability."""
    if agent=='antigravity':
        path=Path(root)/'tools/ipanema/orchestration/models.json' if root else Path(__file__).with_name('models.json')
        if not path.is_file():path=Path(__file__).with_name('models.json')
        value=read_json(path)
        policy=value.get('provider_execution',{}).get(agent,{})
        # A registry edit cannot attest that the credential boundary, egress
        # broker, model access, or tool restrictions have been implemented.
        mandatory=('B1_cli_authentication_not_separated_from_tool_capable_worker',
                   'B2_destination_egress_not_enforced',
                   'model_account_and_output_envelope_unverified',
                   'tool_and_subagent_policy_not_verifiably_disabled')
        configured=policy.get('blockers',[])
        if not isinstance(configured,list) or any(not isinstance(item,str) for item in configured):
            configured=['invalid_execution_policy']
        blockers=list(dict.fromkeys([*mandatory,*configured]))
        return {'enabled':False,'blockers':blockers,
                'identity':'CLI default/session; not authenticated or model-verified'}
    return {'enabled':True,'blockers':[],'identity':'existing V2 provider policy'}


def require_execution_agent(agent,root=None):
    require_agent(agent,root)
    status=execution_policy(agent,root)
    if not status['enabled']:
        raise IpanemaError('Ejecución real bloqueada para '+agent+': '+', '.join(status['blockers'] or ['not_enabled']))


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


def argv(agent,model,effort=None,*,response_schema=None,prompt=None):
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
    elif agent=='antigravity':
        if not isinstance(model,str) or not model.strip():
            raise IpanemaError('Modelo Antigravity no verificado; no se utilizará un default implícito.')
        if response_schema is None:
            raise IpanemaError('Antigravity requiere un rol con JSON Schema verificado; salida sin schema bloqueada.')
        if not isinstance(prompt,str) or not prompt.strip() or len(prompt.encode('utf-8'))>ANTIGRAVITY_MAX_PROMPT_BYTES:
            raise IpanemaError('Prompt Antigravity vacío o supera el límite explícito de '+str(ANTIGRAVITY_MAX_PROMPT_BYTES)+' bytes; no se truncó ni se inició el worker.')
        if effort is not None:
            if effort not in ('low','medium','high','xhigh','max'):
                raise IpanemaError('Esfuerzo Antigravity no admitido por el contrato del CLI.')
        # Linux limits one argv string to 32 pages (128 KiB at the verified 4 KiB
        # page size); 96 KB is a conservative per-argument cap. agy stdin requires
        # stream-json output too, so switching transport also needs a new parser.
        # Flags are limited to those exposed by installed agy --help; this builder does not authorize execution.
        args=[binary,'--model',model,'--output-format','json',
              '--mode','plan','--sandbox','--disable-slash-commands']
        if effort is not None:args+=['--effort',effort]
        if response_schema is not None:
            args+=['--json-schema','/workspace/council-response.schema.json']
        args+=['-p',prompt]
    else:
        args=[binary,'-p','--model',model,'--output-format','text','--max-turns','2','--no-session','--safe-mode','--no-skills',
              '--skip-onboarding','--no-auto-update','--permission-mode','plan']
        if effort:args+=['--effort',effort]
    if response_schema is not None and agent!='antigravity':
        if agent=='codex':args+=['--output-schema','/workspace/council-response.schema.json']
        elif agent=='claude':
            args[args.index('--output-format')+1]='stream-json'
            args+=['--verbose','--include-partial-messages','--json-schema',json.dumps(response_schema,separators=(',',':'))]
        else:args[args.index('--output-format')+1]='json'
    return args


def parse_response(agent,stdout,*,strict=False,expected_schema=None):
    if agent=='antigravity':
        def decode(text,category):
            if not isinstance(text,str) or not text.strip():raise ResponseContractError(category)
            try:
                return json.loads(text,object_pairs_hook=_unique_pairs,
                                  parse_constant=lambda _:(_ for _ in ()).throw(ValueError('invalid constant')))
            except (ValueError,TypeError):
                raise ResponseContractError(category) from None
        envelope=decode(stdout,'antigravity_json_invalid')
        if not isinstance(envelope,dict):raise ResponseContractError('antigravity_json_envelope_invalid')
        required=('conversation_id','status','response','duration_seconds','num_turns','usage')
        missing=[key for key in required if key not in envelope]
        if missing:raise ResponseContractError('antigravity_envelope_incomplete',missing=missing)
        status=envelope.get('status')
        if status!='SUCCESS':
            raise ResponseContractError('antigravity_execution_status',status=status if isinstance(status,str) else 'missing_or_invalid')
        if 'error' in envelope:
            raise ResponseContractError('antigravity_success_with_error')
        if not isinstance(envelope['conversation_id'],str) or not envelope['conversation_id'].strip():
            raise ResponseContractError('antigravity_conversation_id_invalid')
        if not isinstance(envelope.get('response'),str) or not envelope['response'].strip():
            raise ResponseContractError('antigravity_response_missing')
        def finite_number(value):
            return type(value) is int or type(value) is float and math.isfinite(value)
        duration=envelope['duration_seconds'];turns=envelope['num_turns'];usage=envelope['usage']
        if not finite_number(duration) or duration<0:
            raise ResponseContractError('antigravity_duration_invalid')
        if not finite_number(turns) or turns<1:
            raise ResponseContractError('antigravity_num_turns_invalid')
        if not isinstance(usage,dict):raise ResponseContractError('antigravity_usage_invalid')
        documented_usage=('input_tokens','output_tokens','thinking_tokens','cache_read_tokens','total_tokens')
        if any(key not in usage or not finite_number(usage[key]) or usage[key]<0 for key in documented_usage):
            raise ResponseContractError('antigravity_usage_incomplete')
        if {'agent','identity','provider'} & set(envelope):
            raise ResponseContractError('antigravity_identity_claim_rejected')
        if expected_schema is not None:
            if 'structured_output' not in envelope:
                raise ResponseContractError('antigravity_structured_output_missing')
            if not isinstance(envelope.get('json_schema'),dict):
                raise ResponseContractError('antigravity_json_schema_missing')
            if envelope['json_schema']!=expected_schema:
                raise ResponseContractError('antigravity_json_schema_mismatch')
            result=envelope['structured_output']
            if not isinstance(result,dict):raise ResponseContractError('antigravity_structured_output_invalid')
        else:
            raise ResponseContractError('antigravity_schema_required')
        # Provider-supplied identity is never authoritative, regardless of schema.
        def has_identity_claim(value):
            if isinstance(value,dict):
                return bool({'agent','identity','provider'} & set(value)) or any(has_identity_claim(item) for item in value.values())
            if isinstance(value,list):return any(has_identity_claim(item) for item in value)
            return False
        if has_identity_claim(result):
            raise ResponseContractError('antigravity_identity_claim_rejected')
        echoed=decode(envelope['response'],'antigravity_response_json_invalid')
        if echoed!=result:
            raise ResponseContractError('antigravity_response_structured_mismatch')
        validate_schema(result,expected_schema)
        return result
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


def _unique_pairs(pairs):
    value={}
    for key,item in pairs:
        if key in value:raise ValueError('duplicate JSON key')
        value[key]=item
    return value


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
