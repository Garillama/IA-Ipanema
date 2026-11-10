"""Entrada del orquestador. Sin publicación ni integración automática."""
from pathlib import Path
import shutil

from ..core import IpanemaError, Project, now, read_json, write_json
from .planner import make_plan
from .engine import execute,worker


def add_parser(sub):
    parser=sub.add_parser('orchestrate',help='Planificar y ejecutar workers aislados')
    commands=parser.add_subparsers(dest='orchestration_command',required=True)
    commands.add_parser('doctor')
    plan=commands.add_parser('plan');plan.add_argument('request')
    plan.add_argument('--file',action='append');plan.add_argument('--scope',choices=['theme','workspace'],default='theme')
    plan.add_argument('--read-only',action='store_true')
    task=commands.add_parser('task',help='Petición natural: plan y ejecución opcional')
    task.add_argument('request');task.add_argument('--file',action='append');task.add_argument('--scope',choices=['theme','workspace'],default='theme')
    task.add_argument('--read-only',action='store_true');task.add_argument('--execute',action='store_true')
    run=commands.add_parser('run');run.add_argument('plan',type=Path);run.add_argument('--execute',action='store_true')
    status=commands.add_parser('status');status.add_argument('run',type=Path)
    smoke=commands.add_parser('smoke');smoke.add_argument('--agent',choices=['claude','codex','commandcode'],required=True)
    smoke.add_argument('--execute',action='store_true')


def main(project,args):
    from .isolation import probe
    from .recovery import health_check
    op=args.orchestration_command
    if op=='doctor':
        return {'project':project.id,'at':now(),'sandbox':probe(),'runtimes':{name:health_check(name) for name in ('claude','codex','commandcode')},
                'no_unsafe_fallback':True,'production_executor':False},0
    if op in ('plan','task'):
        plan=make_plan(project,args.request,files=args.file,scope=args.scope,read_only=args.read_only)
        path=project.new_run('orchestration-plan')/'plan.json';write_json(path,plan)
        if op=='task' and args.execute:
            result=execute(project,plan,authorize=True)
            return {k:result.get(k) for k in ('run','state','error','patch','original_still_matches','production_modified')},0 if result['state'].startswith('reviewable') else 2
        return {'plan':str(path),'classification':plan['classification'],'skills':plan['skills'],'files':plan['allowed_files'],'tasks':plan['tasks'],'execution_performed':False},0
    if op=='run':
        result=execute(project,read_json(args.plan),authorize=args.execute)
        return {k:result.get(k) for k in ('run','state','error','patch','original_still_matches','production_modified')},0 if result['state'].startswith('reviewable') else 2
    if op=='status':
        result=read_json(args.run/'run.json')
        if result.get('project')!=project.id:raise IpanemaError('Run de otro proyecto.')
        return result,0
    if not args.execute:raise IpanemaError('Smoke realiza inferencia real y requiere --execute; no es simulación.')
    # Deliberately synthetic prompt/file: no store/customer/proprietary code sent.
    from .engine import config
    run=project.new_run('orchestration-smoke');tree=run/'fixture';tree.mkdir();(tree/'fixture.txt').write_text('synthetic fixture; reply approve with no changes\n')
    plan={'scope':'workspace','skills':[],'knowledge':None}
    task={'id':'smoke','objective':'Solo confirma lectura del fixture devolviendo JSON decision approve, summary, evidence y changes vacío.',
          'role':'audit','agent':args.agent,'tier':'fast','read_files':['fixture.txt'],'allowed_files':[]}
    result={'kind':'orchestration-smoke','project':project.id,'at':now(),'task':task,'real_inference_attempted':True,'passed':False}
    try:
        settings=config(project)
        settings['recovery']={**settings.get('recovery',{}),'fallback':False}
        response=worker(project,plan,task,tree,[],settings)
        from .engine import validate_response
        validate_response(task,response,tree)
        result['passed']=response['decision']=='approve';result['response']=response
    except (IpanemaError,OSError,ValueError) as exc:result['error']=str(exc)
    write_json(run/'smoke.json',result)
    return {'report':str(run/'smoke.json'),'agent':args.agent,'passed':result['passed'],'error':result.get('error'),'execution':task.get('execution')},0 if result['passed'] else 2
