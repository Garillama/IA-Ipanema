"""Prefase del controlador existente: workers RO, comprobaciones acotadas y ADR.

No ejecuta comandos sugeridos por modelos ni inicia proveedores/MCP nuevos.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import re
import threading

from ..core import IpanemaError, beneath, digest, now, read_json, write_json
from . import council


class CallBudget:
    def __init__(self, limit):
        if type(limit) is not int or not 1<=limit<=12:raise IpanemaError('Presupuesto del consejo:1–12 llamadas.')
        self.limit=limit;self.used=0;self.lock=threading.Lock()

    def reserve(self):
        with self.lock:
            if self.used>=self.limit:return False
            self.used+=1;return True


def binding(project, plan, tree, run):
    from .adapters import agent_policy
    files={name:digest(tree/name) if (tree/name).is_file() else None for name in plan['allowed_files']}
    return {'project':project.id,'run_id':run.name,
            'source_sha256':hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest(),
            'objective_sha256':hashlib.sha256(plan['objective'].encode()).hexdigest(),'files':files,
            'required_constraints':list(plan.get('council_required_constraints',[])),
            'instructions_sha256':hashlib.sha256(json.dumps(plan.get('_controller_instructions',{}),sort_keys=True).encode()).hexdigest(),
            'require_objections':plan.get('council',{}).get('max_rounds',2)>=2,
            'require_defense':plan.get('council',{}).get('require_defense',False),
            'participation_sha256':hashlib.sha256(json.dumps(agent_policy(),sort_keys=True).encode()).hexdigest()}


def checks(plan, tree, context, baseline, *, phase='before',project=None,alternative_identities=None):
    """Only controller-declared literal/source predicates, never model shell code.

    A receipt states exactly what predicate ran, not universal correctness.
    Source predicates and baseline QA do not prove live SEO, CWV or commerce.
    """
    recipes=plan.get('council_checks',[]) if phase=='before' else plan.get('council_post_checks',[])
    if not isinstance(recipes,list) or len(recipes)>32:raise IpanemaError('Máximo32 comprobaciones declaradas.')
    ledger=[];seen=set()
    for recipe in recipes:
        if not isinstance(recipe,dict):raise IpanemaError('Comprobación del consejo inválida.')
        ident=recipe.get('id','');kind=recipe.get('kind')
        if not re.fullmatch('[a-z][a-z0-9-]{0,63}',ident) or ident in seen:raise IpanemaError('ID de comprobación inválido/repetido.')
        seen.add(ident)
        if kind not in ('file_exists','file_contains','file_not_contains','baseline_qa','qa_report'):
            raise IpanemaError('Comprobación no soportada; no se ejecutan comandos de los modelos.')
        if not isinstance(recipe.get('alternative'),str) or not isinstance(recipe.get('constraint'),str):
            raise IpanemaError('La comprobación debe declarar alternativa y restricción.')
        if kind=='qa_report':
            import datetime as dt
            name=recipe.get('report')
            if project is None or not isinstance(name,str):raise IpanemaError('Reporte QA sin proyecto/ruta.')
            path=project.root/name
            if not beneath(path,project.evidence_root) or any(p.is_symlink() for p in [path,*path.parents] if beneath(p,project.evidence_root)):
                raise IpanemaError('Reporte QA fuera de evidencia autorizada del proyecto.')
            if not path.is_file() or path.stat().st_size>2_000_000:raise IpanemaError('Reporte QA ausente o demasiado grande.')
            report=read_json(path);needed=recipe.get('checks',[])
            if not isinstance(needed,list) or not needed or any(not isinstance(n,str) for n in needed):raise IpanemaError('Declara checks QA concretos.')
            passed_names={c.get('name') for c in report.get('checks',[]) if c.get('status')=='passed'}
            state=report.get('verification_state',{}).get('workspace' if plan['scope']=='workspace' else 'theme',{})
            try:
                age=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(report.get('at','').replace('Z','+00:00'))).total_seconds()
            except (ValueError,TypeError):age=float('inf')
            current_files={f:digest(tree/f) if (tree/f).is_file() else None for f in context['files']}
            passed=(report.get('project')==project.id and report.get('kind')=='qa' and report.get('outcome')=='passed'
                    and 0<=age<=86400 and set(needed)<=passed_names
                    and all(state.get(f)==sha for f,sha in current_files.items()))
            sha=digest(path);scope='Existing dated QA checks only; exact current source hashes, max age24h.'
        elif kind=='baseline_qa':
            passed=baseline.get('executed') is True and baseline.get('passed') is True
            sha=hashlib.sha256(json.dumps(baseline,sort_keys=True).encode()).hexdigest()
            scope='Only the executed baseline QA scope: '+str(baseline.get('kind'))
        else:
            name=recipe.get('file')
            if name not in plan['allowed_files']:raise IpanemaError('Comprobación fuera de archivos autorizados.')
            path=tree/name
            if path.is_symlink():raise IpanemaError('Comprobación no permite symlinks.')
            present=path.is_file();sha=digest(path) if present else hashlib.sha256(b'absent').hexdigest()
            passed=present
            if kind!='file_exists':
                literal=recipe.get('value')
                if not isinstance(literal,str) or not 1<=len(literal)<=500:raise IpanemaError('Predicado literal ausente/excesivo.')
                found=present and literal in path.read_text(encoding='utf-8')
                passed=present and (found if kind=='file_contains' else not found)
            scope='Literal source predicate only; not runtime correctness, indexation or CWV.'
        row={'id':ident,'kind':'resolution' if recipe.get('resolves') else 'constraint',
             'subject':recipe['alternative'],'constraint':recipe['constraint'],'executed':True,'passed':bool(passed),
             'sha256':sha,'context':dict(context),'method':kind,'measurement_scope':scope,'phase':phase}
        row['checked_source_files']={f:digest(tree/f) if (tree/f).is_file() else None for f in context['files']}
        identity=(alternative_identities or {}).get(recipe['alternative'])
        row['alternative_sha256']=identity
        if identity is None:
            row['predicate_passed']=row['passed'];row['passed']=False
            row['identity_status']='missing_or_ambiguous_alternative'
        if recipe.get('resolves'):
            if not isinstance(recipe['resolves'],list) or any(not isinstance(s,str) for s in recipe['resolves']):
                raise IpanemaError('Referencias de objeción inválidas.')
            row['resolves']=recipe['resolves']
        if recipe.get('test') is not None:
            if not isinstance(recipe['test'],str):raise IpanemaError('Referencia de prueba inválida.')
            row['test']=recipe['test']
        ledger.append(row)
    return ledger


def write_adr(run, adr):
    write_json(run/'council/adr.json',adr,overwrite=(run/'council/adr.json').exists())
    lines=['# '+str(adr.get('id','ADR')), '', 'Estado: **'+str(adr.get('status'))+'**', '',
           'Solo decisiones locales; nunca autoriza producción.', '',
           '## Registro verificable', '', '```json', json.dumps(adr,ensure_ascii=False,indent=2),'```']
    (run/'council/ADR.md').write_text('\n'.join(lines)+'\n')


def deliberate(project,plan,snapshot,settings,run,baseline,checkpoint):
    # Import here so the ordinary engine remains the only worker/QA implementation.
    from .engine import worker, git
    from .adapters import enabled_agents,require_agent
    policy=plan['council'];agents=enabled_agents()
    if tuple(policy.get('required_agents',agents))!=agents:raise IpanemaError('Plan de participantes obsoleto/no autorizado; crear plan con política vigente.')
    for a in agents:require_agent(a)
    context=binding(project,plan,snapshot,run)
    budget=CallBudget(settings.get('council_max_calls',len(agents)*(3 if policy.get('require_defense')else 2)));settings['_council_budget']=budget
    directory=run/'council';directory.mkdir(exist_ok=True)
    source_ledger=[{'id':'source:'+name,'kind':'source','subject':name,'executed':True,'passed':sha is not None,
                    'sha256':sha or hashlib.sha256(b'absent').hexdigest(),'context':context,
                    'measurement_scope':'Source existence/hash only, not execution or correctness'} for name,sha in context['files'].items()]
    source_ledger.append({'id':'qa:baseline','kind':'qa','subject':'baseline','executed':baseline.get('executed') is True,
                          'passed':baseline.get('passed') is True,'sha256':hashlib.sha256(json.dumps(baseline,sort_keys=True).encode()).hexdigest(),
                          'context':context,'measurement_scope':baseline.get('kind')})
    metadata={'permissions':{'scope':plan['scope'],'allowed_files':plan['allowed_files'],
                'council_read_only':True,'production_allowed':False,'remote_accounts_used':False,'connection_status':'not_checked'},
              'project':project.id,'source_binding':context,'baseline_qa':baseline,
              'verification_plan':plan.get('council_checks',[]),
              'dependencies':plan.get('consumers',{}),'required_validation':plan.get('required_validation',[]),
              'store_state':{'environment':project.data.get('environment'),'remote_reverified':False},
              'components_available_from_current_sources':context['files'],
              'controller_evidence':source_ledger,
              'version':{'status':'not_available'}}
    manifest=snapshot/'manifest.json'
    if manifest.is_file():
        try:
            values=json.loads(manifest.read_text())
            metadata['version']={k:values.get(k) for k in ('theme','theme_version','forked')}
        except (ValueError,OSError):pass
    proposals=[];objections=[];defenses=[];tasks=[];cached={};cached_debate={};cached_defense={};resuming=(directory/'context.json').exists()
    if resuming:
        if not plan.get('read_only') or read_json(directory/'context.json').get('source_binding')!=context:
            raise IpanemaError('Recuperación solo de lectura con el mismo binding de fuente/objetivo/instrucciones.')
        previous=read_json(directory/'proposals.json') if (directory/'proposals.json').exists() else []
        tasks=read_json(directory/'tasks.json') if (directory/'tasks.json').exists() else []
        from .adapters import validate_schema
        for env in previous:
            if env.get('execution',{}).get('process_reaped') is not True:
                raise IpanemaError('No se acredita salida del proceso anterior; recuperación denegada.')
            if env.get('requested_agent')==env.get('effective_agent') and 'response' in env:
                schema=council.response_schema('council_proposal')
                if 'evidence' not in env['response'] and env.get('execution',{}).get('contract_validation',{}).get('status')=='passed':
                    # v1 normalizer omitted root evidence after native validation. Do not synthesize its lost value.
                    schema['required'].remove('evidence')
                    env['normalization_note']='Legacy controller omitted root evidence; native validation passed. analysis.evidence_refs preserved; omitted value not recreated.'
                validate_schema(env['response'],schema)
                council.validate_proposal(env['response'],plan['allowed_files'])
                cached[env['requested_agent']]=env
        if (directory/'objections.json').exists():
            for env in read_json(directory/'objections.json'):
                if env.get('execution',{}).get('process_reaped') is not True:
                    raise IpanemaError('Contraste anterior sin proceso recogido; recuperación denegada.')
                if env.get('requested_agent')==env.get('effective_agent') and 'response' in env:
                    schema=council.response_schema('council_objection')
                    if 'evidence' not in env['response'] and env.get('execution',{}).get('contract_validation',{}).get('status')=='passed':
                        schema['required'].remove('evidence')
                        env['normalization_note']='Legacy normalizer omitted root evidence after native validation; no values recreated.'
                    validate_schema(env['response'],schema)
                    council.validate_objections(env['response'],plan['allowed_files'])
                    cached_debate[env['requested_agent']]=env
        if (directory/'adr.json').exists():
            old_adr=read_json(directory/'adr.json');budget.used=old_adr.get('worker_attempt_budget',{}).get('used',0)
            if budget.used>=budget.limit:raise IpanemaError('Presupuesto agotado; no se amplía en recuperación.')
            if not (directory/'adr-before-recovery.json').exists():write_json(directory/'adr-before-recovery.json',old_adr)
        if not (directory/'proposals-before-recovery.json').exists():write_json(directory/'proposals-before-recovery.json',previous)
        if (directory/'defenses.json').exists():
            for env in read_json(directory/'defenses.json'):
                if env.get('execution',{}).get('process_reaped')is not True:raise IpanemaError('Defensa anterior sin salida acreditada.')
                if env.get('requested_agent')==env.get('effective_agent') and 'response'in env:
                    validate_schema(env['response'],council.response_schema('council_defense'))
                    try:
                        council.validate_defense(env['response'],plan['allowed_files'],expected_answers=council.assigned_defense_answers(list(cached_debate.values()),env['requested_agent']))
                    except IpanemaError:
                        # Keep the rejected checkpoint; recover only this provider's defense.
                        continue
                    cached_defense[env['requested_agent']]=env
    def collect(agent,round_index,repair_diagnostic=None,defense=False):
        level=plan['classification']['level']
        tier='fast' if level=='L1' else 'balanced' if level=='L2' else 'strong' if level=='L3' else 'critical'
        peers=None if round_index==0 else proposals
        task=council.participant_task(agent,round_index,plan['allowed_files'],tier,plan['objective'],proposals=peers)
        if defense:
            task.update(id='council-defense-'+agent,role='council_defense')
            task['council_context'].update(response_contract=council.contract('council_defense'),
                                           cross_examination=objections,subphase='defense')
        if repair_diagnostic is not None:task['id']+='-retry-1'
        if (run/('worktree-'+task['id'])).exists():task['id']+='-resume-1'
        task['council_context']={**task.get('council_context',{}),'controller_context':metadata}
        if repair_diagnostic is not None:task['council_context']['prior_contract_error']=repair_diagnostic
        # An independent proposal never receives previous DAG results or peer proposals.
        task['state']='running';tasks.append(task)
        tree=run/('worktree-'+task['id'])
        git(snapshot,'worktree','add','-qb',task['id'],str(tree))
        envelope={'requested_agent':agent,'effective_agent':agent,'round':round_index}
        validating=False
        try:
            response=worker(project,plan,task,tree,[],settings)
            if settings['_supervisor'].cancel_event.is_set():raise IpanemaError('Consejo cancelado por denegación.')
            validating=True
            from .adapters import validate_schema
            validate_schema(response,council.response_schema(task['role']))
            normalizer=council.validate_defense if defense else council.validate_proposal if round_index==0 else council.validate_objections
            normalized=normalizer(response,plan['allowed_files'],**({'expected_answers':council.assigned_defense_answers(objections,agent)}if defense else{}))
            task['state']='completed';task['result']=normalized
            envelope['response']=normalized
        except (IpanemaError,OSError,ValueError) as exc:
            task['state']='failed'
            # No raw provider output/error text is exposed here.
            envelope['error']={'category':'invalid_council_contract' if validating else task.get('execution',{}).get('error_category','invalid_contract_or_unavailable'),
                               'summary':'No se recibió una propuesta válida; no cuenta como participación completa.'}
            from .adapters import ResponseContractError
            if isinstance(exc,ResponseContractError):
                envelope['error'].update(category=exc.diagnostic['category'],diagnostic=exc.diagnostic)
            elif validating:
                # Messages from our semantic validator are fixed labels, not raw provider output.
                envelope['error']['semantic_rule']=str(exc)[:180]
        envelope['effective_agent']=task['agent']
        envelope['model']=task.get('model');envelope['execution']=task.get('execution')
        envelope['recovery_attempts']=task.get('recovery_attempts',[])
        task['state']=task.get('state','failed')
        write_json(directory/(task['id']+'.json'),envelope)
        checkpoint()
        category=envelope.get('error',{}).get('category')
        if (repair_diagnostic is None and settings.get('council_contract_retries',1)==1
                and task.get('execution',{}).get('process_reaped') is True
                and category in ('missing_field','schema_type','schema_enum','schema_length','schema_range',
                                 'additional_fields','invalid_council_contract','json_syntax') and budget.used<budget.limit):
            # New inference by the same original provider, not a JSON repair or a replacement vote.
            recovered=collect(agent,round_index,envelope['error'],defense=defense)
            recovered['contract_recovery']=[{'error':envelope['error'],'execution':envelope.get('execution'),
                                            'model':envelope.get('model'),'process_reaped':True}]
            return recovered
        return envelope
    write_json(directory/'context.json',metadata,overwrite=resuming)
    for round_index in range(policy['max_rounds']):
        if round_index and settings['_supervisor'].cancel_event.is_set():break
        # A failed participant does not prevent independent safe tasks from returning.
        preserved=cached if round_index==0 else cached_debate
        with ThreadPoolExecutor(max_workers=min(len(agents),plan.get('max_parallel',2))) as pool:
            future={a:pool.submit(collect,a,round_index) for a in agents if a not in preserved}
            rows=[preserved[a] if a in preserved else future[a].result() for a in agents]
        if round_index==0:proposals=rows
        else:objections=rows
        destination=directory/('proposals.json' if round_index==0 else 'objections.json')
        write_json(destination,rows,overwrite=destination.exists())
        write_json(directory/'tasks.json',tasks,overwrite=(directory/'tasks.json').exists())
        checkpoint()
        # No meaningful debate is possible without any independently valid proposal.
        if not any('response' in row for row in proposals):break
        if round_index==0 and (len({p['effective_agent'] for p in proposals if 'response' in p})<len(agents) or
                              any(p.get('effective_agent')!=p.get('requested_agent') or 'response' not in p for p in proposals)):
            # Do not buy another debate that cannot satisfy independent participation.
            break
    if (policy.get('require_defense') and len(objections)==len(agents) and
            all('response'in e and e['requested_agent']==e['effective_agent']for e in objections)):
        with ThreadPoolExecutor(max_workers=min(len(agents),plan.get('max_parallel',2)))as pool:
            futures={a:pool.submit(collect,a,1,defense=True)for a in agents if a not in cached_defense}
            defenses=[cached_defense[a]if a in cached_defense else futures[a].result()for a in agents]
        write_json(directory/'defenses.json',defenses,overwrite=(directory/'defenses.json').exists())
        write_json(directory/'tasks.json',tasks,overwrite=True);checkpoint()
    identities={}
    for env in proposals:
        for alt in env.get('response',{}).get('analysis',{}).get('alternatives',[]):
            identities.setdefault(alt['id'],set()).add(council.alternative_fingerprint(alt))
    unique={k:next(iter(values)) for k,values in identities.items() if len(values)==1}
    ledger=source_ledger+checks(plan,snapshot,context,baseline,project=project,alternative_identities=unique)
    write_json(directory/'evidence.json',ledger,overwrite=(directory/'evidence.json').exists())
    adr=council.aggregate(proposals,objections,evidence=ledger,required_agents=agents,defenses=defenses,
                          level=plan['classification']['level'],project=project.id,objective=plan['objective'],context=context)
    adr['binding']=context
    adr['alternative_identities']=unique
    adr['worker_attempt_budget']={'limit':budget.limit,'used':budget.used,'includes_retries_and_substitutions':True,
                                 'provider_internal_api_call_count':'not_available'}
    adr['rounds_executed']=1+bool(objections)
    adr['protocol_version']=policy.get('protocol_version',1)
    adr['phases_executed']=['independent_proposals']+(['cross_examination']if objections else[])+(['defense']if defenses else[])
    adr['deliberation_rounds_executed']=int(bool(objections))+int(bool(defenses))
    adr['reused_valid_proposals']=sorted(cached)
    adr['reused_valid_objections']=sorted(cached_debate)
    adr['controller_probes_limit']='Predicates prove only their recorded scope. Stronger claims require appropriate tests; no live SEO/performance certification.'
    write_adr(run,adr)
    return adr
