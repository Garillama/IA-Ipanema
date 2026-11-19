"""Clasificación explicable y DAG proporcional; reutiliza conocimiento V2."""
from pathlib import PurePosixPath
import re
import uuid
import hashlib
import json

from ..core import IpanemaError, now, read_json
from ..coordinator import route, plan as technical_plan
from ..knowledge import normal


def safe_path(value):
    if not isinstance(value,str):raise IpanemaError('Archivo permitido inválido o privado.')
    p=PurePosixPath(value)
    if not value or not p.parts or p.is_absolute() or '..' in p.parts or '\\' in value or any(part.startswith('.') for part in p.parts):
        raise IpanemaError('Archivo permitido inválido o privado.')
    if p.parts[0] in ('node_modules','projects') or value.endswith(('.pem','.key')):
        raise IpanemaError('No se envían credenciales/configuraciones locales a workers.')
    return p.as_posix()


def classify(request,files=()):
    text=normal(request+' '+' '.join(files))
    critical=[t for t in ('precio','price','stock','inventory','carrito','cart','checkout','cupon','discount','descuento','pago','payment','credencial','autenticacion') if re.search(r'(?<!\w)'+t,text)]
    production=[t for t in ('publicar','publish','deploy','push remoto','sincronizar','watch','produccion') if t in text]
    complex_terms=[t for t in ('arquitectura','migracion','global','compartido','carrusel','carousel','refactor','variante') if t in text]
    specialties=route(request)['skills']
    level=4 if critical or production else 3 if complex_terms or len(files)>3 else 2 if len(specialties)>2 or len(files)>1 else 1
    return {'level':'L'+str(level),'risk':'critical' if level==4 else 'high' if level==3 else 'normal',
            'reasons':critical+production+complex_terms or ['Alcance acotado según petición y archivos'],
            'production_request':bool(production),'independent_review_required':level>=3,
            'method':'Reglas conservadoras revisables; la longitud del diff no reduce riesgo comercial.'}


def relevant_constraints(request,scope):
    # Recomputed by the controller; a saved plan cannot silently remove these.
    if scope=='theme':return ['seo','performance','accessibility','responsive']
    skills=route(request)['skills']
    names={'ipanema-seo-expert':'seo','ipanema-performance':'performance',
           'ipanema-responsive':'responsive','ipanema-visual-qa':'accessibility'}
    return sorted({criterion for skill,criterion in names.items() if skill in skills})


FILE_CONTRACT_VERSION=2


def _file_list(values, label):
    if not isinstance(values, (list, tuple)):
        raise IpanemaError(label+' debe ser una lista de rutas.')
    normalized=[]
    for value in values:
        if not isinstance(value,str):raise IpanemaError(label+' contiene una ruta no textual.')
        path=safe_path(value)
        if path in normalized:raise IpanemaError(label+' contiene rutas duplicadas.')
        normalized.append(path)
    return normalized


def file_contract_projection(plan):
    """Fields that define file authority; intentionally excludes descriptive metadata."""
    tasks=plan.get('tasks',[])
    return {'version':plan.get('file_contract_version'),
            'project':plan.get('project'),'objective':plan.get('objective'),
            'scope':plan.get('scope'),'read_only':plan.get('read_only'),
            'candidate_files':plan.get('candidate_files'),
            'context_files':plan.get('context_files'),
            'write_files':plan.get('write_files'),
            'allowed_files':plan.get('allowed_files'),
            'tasks':[{'id':t.get('id'),'role':t.get('role'),'read_files':t.get('read_files'),
                      'allowed_files':t.get('allowed_files')} for t in tasks]}


def file_contract_sha256(plan):
    raw=json.dumps(file_contract_projection(plan),ensure_ascii=False,sort_keys=True,separators=(',',':'))
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_file_contract(plan, *, allow_legacy=False):
    """Validate explicit candidate/context/write sets; migrate only unambiguous V1 plans."""
    if not isinstance(plan,dict) or type(plan.get('read_only')) is not bool:
        raise IpanemaError('El plan debe declarar read_only como booleano.')
    if not isinstance(plan.get('tasks'),list) or any(not isinstance(task,dict) for task in plan['tasks']):
        raise IpanemaError('El plan debe declarar tareas como lista de objetos.')
    typed=('candidate_files','context_files','write_files')
    present=[key in plan for key in typed]
    if not all(present):
        if any(present) or not allow_legacy:
            raise IpanemaError('Plan de archivos incompleto/obsoleto; vuelve a generarlo.')
        legacy=_file_list(plan.get('allowed_files'), 'allowed_files')
        task_writes=[]
        for task in plan.get('tasks',[]):
            for path in _file_list(task.get('allowed_files',[]),'task.allowed_files'):
                if path not in task_writes:task_writes.append(path)
        if set(task_writes)-set(legacy):raise IpanemaError('El plan legado intenta ampliar archivos modificables.')
        if plan.get('read_only') and (task_writes or any(t.get('role')=='implementation' for t in plan.get('tasks',[]))):
            raise IpanemaError('Plan legado read-only con permisos de escritura; requiere regeneración.')
        plan['candidate_files']=legacy
        plan['context_files']=[]
        plan['write_files']=task_writes
        plan['allowed_files']=legacy
        plan['file_contract_version']=FILE_CONTRACT_VERSION
        plan['file_contract_migration']='legacy-all-allowed-files-as-candidates'
        plan['file_contract_sha256']=file_contract_sha256(plan)
    else:
        if plan.get('file_contract_version')!=FILE_CONTRACT_VERSION:
            raise IpanemaError('Versión de contrato de archivos no soportada; regenera el plan.')
        candidates=_file_list(plan['candidate_files'],'candidate_files')
        context=_file_list(plan['context_files'],'context_files')
        writes=_file_list(plan['write_files'],'write_files')
        if set(candidates)&set(context):raise IpanemaError('candidate_files y context_files deben ser disjuntos.')
        if set(writes)-set(candidates):raise IpanemaError('write_files debe ser subconjunto de candidate_files.')
        union=candidates+context
        if plan.get('allowed_files')!=union:
            raise IpanemaError('allowed_files debe coincidir exactamente con candidate_files + context_files.')
        if plan.get('read_only') and writes:
            raise IpanemaError('Un plan read-only requiere write_files=[].')
        if plan.get('file_contract_sha256')!=file_contract_sha256(plan):
            raise IpanemaError('El contrato de archivos cambió después de planificar; regenera y revisa el alcance.')
    candidates=set(plan['candidate_files']);context=set(plan['context_files']);writes=set(plan['write_files'])
    if plan.get('read_only') and writes:
        raise IpanemaError('Un plan read-only requiere write_files=[].')
    if plan.get('read_only') and any(task.get('role') == 'implementation' for task in plan.get('tasks', [])):
        raise IpanemaError('Un plan read-only no puede incluir tareas de implementación.')
    task_write_union=set()
    for task in plan.get('tasks',[]):
        reads=set(_file_list(task.get('read_files',[]),'task.read_files'))
        task_writes=set(_file_list(task.get('allowed_files',[]),'task.allowed_files'))
        if reads-(candidates|context):raise IpanemaError('Tarea lee archivos fuera de candidate_files/context_files.')
        if task_writes-writes:raise IpanemaError('Tarea amplía write_files.')
        if task.get('role')!='implementation' and task_writes:
            raise IpanemaError('Una tarea no implementadora no puede escribir.')
        if plan.get('read_only') and task_writes:
            raise IpanemaError('Tarea read-only con permisos de escritura.')
        task_write_union.update(task_writes)
    if task_write_union!=writes:
        raise IpanemaError('write_files debe coincidir con la unión de permisos de tareas implementadoras.')
    return plan


def make_plan(project,request,*,files=None,candidate_files=None,context_files=None,write_files=None,
              scope='theme',read_only=False,council_mode='auto',council_rounds=2,implementation_agent='codex'):
    if scope not in ('theme','workspace'):raise IpanemaError('Scope no soportado.')
    selection=route(request);knowledge=None;discovery=None
    try:
        discovery=technical_plan(project,request)
        knowledge=discovery['evidence']
    except IpanemaError:pass
    discovered=[x['path'] for x in (knowledge or {}).get('components',[])]
    if files is not None and candidate_files is not None:
        raise IpanemaError('Usa --file legado o candidate_files, no ambos.')
    candidates=_file_list(candidate_files if candidate_files is not None else
                          files if files is not None else (discovered[:1] if scope=='theme' else []),
                          'candidate_files')
    context=_file_list(context_files or [],'context_files')
    if set(candidates)&set(context):raise IpanemaError('candidate_files y context_files deben ser disjuntos.')
    writes=_file_list(write_files if write_files is not None else ([] if read_only else candidates),'write_files')
    if read_only and writes:raise IpanemaError('Un plan read-only requiere write_files=[].')
    if set(writes)-set(candidates):raise IpanemaError('write_files debe ser subconjunto de candidate_files.')
    all_files=candidates+context
    # Context files are for evidence only; their count must not change candidate risk.
    risk=classify(request,candidates);level=int(risk['level'][1]);tasks=[]
    from .adapters import enabled_agents,require_agent
    require_agent(implementation_agent)
    if implementation_agent not in ('claude','codex'):raise IpanemaError('Implementador debe ser Claude o Codex.')
    dual=len(enabled_agents(project.root))==2
    review_agent=('claude'if implementation_agent=='codex'else'codex')if dual else'commandcode'
    from .council import config_policy
    council_policy=config_policy(risk['level'],mode=council_mode,max_rounds=council_rounds)
    tier='critical' if level==4 else 'strong' if level==3 else 'balanced' if level==2 else 'fast'
    def add(ident,role,agent,dependencies,write=False):
        task_tier='balanced' if role in ('review','audit') and level<3 else tier
        tasks.append({'id':ident,'objective':request,'role':role,'agent':agent,'tier':task_tier,'allowed_files':writes if write else [],
                      'read_files':all_files,'dependencies':dependencies,'tests':['central-qa'],'state':'pending','result':None})
    if level>=3:
        add('architecture','architecture','claude',[])
    if read_only:
        add('audit','audit','codex' if dual else 'commandcode',['architecture'] if level>=3 else [])
    else:
        add('implementation','implementation',implementation_agent,['architecture'] if level>=3 else [],True)
        if level>=2:add('review','review',review_agent,['implementation'])
        if level==4 and not dual:add('independent-review','review',next(a for a in enabled_agents()if a not in (implementation_agent,review_agent)),['implementation'])
    result={'kind':'orchestration-plan','id':'orch-'+uuid.uuid4().hex[:12],'project':project.id,'at':now(),'objective':request,
            'scope':scope,'read_only':read_only,'classification':risk,'skills':selection['skills'],
            'knowledge':knowledge,'candidate_files':candidates,'context_files':context,'write_files':writes,
            'allowed_files':all_files,'file_contract_version':FILE_CONTRACT_VERSION,'tasks':tasks,
            'required_validation':discovery['required_checks'] if discovery else ['source-investigation'],
            'validation_plan':discovery['tests'] if discovery else ['Comprobar fuente y pruebas del alcance antes de aprobar.'],
            'consumers':discovery['consumers'] if discovery else {},
            'tests':['repo','unit','integration'] if scope=='workspace' else ['source'],
            'integration':'export_diff_only','max_parallel':2,'max_correction_attempts':2,
            'review_policy':{'independent_provider_required':level>=2,'dual_agent':dual,'critical_controller_qa':level==4},
            'council':council_policy,'council_checks':[],
            'council_required_constraints':relevant_constraints(request,scope),
            'limitations':['Candidatos deben comprobarse en fuente actual.','El modelo no eleva permisos ni publica.','Una revisión de IA no sustituye QA ejecutado.']}
    result['file_contract_sha256']=file_contract_sha256(result)
    return result


def ready_wave(tasks,completed):
    ready=[t for t in tasks if t['state']=='pending' and set(t['dependencies'])<=completed]
    writes=set()
    for task in ready:
        overlap=writes.intersection(task['allowed_files'])
        if overlap:raise IpanemaError('Solapamiento de escritores en la misma ola: '+','.join(sorted(overlap)))
        writes.update(task['allowed_files'])
    independent=[];reads=set();writes=set()
    for task in ready:
        task_writes=set(task['allowed_files']);task_reads=set(task.get('read_files',[]))
        if task_writes.intersection(reads) or task_reads.intersection(writes):continue
        independent.append(task);writes.update(task_writes);reads.update(task_reads)
    return independent
