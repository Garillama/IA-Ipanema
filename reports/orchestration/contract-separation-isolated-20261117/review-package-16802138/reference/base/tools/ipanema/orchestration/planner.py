"""Clasificación explicable y DAG proporcional; reutiliza conocimiento V2."""
from pathlib import PurePosixPath
import re
import uuid

from ..core import IpanemaError, now, read_json
from ..coordinator import route, plan as technical_plan
from ..knowledge import normal


def safe_path(value):
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


def make_plan(project,request,*,files=None,scope='theme',read_only=False,council_mode='auto',council_rounds=2,implementation_agent='codex'):
    if scope not in ('theme','workspace'):raise IpanemaError('Scope no soportado.')
    selection=route(request);knowledge=None;discovery=None
    try:
        discovery=technical_plan(project,request)
        knowledge=discovery['evidence']
    except IpanemaError:pass
    candidates=[x['path'] for x in (knowledge or {}).get('components',[])]
    allowed=list(dict.fromkeys(safe_path(f) for f in (files or (candidates[:1] if scope=='theme' else []))))
    risk=classify(request,allowed);level=int(risk['level'][1]);tasks=[]
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
        tasks.append({'id':ident,'objective':request,'role':role,'agent':agent,'tier':task_tier,'allowed_files':allowed if write else [],
                      'read_files':allowed,'dependencies':dependencies,'tests':['central-qa'],'state':'pending','result':None})
    if level>=3:
        add('architecture','architecture','claude',[])
    if read_only:
        add('audit','audit','codex' if dual else 'commandcode',['architecture'] if level>=3 else [])
    else:
        add('implementation','implementation',implementation_agent,['architecture'] if level>=3 else [],True)
        if level>=2:add('review','review',review_agent,['implementation'])
        if level==4 and not dual:add('independent-review','review',next(a for a in enabled_agents()if a not in (implementation_agent,review_agent)),['implementation'])
    return {'kind':'orchestration-plan','id':'orch-'+uuid.uuid4().hex[:12],'project':project.id,'at':now(),'objective':request,
            'scope':scope,'read_only':read_only,'classification':risk,'skills':selection['skills'],
            'knowledge':knowledge,'candidate_files':candidates,'allowed_files':allowed,'tasks':tasks,
            'required_validation':discovery['required_checks'] if discovery else ['source-investigation'],
            'validation_plan':discovery['tests'] if discovery else ['Comprobar fuente y pruebas del alcance antes de aprobar.'],
            'consumers':discovery['consumers'] if discovery else {},
            'tests':['repo','unit','integration'] if scope=='workspace' else ['source'],
            'integration':'export_diff_only','max_parallel':2,'max_correction_attempts':2,
            'review_policy':{'independent_provider_required':level>=2,'dual_agent':dual,'critical_controller_qa':level==4},
            'council':council_policy,'council_checks':[],
            'council_required_constraints':relevant_constraints(request,scope),
            'limitations':['Candidatos deben comprobarse en fuente actual.','El modelo no eleva permisos ni publica.','Una revisión de IA no sustituye QA ejecutado.']}


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
