"""Current dual policy. All worker/provider responses here are explicit OFFLINE fixtures."""
import copy,json,subprocess,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tests.support import ROOT,make_project
from ipanema.core import Project,IpanemaError,write_json
from ipanema.orchestration import adapters,council,engine,planner,isolation
from ipanema.orchestration.recovery import Supervisor,WorkerFailure,candidates,health_check
from ipanema.access.policy import Policy
from tests.unit.test_council_policy import proposal,receipts,context

class DualPolicy(unittest.TestCase):
 def test_single_registry_disables_commandcode_without_deleting_it(self):
  p=adapters.agent_policy();self.assertEqual(p['mode'],'dual-agent');self.assertEqual(p['members'],['claude','codex'])
  self.assertEqual(p['disabled'],['commandcode']);self.assertIn('commandcode',adapters.NAMES)
  self.assertIn('commandcode',json.loads((ROOT/'tools/ipanema/orchestration/models.json').read_text())['profiles'])
 def test_disabled_provider_cannot_reach_cli_watchdog_or_health_probe(self):
  with patch('subprocess.Popen')as process,patch('subprocess.run')as run:
   with self.assertRaises(IpanemaError):adapters.argv('commandcode','historical-model')
   with self.assertRaises(IpanemaError):isolation.run_isolated(['/bin/true'],'fixture',ROOT,provider='commandcode')
   self.assertFalse(health_check('commandcode')['enabled']);process.assert_not_called();run.assert_not_called()
 def test_invalid_member_config_fails_closed(self):
  base=json.loads((ROOT/'tools/ipanema/orchestration/models.json').read_text())
  with tempfile.TemporaryDirectory()as folder:
   root=Path(folder);p=root/'tools/ipanema/orchestration/models.json';p.parent.mkdir(parents=True)
   for change in ({'members':['claude','codex','commandcode']},{'members':['codex']},{'disabled':[]},{'production_requires_human_authorization':False}):
    value=copy.deepcopy(base);value['council'].update(change);write_json(p,value,overwrite=True)
    with self.assertRaises(IpanemaError):adapters.agent_policy(root)
 def test_no_new_or_existing_active_mcp_grant_for_disabled_agent(self):
  with tempfile.TemporaryDirectory()as folder:
   project=Project(make_project(Path(folder),theme=False));policy=Policy(project)
   with self.assertRaises(IpanemaError):policy.issue('commandcode','fixture',['devtools.read'],allow_network=True)
   grant=policy.issue('claude','fixture',['devtools.read'],allow_network=True)
   grant['agent']='commandcode';policy.save(grant)
   with self.assertRaises(IpanemaError):policy.load(grant['id'])
   self.assertEqual(policy.load(grant['id'],active=False)['agent'],'commandcode')
 def test_planner_and_reversed_roles_have_external_reviewer(self):
  with tempfile.TemporaryDirectory()as folder:
   project=Project(make_project(Path(folder),theme=False))
   for primary in ['claude','codex']:
    for request in ['Ajuste de etiquetas compartido','Corregir presentación de carrito']:
     p=planner.make_plan(project,request,files=['a.txt'],scope='workspace',implementation_agent=primary)
     self.assertFalse(any(t['agent']=='commandcode'for t in p['tasks']))
     impl=next(t for t in p['tasks']if t['role']=='implementation');review=next(t for t in p['tasks']if t['role']=='review')
     self.assertEqual(impl['agent'],primary);self.assertNotEqual(impl['agent'],review['agent'])
     self.assertEqual(p['council']['required_agents'],['claude','codex'])
 def test_failover_is_only_peer_and_never_a_self_reviewer(self):
  task={'id':'audit','role':'audit','agent':'claude','tier':'fast','dependencies':[]}
  supervisor=Supervisor({'recovery':{'max_retries':0}});seen=[]
  def invoke():
   seen.append(task['agent']);task['execution']={'process_reaped':True,'context_complete':True,'prompt_sha256':'a'*64}
   if task['agent']=='claude':raise WorkerFailure('authentication',reaped=True)
   return {'decision':'approve','changes':[]}
  with patch('ipanema.orchestration.recovery.shutil.which',return_value='/fixture'):
   supervisor.run({'tasks':[task],'classification':{'level':'L1'}},task,invoke)
  self.assertEqual(seen,['claude','codex'])
  impl={'id':'implementation','role':'implementation','agent':'codex','dependencies':[]}
  reviewer={'id':'review','role':'review','agent':'claude','dependencies':['implementation']}
  p={'tasks':[impl,reviewer],'classification':{'level':'L2'},'read_only':False}
  self.assertEqual(candidates(p,impl),[]);self.assertEqual(candidates(p,reviewer),[])
 def test_disabled_assignment_rejected_before_any_model(self):
  with tempfile.TemporaryDirectory()as folder:
   project=Project(make_project(Path(folder),theme=False));(project.root/'AGENTS.md').write_text('Fixture')
   p=planner.make_plan(project,'Corrige texto',files=['a.txt'],scope='workspace')
   p['tasks'][0]['agent']='commandcode'
   with patch.object(engine,'central_qa')as qa:
    with self.assertRaises(IpanemaError):engine.execute(project,p,authorize=True)
    qa.assert_not_called()
 def test_l2_cannot_omit_reviewer_from_received_plan(self):
  with tempfile.TemporaryDirectory()as folder:
   project=Project(make_project(Path(folder),theme=False))
   p=planner.make_plan(project,'Ajuste compartido',files=['a.txt'],scope='workspace')
   p['classification']['level']='L2';p['tasks']=[t for t in p['tasks']if t['role']!='review']
   with patch.object(engine,'central_qa')as qa:
    with self.assertRaisesRegex(IpanemaError,'revisiones independientes'):engine.execute(project,p,authorize=True)
    qa.assert_not_called()
 def test_native_schema_rejects_invalid_alternative_id_at_exact_path(self):
  schema=council.response_schema('council_proposal');value=copy.deepcopy(council.dual_contract('council_proposal')['example'])
  value['analysis']['alternatives'][0]['id']='Invalid_id'
  with self.assertRaises(adapters.ResponseContractError)as caught:adapters.validate_schema(value,schema)
  self.assertEqual(caught.exception.diagnostic,{'category':'schema_pattern','path':'$.analysis.alternatives[0].id'})
 def test_native_proposal_requires_nonempty_acceptance_tests(self):
  schema=council.response_schema('council_proposal');value=copy.deepcopy(council.dual_contract('council_proposal')['example'])
  for path in ['analysis','alternative']:
   bad=copy.deepcopy(value)
   (bad['analysis']if path=='analysis'else bad['analysis']['alternatives'][0])['tests']=[]
   with self.assertRaises(adapters.ResponseContractError)as caught:adapters.validate_schema(bad,schema)
   self.assertEqual(caught.exception.diagnostic['category'],'schema_length')
 def test_legacy_local_overrides_cannot_enable_members(self):
  with tempfile.TemporaryDirectory()as folder:
   project=Project(make_project(Path(folder),theme=False))
   write_json(project.root/'.local/orchestration.json',{'council':{'members':['commandcode']}})
   with self.assertRaises(IpanemaError):engine.config(project)

class DualDecision(unittest.TestCase):
 def setUp(self):
  self.ctx=context(files=['fixture.txt'],require_objections=True,require_defense=True)
  self.props=[proposal('claude'),proposal('codex')];self.probes=receipts(self.ctx)
  self.cross=[];self.defense=[]
  for who,other in [('claude','codex'),('codex','claude')]:
   q=copy.deepcopy(council.contract('council_objection')['example']);q['objections']=[]
   q['questions']=[{'id':'Q1','to_agent':other,'alternative_id':'native','question':'How does the executed fixture check establish this contract?','evidence_refs':['check-native-functional']}]
   self.cross.append({'requested_agent':who,'effective_agent':who,'response':q})
   a=copy.deepcopy(council.contract('council_defense')['example']);a['objections']=[]
   a['answers']=[{'question_id':'Q1','from_agent':other,'answer':'Executed controller fixture receipt, no claim about production.','evidence_refs':['check-native-functional'],'disposition':'defend'}]
   self.defense.append({'requested_agent':who,'effective_agent':who,'response':a})
 def decide(self,**kwargs):
  return council.aggregate(kwargs.get('proposals',self.props),kwargs.get('objections',self.cross),
   evidence=kwargs.get('evidence',self.probes),defenses=kwargs.get('defenses',self.defense),context=self.ctx,project='fixture',objective='Fixture')
 def test_two_proposals_questions_answers_and_approval_require_evidence(self):
  a=self.decide();self.assertTrue(a['coverage']['deliberation_complete']);self.assertTrue(a['coverage']['defense_complete'])
  self.assertEqual(len(a['questions']),2);self.assertEqual(len(a['answers']),2);self.assertTrue(a['implementation_allowed'])
  self.assertFalse(a['production_authorized'])
 def test_missing_agent_or_defense_blocks_major_approval(self):
  for args in [{'proposals':self.props[:1]},{'defenses':self.defense[:1]},{'objections':self.cross[:1]}]:
   with self.subTest(args=args):
    a=self.decide(**args);self.assertFalse(a['implementation_allowed']);self.assertFalse(a['coverage']['deliberation_complete'])
 def test_insufficient_evidence_never_becomes_an_approval(self):
  self.assertFalse(self.decide(evidence=[])['implementation_allowed'])
 def test_unanswered_or_invented_question_rejected(self):
  for responses in [[],[{'question_id':'invented','from_agent':'codex','answer':'Fixture','evidence_refs':[],'disposition':'defend'}]]:
   d=copy.deepcopy(self.defense);d[0]['response']['answers']=responses
   result=self.decide(defenses=d);self.assertFalse(result['implementation_allowed'])
   self.assertFalse(result['coverage']['defense_complete']);self.assertFalse(result['coverage']['deliberation_complete'])
 def test_critical_objection_cannot_be_resolved_by_model_defense(self):
  c=copy.deepcopy(self.cross);c[0]['response']['objections']=[{'id':'CRIT','alternative_id':'native','category':'security','severity':'critical','claim':'Fixture missing security guarantee','evidence_refs':['check-native-functional'],'resolution_evidence_refs':[],'status':'resolved'}]
  self.assertFalse(self.decide(objections=c)['implementation_allowed'])
 def test_objective_comparison_can_override_different_preferences(self):
  props=[proposal('claude'),proposal('codex',alternative='other')]
  c=copy.deepcopy(self.cross);d=copy.deepcopy(self.defense)
  c[0]['response']['preferred_alternative']='other';d[0]['response']['preferred_alternative']='other'
  a=self.decide(proposals=props,objections=c,defenses=d)
  self.assertEqual(a['selected_alternative'],'native');self.assertTrue(a['implementation_allowed'])
 def test_invalid_contract_not_repaired(self):
  d=copy.deepcopy(self.defense);del d[0]['response']['answers']
  self.assertFalse(self.decide(defenses=d)['implementation_allowed'])

class DualRuntime(unittest.TestCase):
 def test_frozen_council_prompt_keeps_original_participant_identity(self):
  with tempfile.TemporaryDirectory()as folder:
   root=make_project(Path(folder),theme=False);(root/'AGENTS.md').write_text('Offline identity fixture')
   project=Project(root);plan={'scope':'workspace','skills':[],'knowledge':None}
   for agent in ['claude','codex']:
    task=council.participant_task(agent,0,['a.txt'],'balanced','Read only fixture')
    def invoke(*args,**kwargs):
     packet=json.loads(kwargs['frozen_prompt']);self.assertEqual(packet['agent'],agent)
     self.assertNotIn('peer_proposals',packet);return {'decision':'proposed','changes':[]}
    with patch.object(Supervisor,'run',side_effect=lambda p,t,call,checkpoint=None:call()),patch.object(engine,'_worker_once',side_effect=invoke):
     engine.worker(project,plan,task,root,[],{})
 def test_actual_git_pipeline_preserves_independence_and_routes_questions_to_defense(self):
  with tempfile.TemporaryDirectory()as folder:
   root=make_project(Path(folder),theme=False);(root/'AGENTS.md').write_text('Read only offline fixture')
   (root/'copy.txt').write_text('native fixture contract')
   for args in [['init','-q'],['add','.'],['-c','user.name=Fixture','-c','user.email=fixture@invalid','commit','-qm','fixture']]:
    subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
   project=Project(root);plan=planner.make_plan(project,'Audita componente compartido',files=['copy.txt'],scope='workspace',read_only=True)
   calls=[]
   def worker(project,plan,task,tree,history,settings):
    calls.append((task['role'],task['agent']))
    task['execution']={'process_reaped':True,'contract_validation':{'status':'passed'}}
    r=copy.deepcopy(council.contract(task['role'])['example']);r['objections']=[] if task['role']!='council_proposal'else r.get('objections',[])
    if task['role']=='council_proposal':
     r.pop('objections',None);self.assertEqual(history,[]);self.assertNotIn('peer_proposals',json.loads(engine.prompt_for(project,plan,task,tree,history)))
     r['analysis']['files']=['copy.txt'];r['analysis']['alternatives'][0]['files']=['copy.txt']
    elif task['role']=='council_objection':
     peer='codex'if task['agent']=='claude'else'claude';r['questions']=[{'id':'Q','to_agent':peer,'alternative_id':'native','question':'What does this exact source establish?','evidence_refs':['source:copy.txt']}]
    else:
     incoming=[(e['requested_agent'],q)for e in task['council_context']['cross_examination']for q in e['response']['questions']if q['to_agent']==task['agent']]
     r['answers']=[{'question_id':q['id'],'from_agent':sender,'answer':'The fixture proves source identity only.','evidence_refs':['source:copy.txt'],'disposition':'needs_evidence'}for sender,q in incoming]
    return r
   baseline={'executed':True,'passed':True,'kind':'offline fixture'}
   run=project.new_run('dual-fixture')
   with patch.object(engine,'worker',side_effect=worker):
    a=engine.run_council(project,plan,root,{'council_contract_retries':0},run,baseline,lambda:None)
   self.assertEqual(len(calls),6);self.assertTrue(a['coverage']['deliberation_complete'])
   self.assertFalse(a['implementation_allowed']);self.assertEqual(a['phases_executed'],['independent_proposals','cross_examination','defense'])
   self.assertNotIn('commandcode',[agent for _,agent in calls]);self.assertEqual((root/'copy.txt').read_text(),'native fixture contract')
   # Recovery must reuse five valid nodes and replace only a defense of wrong questions.
   path=run/'council/defenses.json';saved=json.loads(path.read_text())
   saved[0]['response']['answers'][0]['question_id']='wrong-recipient-question'
   write_json(path,saved,overwrite=True);calls.clear()
   with patch.object(engine,'worker',side_effect=worker):
    recovered=engine.run_council(project,plan,root,{'council_contract_retries':0,'council_max_calls':8},run,baseline,lambda:None)
   self.assertEqual(calls,[('council_defense','claude')]);self.assertTrue(recovered['coverage']['deliberation_complete'])

