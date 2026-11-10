"""Contratos y decisión del consejo; sin inferencia, comandos ni permisos remotos.

Los recibos son un ledger del controlador, nunca campos de una respuesta del
modelo. Un hash de fuente prueba identidad; no acredita una restricción técnica.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re

from ..core import IpanemaError, now

AGENTS = ('claude', 'codex', 'commandcode')
HARD_CONSTRAINTS = ('functional', 'security', 'compatibility', 'native_reuse')
CRITERIA = HARD_CONSTRAINTS + ('seo', 'performance', 'accessibility', 'responsive',
                             'maintainability', 'reversibility', 'complexity',
                             'development_cost', 'execution_cost')
STATES = ('pass', 'fail', 'unknown')
IMPACTS = ('seo', 'performance', 'responsive', 'accessibility')


def alternative_fingerprint(alternative):
    """Identidad de solución, no del ID local ni de sus opiniones sobre calidad.

    Diferencias de archivos, requisitos de prueba o descripción no se consideran
    equivalencia semántica automáticamente. El controlador debe deliberarlas.
    """
    value = {'description': alternative['description'], 'files': sorted(alternative.get('files', [])),
             'tests': sorted(alternative.get('tests', []))}
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def config_policy(level, mode='auto', max_rounds=2):
    from .adapters import agent_policy
    participation=agent_policy()
    if level not in ('L1', 'L2', 'L3', 'L4') or mode not in ('auto', 'full', 'off'):
        raise IpanemaError('Nivel o modo del consejo inválido.')
    if type(max_rounds) is not int or not 1 <= max_rounds <= 2:
        raise IpanemaError('El consejo admite una o dos rondas totales.')
    if mode == 'off' and level in ('L3', 'L4'):
        raise IpanemaError('No se puede omitir el consejo en L3/L4.')
    enabled = mode == 'full' or mode == 'auto' and level in ('L3', 'L4')
    if enabled and level in ('L3','L4') and max_rounds<2 and participation['require_defense']:
        raise IpanemaError('Las decisiones mayores requieren contraste y defensa, máximo dos intercambios.')
    return {'enabled': enabled, 'mode': mode, 'max_rounds': max_rounds,
            'system_mode':participation['mode'],'protocol_version':2 if participation['require_defense'] else 1,
            'required_agents': list(participation['members']) if enabled else [],
            'require_defense':enabled and participation['require_defense'] and max_rounds>=2,
            'independent_first_round': True, 'local_implementation_only': True,
            'production_authorized': False}


def contract(role):
    """Contrato compacto para insertar en el prompt existente del worker."""
    if role=='council_defense':return dual_contract(role)
    if role == 'council_proposal':
        value={'role': role, 'instruction': 'Investiga independientemente sin conocer otras propuestas. '
                'Describe hechos e hipótesis; no declares ejecutadas pruebas. No inventes recibos. '
                'Los estados pass son afirmaciones que el controlador deberá comprobar.',
                'example': {'decision': 'proposed', 'summary': 'Resumen técnico', 'evidence': [], 'changes': [],
                            'analysis': {'problem': 'Problema observado', 'cause': 'Causa comprobada o no determinada',
                                         'evidence_refs': [], 'hypotheses': [], 'recommendation': 'native',
                                         'alternatives': [{'id': 'native', 'description': 'Alternativa nativa real',
                                                           'constraints': {k: {'status': 'unknown', 'evidence_refs': []}
                                                                           for k in CRITERIA},
                                                           'files': [], 'tests': ['Comprobar el contrato relevante']}],
                                         'native_components': [], 'files': [], 'risks': [],
                                         'impacts': {k: 'No medido o explicar impacto' for k in IMPACTS},
                                         'tests': ['Prueba necesaria'], 'confidence': 0.5}}}
        from .adapters import agent_policy
        if agent_policy()['require_defense']:
            value['example']['analysis']['impacts'].update(uiux='Impacto UI/UX o no aplicable con motivo',commerce='Contratos comerciales afectados o no aplicable con motivo')
        return value
    if role == 'council_objection':
        value={'role': role, 'instruction': 'Contrasta propuestas con fuentes; objeta aspectos concretos. '
                'Un estado resolved no prueba resolución: requiere un recibo del controlador ligado a la objeción. '
                'No inventes consenso ni ejecuciones.',
                'example': {'decision': 'approve', 'summary': 'Contraste y límites', 'evidence': [], 'changes': [],
                            'preferred_alternative': 'native', 'objections': [
                                {'id': 'O1', 'alternative_id': 'native', 'category': 'compatibility',
                                 'severity': 'critical', 'claim': 'Contrato potencialmente incumplido',
                                 'evidence_refs': [], 'resolution_evidence_refs': [], 'status': 'open'}]}}
        from .adapters import agent_policy
        if agent_policy()['require_defense']:
            value['example']['questions']=[{'id':'Q1','to_agent':'codex','alternative_id':'native',
                'question':'Pregunta sobre una fuente o prueba concreta','evidence_refs':[]}]
        return value
    raise IpanemaError('Rol de consejo no soportado.')


def dual_contract(role):
    """Extend existing role contracts, retaining legacy proposal/objection readers."""
    if role=='council_defense':
        value=copy.deepcopy(contract('council_objection'))
        value['example'].pop('questions',None)
        value['role']=role;value['instruction']='Responde cada pregunta recibida con evidencia. Puedes defender, corregir, retirar o pedir pruebas; no inventes resoluciones.'
        value['example']['answers']=[{'question_id':'Q1','from_agent':'claude','answer':'Respuesta técnica concisa',
                                     'evidence_refs':[],'disposition':'needs_evidence'}]
        value['example']['withdrawn_alternatives']=[]
        value['example']['revision_notes']=[]
        return value
    value=copy.deepcopy(contract(role))
    if role=='council_objection':
        value['example']['questions']=[{'id':'Q1','to_agent':'codex','alternative_id':'native',
                                       'question':'Pregunta vinculada a una fuente o prueba concreta','evidence_refs':[]}]
    return value


def response_schema(role,*,dual=None):
    """Same role contract, bounded and enforceable by native provider schemas."""
    def shape(value):
        if isinstance(value,dict):
            return {'type':'object','properties':{k:shape(v) for k,v in value.items()},
                    'required':list(value),'additionalProperties':False}
        if isinstance(value,list):return {'type':'array','items':shape(value[0]) if value else {'type':'string'},'maxItems':8}
        if isinstance(value,str):return {'type':'string','minLength':1,'maxLength':1000}
        return {'type':'number','minimum':0,'maximum':1}
    if dual is None:
        from .adapters import agent_policy
        dual=agent_policy()['require_defense']
    schema=shape((dual_contract(role)if dual or role=='council_defense'else contract(role))['example'])
    schema['properties']['decision']['enum']=['approve','proposed','changes_requested','blocked']
    schema['properties']['changes']={'type':'array','items':{'type':'string'},'maxItems':0}
    if role=='council_proposal':
        alt=schema['properties']['analysis']['properties']['alternatives']
        alt.update(minItems=1,maxItems=3)
        alt['items']['properties']['id'].update(pattern=r'^[a-z][a-z0-9-]{0,50}$',maxLength=51)
        schema['properties']['analysis']['properties']['tests']['minItems']=1
        alt['items']['properties']['tests']['minItems']=1
        for value in alt['items']['properties']['constraints']['properties'].values():
            value['properties']['status']['enum']=list(STATES)
    else:
        schema['properties']['objections']['maxItems']=8
        if role=='council_objection' and dual:schema['properties']['questions']['minItems']=1
        if role=='council_defense':schema['properties']['answers']['minItems']=1
        obj=schema['properties']['objections']['items']['properties']
        obj['severity']['enum']=['critical','high','medium','low']
        obj['status']['enum']=['open','resolved']
        if role=='council_defense':
            schema['properties']['answers']['items']['properties']['disposition']['enum']=['defend','revise','withdraw','needs_evidence']
    return schema


def participant_task(agent, round_index, read_files, tier, objective, proposals=None):
    if agent not in AGENTS or type(round_index) is not int or round_index not in (0, 1):
        raise IpanemaError('Participante o ronda inválida.')
    if tier not in ('fast', 'balanced', 'strong', 'critical'):
        raise IpanemaError('Perfil de modelo inválido.')
    role = 'council_proposal' if round_index == 0 else 'council_objection'
    specialty = {'claude': 'arquitectura y reutilización', 'codex': 'viabilidad e integración',
                 'commandcode': 'calidad, SEO, rendimiento y accesibilidad'}[agent]
    from .adapters import agent_policy
    use_dual=agent_policy()['require_defense']
    context = {'round_index': round_index, 'specialty': specialty,
               'independent': round_index == 0, 'response_contract': contract(role)}
    if use_dual:context['response_contract']=dual_contract(role)
    if round_index:
        context['peer_proposals'] = copy.deepcopy(proposals or [])
    # No proposals, history or responses are included in round zero.
    return {'id': 'council-' + ('proposal-' if round_index == 0 else 'objection-') + agent,
            'objective': objective, 'role': role, 'agent': agent, 'tier': tier,
            'allowed_files': [], 'read_files': list(read_files), 'dependencies': [],
            'tests': ['central-qa'], 'state': 'pending', 'result': None,
            'council_context': context}


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 12000:
        raise IpanemaError('Texto de consejo inválido: ' + label)
    return value.strip()


def _strings(value, label, limit=100):
    if not isinstance(value, list) or len(value) > limit:
        raise IpanemaError('Lista de consejo inválida: ' + label)
    return list(dict.fromkeys(_text(x, label) for x in value))


def _files(value, allowed_files):
    # Import lazy: planner may use this module when constructing its policy.
    from .planner import safe_path
    allowed = set(allowed_files)
    result = [safe_path(x) for x in _strings(value, 'files')]
    if set(result) - allowed:
        raise IpanemaError('La propuesta del consejo excede archivos autorizados.')
    return result


def _base(response):
    if not isinstance(response, dict) or response.get('decision') not in ('approve', 'proposed', 'changes_requested', 'blocked'):
        raise IpanemaError('Respuesta de consejo fuera del contrato.')
    if response.get('changes') != []:
        raise IpanemaError('Los participantes del consejo no escriben código.')
    if len(json.dumps(response, ensure_ascii=False).encode()) > 200000:
        raise IpanemaError('Respuesta del consejo demasiado grande.')
    result={'decision': response['decision'], 'summary': _text(response.get('summary'), 'summary'), 'changes': []}
    if 'evidence' in response:result['evidence']=_strings(response['evidence'],'evidence')
    return result


def _criterion(value):
    if not isinstance(value, dict) or value.get('status') not in STATES:
        raise IpanemaError('Cada criterio debe declarar status pass/fail/unknown.')
    return {'status': value['status'], 'evidence_refs': _strings(value.get('evidence_refs', []), 'evidence_refs')}


def validate_proposal(response, allowed_files):
    result = _base(response)
    analysis = response.get('analysis')
    if not isinstance(analysis, dict):
        raise IpanemaError('Falta análisis independiente estructurado.')
    normal = {k: _text(analysis.get(k), k) for k in ('problem', 'cause', 'recommendation')}
    for k in ('evidence_refs', 'hypotheses', 'native_components', 'risks', 'tests'):
        normal[k] = _strings(analysis.get(k), k)
    if not normal['tests']:
        raise IpanemaError('La propuesta debe declarar pruebas de aceptación.')
    normal['files'] = _files(analysis.get('files'), allowed_files)
    impacts = analysis.get('impacts')
    if not isinstance(impacts, dict):
        raise IpanemaError('Faltan impactos de la propuesta.')
    normal['impacts'] = {k: _text(impacts.get(k), k) for k in IMPACTS}
    for k in ('uiux','commerce'):
        if k in impacts:normal['impacts'][k]=_text(impacts[k],k)
    confidence = analysis.get('confidence')
    if type(confidence) not in (int, float) or not 0 <= confidence <= 1:
        raise IpanemaError('Confianza inválida; usar valor entre cero y uno.')
    normal['confidence'] = confidence
    alternatives = analysis.get('alternatives')
    if not isinstance(alternatives, list) or not 1 <= len(alternatives) <= 20:
        raise IpanemaError('Se requiere al menos una alternativa real y como máximo veinte.')
    normal['alternatives'] = []
    ids = set()
    for alt in alternatives:
        if not isinstance(alt, dict) or not re.fullmatch(r'[a-z][a-z0-9-]{0,50}', str(alt.get('id', ''))):
            raise IpanemaError('Identificador de alternativa inválido.')
        if alt['id'] in ids:
            raise IpanemaError('Alternativa repetida dentro de una propuesta.')
        ids.add(alt['id'])
        values = alt.get('constraints')
        if not isinstance(values, dict) or not set(HARD_CONSTRAINTS) <= set(values):
            raise IpanemaError('Faltan restricciones obligatorias de la alternativa.')
        if set(values) - set(CRITERIA):
            raise IpanemaError('Criterio desconocido en matriz del consejo.')
        criteria = {k: _criterion(values.get(k, {'status': 'unknown'})) for k in CRITERIA}
        tests = _strings(alt.get('tests', normal['tests']), 'tests')
        if not tests:
            raise IpanemaError('Cada alternativa debe declarar pruebas.')
        normal['alternatives'].append({'id': alt['id'], 'description': _text(alt.get('description'), 'description'),
                                       'constraints': criteria,
                                       'files': _files(alt.get('files', normal['files']), allowed_files),
                                       'tests': tests})
    if normal['recommendation'] not in ids:
        raise IpanemaError('La recomendación debe referir una alternativa incluida.')
    result['analysis'] = normal
    return result


def validate_objections(response, allowed_files=()):
    result = _base(response)
    rows = response.get('objections')
    if not isinstance(rows, list) or len(rows) > 100:
        raise IpanemaError('Lista de objeciones inválida.')
    normal = []
    ids = set()
    for row in rows:
        if not isinstance(row, dict) or not re.fullmatch(r'[a-zA-Z0-9._-]{1,80}', str(row.get('id', ''))):
            raise IpanemaError('ID de objeción inválido.')
        if row['id'] in ids:
            raise IpanemaError('Objeción repetida.')
        ids.add(row['id'])
        if row.get('severity') not in ('critical', 'high', 'medium', 'low'):
            raise IpanemaError('Severidad de objeción inválida.')
        if row.get('status', 'open') not in ('open', 'resolved'):
            raise IpanemaError('Estado de objeción inválido.')
        normal.append({'id': row['id'], 'alternative_id': _text(row.get('alternative_id'), 'alternative_id'),
                       'category': _text(row.get('category'), 'category'), 'severity': row['severity'],
                       'claim': _text(row.get('claim'), 'claim'), 'status': row.get('status', 'open'),
                       'evidence_refs': _strings(row.get('evidence_refs', []), 'evidence_refs'),
                       'resolution_evidence_refs': _strings(row.get('resolution_evidence_refs', []), 'resolution_evidence_refs')})
    result['objections'] = normal
    result['preferred_alternative'] = response.get('preferred_alternative')
    if result['preferred_alternative'] is not None:
        result['preferred_alternative'] = _text(result['preferred_alternative'], 'preferred_alternative')
    if 'questions' in response:
        questions=response['questions']
        if not isinstance(questions,list)or len(questions)>8:raise IpanemaError('Preguntas de contraste inválidas.')
        result['questions']=[];seen=set()
        for q in questions:
            if not isinstance(q,dict)or not re.fullmatch('[a-zA-Z0-9._-]{1,80}',str(q.get('id','')))or q['id']in seen:
                raise IpanemaError('Identificador de pregunta inválido/repetido.')
            seen.add(q['id'])
            result['questions'].append({k:_text(q.get(k),k)for k in ('id','to_agent','alternative_id','question')}|
                                       {'evidence_refs':_strings(q.get('evidence_refs'),'evidence_refs')})
    return result


def assigned_defense_answers(examinations,agent):
    return {(e['requested_agent'],q['id'])for e in examinations for q in e.get('response',{}).get('questions',[])if q['to_agent']==agent}


def validate_defense(response,allowed_files=(),*,expected_answers=None):
    result=validate_objections(response,allowed_files)
    rows=response.get('answers')
    if not isinstance(rows,list)or len(rows)>8:raise IpanemaError('Respuestas de defensa inválidas.')
    result['answers']=[];seen=set()
    for row in rows:
        if not isinstance(row,dict)or row.get('disposition')not in ('defend','revise','withdraw','needs_evidence'):
            raise IpanemaError('Disposición de defensa inválida.')
        key=(row.get('from_agent'),row.get('question_id'))
        if key in seen:raise IpanemaError('Respuesta duplicada.')
        seen.add(key)
        result['answers'].append({k:_text(row.get(k),k)for k in ('question_id','from_agent','answer','disposition')}|
                                  {'evidence_refs':_strings(row.get('evidence_refs'),'evidence_refs')})
    if expected_answers is not None and seen!=set(expected_answers):
        raise IpanemaError('La defensa debe responder exactamente las preguntas asignadas al participante.')
    result['withdrawn_alternatives']=_strings(response.get('withdrawn_alternatives'),'withdrawn_alternatives')
    result['revision_notes']=_strings(response.get('revision_notes'),'revision_notes')
    return result


def _ledger(evidence, context):
    valid, invalid = {}, []
    if not isinstance(evidence, list) or len(evidence) > 1000:
        raise IpanemaError('Ledger del controlador inválido.')
    for receipt in evidence:
        if not isinstance(receipt, dict) or not isinstance(receipt.get('id'), str):
            invalid.append('malformed_receipt'); continue
        ident = receipt['id']
        if ident in valid:
            raise IpanemaError('IDs duplicados en ledger de evidencia.')
        if not context or receipt.get('context') != context or not re.fullmatch(r'[a-f0-9]{64}', str(receipt.get('sha256', ''))):
            invalid.append(ident); continue
        if receipt.get('kind') not in ('source', 'constraint', 'resolution', 'qa'):
            invalid.append(ident); continue
        if receipt.get('kind') in ('constraint', 'resolution') and not re.fullmatch(
                r'[a-f0-9]{64}', str(receipt.get('alternative_sha256', ''))):
            invalid.append(ident); continue
        if type(receipt.get('executed')) is not bool or type(receipt.get('passed')) is not bool:
            invalid.append(ident); continue
        valid[ident] = receipt
    return valid, invalid


def _proven(receipt):
    return receipt.get('executed') is True and receipt.get('passed') is True


def _resolution(ledger, subject, key, refs=None, fingerprint=None):
    if fingerprint is None:
        return []
    return [r['id'] for r in ledger.values() if r.get('kind') == 'resolution' and
            r.get('alternative_sha256') == fingerprint and
            r.get('subject') in (subject, '*') and isinstance(r.get('resolves'), list) and
            key in r['resolves'] and _proven(r) and
            (not refs or r['id'] in refs)]


def aggregate(proposals, objections, *, evidence, required_agents=None, level='L3',
              project=None, objective=None, context=None,defenses=None):
    if required_agents is None:
        from .adapters import enabled_agents
        required_agents=enabled_agents()
    """Decide por restricciones comprobadas; nunca convierte votos en pruebas.

    Envelopes de entrada son del controlador: requested_agent/effective_agent y
    response (o error). context liga cada recibo al run, proyecto y fuente exactos.
    """
    if level not in ('L1', 'L2', 'L3', 'L4'):
        raise IpanemaError('Nivel de consejo inválido.')
    required = list(required_agents)
    if not required or len(set(required)) != len(required) or set(required) - set(AGENTS):
        raise IpanemaError('Participantes requeridos inválidos.')
    if not isinstance(proposals, list) or not isinstance(objections, list):
        raise IpanemaError('Propuestas/objeciones deben ser listas de envelopes.')
    context = copy.deepcopy(context)
    if context is not None and not isinstance(context, dict):
        raise IpanemaError('Contexto del consejo inválido.')
    extra = (context or {}).get('required_constraints', [])
    if not isinstance(extra, list) or set(extra) - set(CRITERIA):
        raise IpanemaError('Restricciones adicionales inválidas.')
    mandatory = list(dict.fromkeys(HARD_CONSTRAINTS + tuple(extra)))
    ledger, invalid_receipts = _ledger(evidence, context)
    scoped_files = (context or {}).get('files', [])
    if not isinstance(scoped_files, (list, dict)):
        raise IpanemaError('El controlador debe declarar archivos autorizados en context.files.')
    known_files = set(scoped_files)
    # Never derive authority from a model's own analysis.files declaration.
    participants, seen, effective, reasons = [], set(), set(), []
    candidates = {}
    recommendations = []
    for env in proposals:
        if not isinstance(env, dict) or env.get('requested_agent') not in required:
            reasons.append('Participante solicitado desconocido'); continue
        requested = env['requested_agent']
        if requested in seen:
            reasons.append('Propuesta duplicada para ' + requested); continue
        seen.add(requested)
        actual = env.get('effective_agent')
        item = {'requested_agent': requested, 'effective_agent': actual, 'status': 'unavailable'}
        if actual not in AGENTS or not env.get('response'):
            item['error'] = env.get('error', 'missing_response'); participants.append(item); continue
        try:
            proposal = validate_proposal(env['response'], known_files)
        except (IpanemaError, TypeError, ValueError):
            item.update(status='invalid', error='invalid_proposal_contract'); participants.append(item); continue
        item.update(status='available', proposal=proposal)
        if actual in effective:
            reasons.append('Proveedor efectivo duplicado: ' + actual)
        effective.add(actual)
        participants.append(item)
        if proposal['decision'] in ('blocked', 'changes_requested'):
            reasons.append('Participante no recomienda implementar: ' + requested)
        analysis = proposal['analysis']
        recommendations.append(analysis['recommendation'])
        for alt in analysis['alternatives']:
            candidates.setdefault(alt['id'], []).append({'participant': requested, 'analysis': analysis, 'alternative': alt})
    available = [p for p in participants if p['status'] == 'available']
    coverage_complete = (set(p['requested_agent'] for p in available) == set(required) and len(effective) == len(required)
                         and len(proposals) == len(required))
    if not coverage_complete: reasons.append('Deliberación incompleta: faltan participantes originales o proveedores independientes')
    identities = {ident: sorted({alternative_fingerprint(e['alternative']) for e in entries})
                  for ident, entries in candidates.items()}
    contradictions = [{'kind': 'alternative_identity', 'alternative_id': ident, 'fingerprints': fingerprints}
                      for ident, fingerprints in identities.items() if len(fingerprints) != 1]
    if contradictions:
        reasons.append('Un ID local representa alternativas distintas; no se unen archivos ni se prestan recibos')
    normalized_objections = [];questions=[];answers=[];defense_speakers=set();withdrawn=set()
    objection_speakers = set()
    valid_debate_speakers = set()
    final_preferences = {}
    for env in objections:
        if not isinstance(env, dict) or env.get('requested_agent') not in required:
            reasons.append('Objeción sin participante válido'); continue
        requested, actual = env['requested_agent'], env.get('effective_agent')
        if requested in objection_speakers:
            reasons.append('Ronda de objeciones duplicada'); continue
        objection_speakers.add(requested)
        # A substituted debate cannot count as another distinct original opinion.
        participant = next((p for p in available if p['requested_agent'] == requested), None)
        if not participant or actual != participant['effective_agent'] or not env.get('response'):
            reasons.append('Objeciones ausentes o sustitución no independiente: ' + requested); continue
        try: debate = validate_objections(env['response'], known_files)
        except (IpanemaError, TypeError, ValueError):
            reasons.append('Contrato de objeciones inválido: ' + requested); continue
        valid_debate_speakers.add(requested)
        if (context or {}).get('require_defense') and not debate.get('questions'):
            reasons.append('Faltan preguntas concretas de contraste: '+requested)
        for q in debate.get('questions',[]):
            if q['to_agent']not in required or q['to_agent']==requested or q['alternative_id']not in candidates:
                reasons.append('Destinatario/alternativa de pregunta inválido: '+requested);continue
            if set(q['evidence_refs'])-set(ledger):reasons.append('Pregunta con evidencia desconocida: '+requested)
            questions.append({**q,'from_agent':requested,'key':requested+':'+q['id']})
        preferred = debate['preferred_alternative']
        if preferred is not None:
            if preferred not in candidates:
                reasons.append('Preferencia final sobre alternativa desconocida: ' + requested)
            else:
                final_preferences[requested] = preferred
        if debate['decision'] == 'blocked': reasons.append('Contraste bloqueado: ' + requested)
        if debate['decision'] == 'changes_requested' and not debate['objections']:
            reasons.append('Contraste solicita cambios sin objeción verificable: ' + requested)
        for row in debate['objections']:
            if row['alternative_id'] not in candidates and row['alternative_id'] != '*':
                reasons.append('Objeción sobre alternativa desconocida: ' + row['alternative_id'])
            obj = {**row, 'participant': requested, 'effective_agent': actual, 'key': requested + ':' + row['id']}
            fingerprints = identities.get(row['alternative_id'], [])
            receipts = _resolution(ledger, row['alternative_id'], obj['key'], row['resolution_evidence_refs'],
                                   fingerprints[0] if len(fingerprints) == 1 else None)
            obj['resolved_by_controller'] = bool(receipts)
            obj['resolution_receipts'] = receipts
            normalized_objections.append(obj)
    if (context or {}).get('require_objections') and valid_debate_speakers != set(required):
        reasons.append('Falta contraste de objeciones de todos los participantes requeridos')
    if (context or {}).get('require_defense'):
        for env in defenses or []:
            speaker=env.get('requested_agent')
            if speaker not in required or speaker in defense_speakers or env.get('effective_agent')!=speaker or 'response'not in env:
                reasons.append('Defensa ausente/duplicada/no independiente');continue
            try:response=validate_defense(env['response'],known_files,expected_answers={(q['from_agent'],q['id'])for q in questions if q['to_agent']==speaker})
            except (IpanemaError,ValueError,TypeError):reasons.append('Contrato de defensa inválido: '+speaker);continue
            defense_speakers.add(speaker)
            expected={q['key']:q for q in questions if q['to_agent']==speaker};seen_answers=set()
            for answer in response['answers']:
                key=answer['from_agent']+':'+answer['question_id']
                if key not in expected or key in seen_answers:reasons.append('Respuesta sin pregunta asignada: '+speaker);continue
                seen_answers.add(key)
                if set(answer['evidence_refs'])-set(ledger):reasons.append('Defensa con evidencia desconocida: '+speaker)
                answers.append({**answer,'by_agent':speaker,'question_key':key})
                if answer['disposition']=='needs_evidence':reasons.append('Respuesta requiere evidencia: '+key)
            if seen_answers!=set(expected):reasons.append('Preguntas sin contestar: '+speaker)
            if response['preferred_alternative']in candidates:final_preferences[speaker]=response['preferred_alternative']
            else:reasons.append('Defensa prefiere alternativa desconocida: '+speaker)
            if response['decision']=='blocked':reasons.append('Defensa bloqueada: '+speaker)
            own={a['id']for p in available if p['requested_agent']==speaker for a in p['proposal']['analysis']['alternatives']}
            if set(response['withdrawn_alternatives'])-own:reasons.append('No puede retirar alternativas ajenas: '+speaker)
            withdrawn.update(set(response['withdrawn_alternatives'])&own)
            for row in response['objections']:
                if row['alternative_id']not in candidates and row['alternative_id']!='*':reasons.append('Objeción de defensa desconocida')
                normalized_objections.append({**row,'participant':speaker,'effective_agent':speaker,
                    'key':speaker+':defense:'+row['id'],'resolved_by_controller':False,'resolution_receipts':[],'phase':'defense'})
        if defense_speakers!=set(required):reasons.append('Falta defensa de ambos participantes originales')
    debate_requested = bool(objections) or bool((context or {}).get('require_objections'))
    decision_preferences = list(final_preferences.values()) if debate_requested else recommendations
    preferences_complete = (set(final_preferences) == set(required)) if debate_requested else coverage_complete
    unanimous_preference = decision_preferences[0] if (preferences_complete and coverage_complete and
                            len(set(decision_preferences)) == 1) else None
    matrix = []
    eligible = []
    for ident, entries in sorted(candidates.items()):
        fingerprints = identities[ident]
        if len(fingerprints) != 1:
            matrix.append({'alternative_id': ident, 'identity_ambiguous': True,
                           'variants': [{'fingerprint': alternative_fingerprint(e['alternative']),
                                         'participant': e['participant'], 'description': e['alternative']['description'],
                                         'files': e['alternative']['files'], 'tests': e['alternative']['tests']}
                                        for e in entries],
                           'criteria': {k: {'status': 'unknown', 'claimed_statuses': [], 'controller_receipts': []}
                                        for k in CRITERIA},
                           'blocked_by': [], 'needs_evidence': ['Identidad de alternativa ambigua; se requiere nueva evidencia/deliberación'],
                           'eligible': False, 'files': [], 'tests': []})
            continue
        fingerprint = fingerprints[0]
        verdicts, blocked_by, unknown = {}, [], []
        all_refs = set()
        for entry in entries:
            all_refs.update(entry['analysis']['evidence_refs'])
            for criterion in entry['alternative']['constraints'].values(): all_refs.update(criterion['evidence_refs'])
        missing_refs = sorted(all_refs - set(ledger))
        if missing_refs: unknown.append('referencias no comprobadas: ' + ', '.join(missing_refs))
        for criterion in CRITERIA:
            claims = sorted({entry['alternative']['constraints'][criterion]['status'] for entry in entries})
            checks = [r for r in ledger.values() if r.get('kind') == 'constraint' and
                      r.get('subject') == ident and r.get('alternative_sha256') == fingerprint and
                      r.get('constraint') == criterion and r.get('executed') is True]
            failed = [r['id'] for r in checks if r.get('passed') is False]
            passed = [r['id'] for r in checks if _proven(r)]
            conflict = 'fail' in claims and (passed or 'pass' in claims)
            resolution = _resolution(ledger, ident, 'constraint:' + ident + ':' + criterion,
                                     fingerprint=fingerprint) if conflict else []
            status = 'fail' if failed else 'pass' if passed and (not conflict or resolution) else 'unknown'
            verdicts[criterion] = {'status': status, 'claimed_statuses': claims,
                                   'controller_receipts': failed or passed, 'conflict_resolutions': resolution}
            if criterion in mandatory:
                if status == 'fail': blocked_by.append('restricción incumplida: ' + criterion)
                elif status != 'pass': unknown.append('restricción sin comprobar: ' + criterion)
        open_critical = [o['key'] for o in normalized_objections if o['alternative_id'] in (ident, '*') and
                         o['severity'] in ('critical', 'high') and
                         not _resolution(ledger, ident, o['key'], o['resolution_evidence_refs'], fingerprint)]
        if open_critical: blocked_by += ['objeciones críticas abiertas: ' + ', '.join(open_critical)]
        if ident in withdrawn:blocked_by.append('Alternativa retirada por su autor')
        # A hard veto declared by a participant must be resolved rather than
        # ignored because no controller probe was configured.
        declared_failure = [k for k in mandatory if any(e['alternative']['constraints'][k]['status'] == 'fail' for e in entries)
                            and verdicts[k]['status'] != 'pass']
        if declared_failure: blocked_by.append('incumplimiento declarado pendiente: ' + ', '.join(declared_failure))
        row = {'alternative_id': ident, 'fingerprint': fingerprint, 'identity_ambiguous': False,
               'descriptions': list(dict.fromkeys(e['alternative']['description'] for e in entries)),
               'proposed_by': [e['participant'] for e in entries], 'criteria': verdicts,
               'blocked_by': blocked_by, 'needs_evidence': unknown, 'eligible': not blocked_by and not unknown,
               'files': sorted({f for e in entries for f in e['alternative']['files']}),
               'tests': list(dict.fromkeys(t for e in entries for t in e['alternative']['tests']))}
        matrix.append(row)
        if row['eligible']: eligible.append(row)
    selected = None
    if len(eligible) == 1: selected = eligible[0]
    elif eligible:
        # Compare only controller-proven observations. No scores or averages.
        rest = [k for k in CRITERIA if k not in mandatory]
        rank = {'pass': 2, 'unknown': 1, 'fail': 0}
        def dominates(a, b):
            x = [rank[a['criteria'][k]['status']] for k in rest]
            y = [rank[b['criteria'][k]['status']] for k in rest]
            return all(v >= w for v, w in zip(x, y)) and any(v > w for v, w in zip(x, y))
        front = [a for a in eligible if not any(dominates(b, a) for b in eligible if b is not a)]
        if len(front) == 1: selected = front[0]
        elif unanimous_preference is not None:
            selected = next((a for a in front if a['alternative_id'] == unanimous_preference), None)
        if selected is None: reasons.append('Alternativas admisibles sin diferencia objetiva ni recomendación unánime; no elegir por mayoría')
    if not matrix: reasons.append('No hay alternativas válidas para contrastar')
    if selected and reasons: selected = None
    if selected:
        conditions = [{'id': o['key'], 'required': False, 'status': 'pending',
                       'detail': 'Objeción no crítica aceptada solo para implementación local: ' + o['claim']}
                      for o in normalized_objections if o['alternative_id'] in (selected['alternative_id'], '*') and
                      not _resolution(ledger, selected['alternative_id'], o['key'], o['resolution_evidence_refs'], selected['fingerprint'])]
        unmeasured = [k for k in CRITERIA if k not in mandatory and selected['criteria'][k]['status'] == 'unknown']
        conditions += [{'id': 'unmeasured-' + k, 'required': False, 'status': 'pending',
                        'detail': 'Criterio comparativo no medido: ' + k} for k in unmeasured]
        if decision_preferences and (not preferences_complete or
                                     any(p != selected['alternative_id'] for p in decision_preferences)):
            conditions.append({'id': 'preference-disagreement', 'required': False, 'status': 'pending',
                               'detail': 'La decisión sigue restricciones/dominancia comprobadas; '
                                         'no existe consenso completo sobre esta alternativa.'})
        for objection in normalized_objections:
            if objection['alternative_id'] in (selected['alternative_id'], '*'):
                receipts = _resolution(ledger, selected['alternative_id'], objection['key'], objection['resolution_evidence_refs'], selected['fingerprint'])
                objection['resolved_by_controller'] = bool(receipts)
                objection['resolution_receipts'] = receipts
                objection['resolution_scope'] = selected['alternative_id']
        status = 'approved_with_conditions' if conditions else 'approved'
        justification = 'Alternativa admisible tras verificar restricciones obligatorias con recibos del controlador; sin promedio ni voto mayoritario.'
    else:
        conditions = [{'id': row['alternative_id'] + '-evidence-' + str(i), 'required': True,
                       'status': 'pending', 'detail': missing}
                      for row in matrix for i, missing in enumerate(row['needs_evidence'])]
        status = 'blocked' if matrix and all(r['blocked_by'] for r in matrix) else 'needs_evidence'
        justification = ('Deliberación independiente completa; implementación detenida por restricciones sin comprobar u objeciones abiertas.'
                         if coverage_complete and valid_debate_speakers==set(required) and
                            (not (context or {}).get('require_defense') or defense_speakers==set(required)) else
                         'Implementación detenida hasta disponer de evidencia suficiente y deliberación independiente completa.')
    if invalid_receipts: reasons.append('Recibos rechazados por contexto, formato o identidad: ' + ', '.join(invalid_receipts))
    # Invalid ledger material may never silently accompany an approval.
    if invalid_receipts and status.startswith('approved'):
        status, selected = 'needs_evidence', None
    basis = json.dumps({'context': context, 'project': project, 'objective': objective,
                        'proposals': participants, 'matrix': matrix}, ensure_ascii=False, sort_keys=True)
    return {'kind': 'engineering-council-adr', 'version': 1, 'id': 'ADR-' + hashlib.sha256(basis.encode()).hexdigest()[:12],
            'at': now(), 'project': project or (context or {}).get('project'), 'objective': objective,
            'problem': [p['proposal']['analysis']['problem'] for p in available],
            'context': context, 'status': status, 'implementation_allowed': status in ('approved', 'approved_with_conditions'),
            'production_authorized': False, 'approval_scope': 'local_implementation_only',
            'coverage': {'required_agents': required,
                         'participants': [{k: v for k, v in p.items() if k != 'proposal'} for p in participants],
                         'effective_agents': sorted(effective), 'complete': coverage_complete,
                         'objections_complete': valid_debate_speakers == set(required),
                         'deliberation_complete': coverage_complete and valid_debate_speakers==set(required) and
                              (not (context or {}).get('require_defense') or defense_speakers==set(required)),
                         'defense_complete':defense_speakers==set(required) if (context or {}).get('require_defense') else None,
                         'agreement': ('unanimous_preference' if unanimous_preference else 'disagreement')
                                      if coverage_complete and valid_debate_speakers==set(required) and
                                         (not (context or {}).get('require_defense') or defense_speakers==set(required)) else 'incomplete',
                         'consensus': 'complete' if selected and unanimous_preference == selected['alternative_id']
                                      and not any(o['alternative_id'] in (selected['alternative_id'], '*')
                                                  and not o['resolved_by_controller'] for o in normalized_objections)
                                      else 'incomplete_or_disagreement'},
            'proposals': participants, 'objections': normalized_objections, 'matrix': matrix,
            'questions':questions,'answers':answers,'defenses':defenses or [],'withdrawn_alternatives':sorted(withdrawn),
            'contradictions': contradictions,
            'final_preferences': final_preferences,
            'preference_source': 'final_defense' if defense_speakers==set(required) else 'final_debate' if debate_requested else 'independent_proposals',
            'mandatory_constraints': mandatory, 'selected_alternative': selected['alternative_id'] if selected else None,
            'files': selected['files'] if selected else [], 'required_tests': selected['tests'] if selected else [],
            'post_implementation_requirements': [{'test': t, 'phase': 'post_implementation', 'required': True,
                                                 'status': 'pending'} for t in selected['tests']] if selected else [],
            'discarded_alternatives': [r for r in matrix if not selected or r['alternative_id'] != selected['alternative_id']],
            'justification': justification, 'conditions': conditions, 'reasons': list(dict.fromkeys(reasons)),
            'accepted_risks': [risk for p in available for risk in p['proposal']['analysis']['risks']] if selected else [],
            'evidence_receipts': list(ledger.values()),
            'limits': ['Los hashes de fuente no prueban ejecución ni corrección.',
                       'La aprobación del consejo no sustituye QA posterior ni autoriza producción.',
                       'Las opiniones y confidence del modelo no son mediciones.']}
