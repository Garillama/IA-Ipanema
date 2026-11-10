"""Controller evidence and resource limits; fixtures, not Google/model results."""
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest

from tests.support import make_project
from ipanema.core import IpanemaError,Project,digest,now,write_json
from ipanema.orchestration import council_runtime,engine


class Receipts(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='council evidence ')
        self.addCleanup(self.tmp.cleanup)
        self.root=make_project(Path(self.tmp.name),theme=False)
        self.project=Project(self.root)
        (self.root/'copy.txt').write_text('before\n')
        (self.root/'AGENTS.md').write_text('Frozen fixture rules A\n')
        self.plan={'objective':'Inspect a fixture','scope':'workspace','allowed_files':['copy.txt'],'skills':[],
                   'council':{'max_rounds':2},'council_required_constraints':[]}
        self.run=self.project.new_run('fixture')
        self.context=council_runtime.binding(self.project,self.plan,self.root,self.run)
        self.ids={'native':'1'*64}

    def recipes(self,kind='file_contains',**extra):
        self.plan['council_checks']=[{'id':'check-one','kind':kind,'alternative':'native',
                                    'constraint':'functional','file':'copy.txt','value':'before',**extra}]

    def check(self,phase='before'):
        return council_runtime.checks(self.plan,self.root,self.context,{'executed':True,'passed':True},
            phase=phase,project=self.project,alternative_identities=self.ids)[0]

    def test_literal_receipt_exact_source_and_alternative_identity(self):
        self.recipes();row=self.check()
        self.assertTrue(row['passed']);self.assertTrue(row['executed'])
        self.assertEqual(row['context'],self.context)
        self.assertEqual(row['sha256'],digest(self.root/'copy.txt'))
        self.assertEqual(row['alternative_sha256'],self.ids['native'])

    def test_ambiguous_or_missing_identity_cannot_prove_constraint(self):
        self.recipes();self.ids={}
        row=self.check();self.assertTrue(row['predicate_passed']);self.assertFalse(row['passed'])

    def test_no_command_execution_or_path_expansion(self):
        for recipe in ({'kind':'shell','command':'publish'}, {'kind':'file_exists','file':'../private'}):
            self.recipes(**recipe)
            with self.assertRaises(IpanemaError):self.check()

    def make_qa(self):
        report=self.project.new_run('qa')/'report.json'
        write_json(report,{'kind':'qa','project':self.project.id,'at':now(),'outcome':'passed',
                           'checks':[{'name':'unit-tests','status':'passed'}],
                           'verification_state':{'workspace':{'copy.txt':digest(self.root/'copy.txt')}}})
        self.recipes('qa_report',report=str(report.relative_to(self.root)),checks=['unit-tests'])
        return report

    def test_old_baseline_qa_does_not_prove_changed_implementation(self):
        self.make_qa();self.assertTrue(self.check()['passed'])
        self.plan['council_post_checks']=self.plan['council_checks']
        (self.root/'copy.txt').write_text('after\n')
        row=self.check('after');self.assertFalse(row['passed'])
        self.assertEqual(row['checked_source_files']['copy.txt'],digest(self.root/'copy.txt'))

    def test_qa_wrong_project_expired_or_missing_check_fails(self):
        report=self.make_qa();initial=json.loads(report.read_text())
        for change in ({'project':'another'},{'at':(dt.datetime.now(dt.timezone.utc)-dt.timedelta(hours=30)).isoformat()},
                       {'checks':[]}):
            write_json(report,{**initial,**change},overwrite=True)
            self.assertFalse(self.check()['passed'])

    def test_qa_outside_project_evidence_is_rejected(self):
        self.recipes('qa_report',report='AGENTS.md',checks=['unit-tests'])
        with self.assertRaises(IpanemaError):self.check()

    def test_budget_shared_across_concurrent_attempts(self):
        budget=council_runtime.CallBudget(6)
        with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(lambda _:budget.reserve(),range(40)))
        self.assertEqual(sum(results),6);self.assertEqual(budget.used,6)

    def test_council_rules_are_same_despite_original_mutation(self):
        self.plan['_controller_instructions']=engine.instruction_context(self.project,self.plan)
        task={'id':'proposal','role':'council_proposal','read_files':['copy.txt'],'allowed_files':[]}
        a=json.loads(engine.prompt_for(self.project,self.plan,task,self.root,[]))
        (self.root/'AGENTS.md').write_text('Changed fixture rules B\n')
        b=json.loads(engine.prompt_for(self.project,self.plan,task,self.root,[]))
        self.assertEqual(a['rules'],b['rules'])
        self.assertNotEqual(engine.instruction_context(self.project,self.plan),self.plan['_controller_instructions'])

    def test_skill_escape_rejected_before_loading_context(self):
        self.plan['skills']=['../../outside']
        with self.assertRaises(IpanemaError):engine.instruction_context(self.project,self.plan)
