from pathlib import Path
import tempfile
import unittest

from tests.support import make_project, put
from ipanema.core import IpanemaError, Project, digest, now
from ipanema.solutions import effective_solutions, register


class SolutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=make_project(Path(self.tmp.name))
        self.project=Project(self.root)
        put(self.root/'tools/example.py','value=1\n')
        self.entry={k:'fixture' for k in ('id','problem','context','component','cause','solution','tests','results','limitations','risks','compatibility','reuse')}
        self.entry.update(scope='workspace',files=['tools/example.py'])
        self.evidence=self.root/'reports/qa.json'
        put(self.evidence,{'kind':'qa','project':'sample','at':now(),'outcome':'passed','checks':[{'name':'test','status':'passed'}],
            'verification_state':{'workspace':{'tools/example.py':digest(self.root/'tools/example.py')}}})

    def tearDown(self):
        self.tmp.cleanup()

    def test_register_and_invalidate_changed_implementation(self):
        register(self.project,self.entry,[self.evidence])
        self.assertEqual(effective_solutions(self.project)[0]['effective_status'],'verified')
        put(self.root/'tools/example.py','value=2\n')
        self.assertEqual(effective_solutions(self.project)[0]['effective_status'],'requires_revalidation')

    def test_no_proof_or_unrelated_hash_is_not_verified(self):
        with self.assertRaises(IpanemaError):register(self.project,self.entry,[])
        put(self.root/'tools/example.py','value=3\n')
        with self.assertRaises(IpanemaError):register(self.project,self.entry,[self.evidence])

    def test_changed_evidence_invalidates_solution(self):
        register(self.project,self.entry,[self.evidence])
        put(self.evidence,{'outcome':'failed'})
        self.assertEqual(effective_solutions(self.project)[0]['effective_status'],'requires_revalidation')

    def test_duplicate_id_does_not_overwrite_history(self):
        register(self.project,self.entry,[self.evidence])
        with self.assertRaises(IpanemaError):register(self.project,self.entry,[self.evidence])

    def test_theme_version_update_invalidates_unchanged_component(self):
        self.entry.update(scope='theme',files=['sections/hero.tpl'])
        self.project.data['remote_observation']={'version':'1.8.0','theme':'ipanema'}
        put(self.evidence,{'kind':'qa','project':'sample','outcome':'passed','at':now(),'checks':[{'name':'test','status':'passed'}],
            'verification_state':{'theme':{'sections/hero.tpl':digest(self.root/'theme/sections/hero.tpl')}}})
        register(self.project,self.entry,[self.evidence])
        self.assertEqual(effective_solutions(self.project)[0]['effective_status'],'verified')
        self.project.data['remote_observation']={'version':'1.9.0','theme':'ipanema'}
        self.assertEqual(effective_solutions(self.project)[0]['effective_status'],'requires_revalidation')
