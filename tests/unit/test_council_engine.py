"""Council boundaries with explicit MOCK workers; Git/snapshots are real.

These cases prove controller behavior, not provider quality or account access.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tests.support import make_project
from ipanema.core import IpanemaError, Project, digest
from ipanema.orchestration import engine, planner


class CouncilEngine(unittest.TestCase):
    def setUp(self):
        from tests.support import historical_trio_policy
        historical_trio_policy(self)
        self.tmp = tempfile.TemporaryDirectory(prefix="council controller fixture ")
        self.root = make_project(Path(self.tmp.name), theme=False)
        (self.root / "AGENTS.md").write_text("Synthetic fixture. No production mutations.\n")
        (self.root / "copy.txt").write_text("before\n")
        self.project = Project(self.root)
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "Synthetic baseline")
        self.head = self.git("rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        run = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True, timeout=20,
                             env=engine.git_environment())
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout.strip()

    def plan(self, *, read_only=False):
        return planner.make_plan(self.project, "Revisa componente compartido", files=["copy.txt"],
                                 scope="workspace", read_only=read_only)

    @staticmethod
    def qa(*args):
        return {"name": "central-qa", "executed": True, "passed": True,
                "kind": "synthetic-controller-fixture", "mock": True, "exit_code": 0}

    @staticmethod
    def adr(status="approved"):
        return {"id": "ADR-synthetic", "status": status, "implementation_allowed": status == "approved",
                "selected_alternative": "native", "conditions": [], "required_tests": [],
                "allowed_files": ["copy.txt"], "files": ["copy.txt"], "matrix": [], "proposals": [], "objections": [], "project": "sample"}

    def controller_adr(self, value=None):
        """A fixture ADR is bound by the same controller function as real runs."""
        def issue(project, plan, tree, settings, run, *args):
            from ipanema.orchestration.council_runtime import binding
            result = deepcopy(self.adr() if value is None else value)
            result["binding"] = binding(project, plan, tree, run)
            return result
        return issue

    @staticmethod
    def mock_response(task):
        from ipanema.orchestration import council
        response = deepcopy(council.contract(task["role"])["example"])
        response["summary"] = "Synthetic " + task["agent"]
        if task["role"] == "council_proposal":
            response["analysis"]["problem"] = "UNSHARED_FIXTURE_SOLUTION_" + task["agent"]
            response["analysis"]["files"] = ["copy.txt"]
            response["analysis"]["alternatives"][0]["files"] = ["copy.txt"]
        else:
            response["objections"] = []
        return response

    def test_first_round_has_no_peer_history_and_no_writer_permissions(self):
        from ipanema.orchestration import council
        calls = []
        initial = (self.root / "copy.txt").read_bytes()

        def worker(project, plan, task, tree, history, settings):
            calls.append((task["role"], task["agent"], deepcopy(history), deepcopy(task)))
            self.assertEqual(task["allowed_files"], [])
            if task["role"] == "council_proposal":
                self.assertEqual(history, [])
                prompt = engine.prompt_for(project, plan, task, tree, history)
                self.assertNotIn("UNSHARED_FIXTURE_SOLUTION_", prompt)
                self.assertIn("analysis COMPLETO", json.loads(prompt)["instruction"])
            elif task["role"] == "council_objection":
                prompt = engine.prompt_for(project, plan, task, tree, history)
                for agent in ("claude", "codex", "commandcode"):
                    self.assertIn("UNSHARED_FIXTURE_SOLUTION_" + agent, prompt)
            return self.mock_response(task)

        with patch.object(engine, "worker", side_effect=worker), \
             patch.object(council, "aggregate", return_value=self.adr()):
            result = engine.run_council(self.project, self.plan(read_only=True), self.root,
                                        {}, self.project.new_run("council-unit"), self.qa(), lambda: None)
        first = [entry for entry in calls if entry[0] == "council_proposal"]
        self.assertEqual({entry[1] for entry in first}, {"claude", "codex", "commandcode"})
        self.assertEqual(len(first), 3)
        self.assertEqual(len([entry for entry in calls if entry[0] == "council_objection"]), 3)
        self.assertLessEqual(len(calls), 6)
        self.assertEqual(result["status"], "approved")
        self.assertEqual((self.root / "copy.txt").read_bytes(), initial)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.head)

    def test_invalid_analysis_is_not_misreported_as_authentication_failure(self):
        def worker(project, plan, task, tree, history, settings):
            if task['agent']=='codex':
                return {'decision':'approve','summary':'Mock base JSON only','changes':[],'evidence':[]}
            return self.mock_response(task)
        run=self.project.new_run('council-invalid-contract-unit')
        with patch.object(engine,'worker',side_effect=worker):
            result=engine.run_council(self.project,self.plan(read_only=True),self.root,{},run,self.qa(),lambda:None)
        rows=json.loads((run/'council/proposals.json').read_text())
        failed=next(row for row in rows if row['requested_agent']=='codex')
        self.assertEqual(failed['error']['category'],'missing_field')
        self.assertEqual(failed['error']['diagnostic']['path'],'$.analysis')
        self.assertFalse(result['implementation_allowed'])

    def test_readonly_recovery_reuses_completed_original_proposals_and_contrast(self):
        calls=[];fail=True
        def worker(project,plan,task,tree,history,settings):
            calls.append((task['role'],task['agent']))
            task['execution']={'process_reaped':True,'contract_validation':{'status':'passed'}}
            if fail and task['role']=='council_objection' and task['agent']=='commandcode':
                raise IpanemaError('Synthetic failed contrast; no real provider')
            return self.mock_response(task)
        plan=self.plan(read_only=True);run=self.project.new_run('council-resume-unit')
        with patch.object(engine,'worker',side_effect=worker):
            first=engine.run_council(self.project,plan,self.root,{},run,self.qa(),lambda:None)
            self.assertFalse(first['coverage']['objections_complete'])
            fail=False
            second=engine.run_council(self.project,plan,self.root,{},run,self.qa(),lambda:None)
        self.assertEqual(len(calls),7)
        self.assertEqual(calls[-1],('council_objection','commandcode'))
        self.assertEqual(second['reused_valid_proposals'],['claude','codex','commandcode'])
        self.assertEqual(second['reused_valid_objections'],['claude','codex'])
        self.assertTrue(second['coverage']['objections_complete'])

    def test_readonly_recovery_rejects_changed_source_binding(self):
        def worker(project,plan,task,tree,history,settings):
            task['execution']={'process_reaped':True}
            return self.mock_response(task)
        plan=self.plan(read_only=True);run=self.project.new_run('council-resume-drift-unit')
        with patch.object(engine,'worker',side_effect=worker):
            engine.run_council(self.project,plan,self.root,{},run,self.qa(),lambda:None)
            (self.root/'copy.txt').write_text('changed fixture source\n')
            with self.assertRaises(IpanemaError):engine.run_council(self.project,plan,self.root,{},run,self.qa(),lambda:None)

    def test_blocked_adr_stops_implementation_before_any_patch(self):
        plan = self.plan()
        calls = []
        with patch.object(engine, "run_council", side_effect=lambda *a, **k: self.adr("blocked")), \
             patch.object(engine, "worker", side_effect=lambda *a: calls.append(a)), \
             patch.object(engine, "central_qa", side_effect=self.qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, plan, authorize=True)
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(calls, [])
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.head)

    def test_missing_participant_is_preserved_as_missing_not_unanimous(self):
        calls = []

        def worker(project, plan, task, tree, history, settings):
            calls.append((task["role"], task["agent"]))
            if task["agent"] == "claude":
                raise IpanemaError("Synthetic unavailable provider; not real inference")
            return self.mock_response(task)

        with patch.object(engine, "worker", side_effect=worker):
            result = engine.run_council(self.project, self.plan(read_only=True), self.root,
                                        {}, self.project.new_run("council-missing-unit"), self.qa(), lambda: None)
        self.assertFalse(result["coverage"]["complete"])
        available = [item for item in result["coverage"]["participants"] if item["status"] == "available"]
        self.assertEqual({item["effective_agent"] for item in available}, {"codex", "commandcode"})
        self.assertFalse(result["implementation_allowed"])
        self.assertNotEqual(result["coverage"]["consensus"], "complete")
        self.assertTrue(any(agent == "codex" for _, agent in calls))
        self.assertTrue(any(agent == "commandcode" for _, agent in calls))

    def test_failover_to_same_provider_does_not_create_third_opinion(self):
        def worker(project, plan, task, tree, history, settings):
            if task["agent"] == "claude":
                task["assigned_agent"] = "claude"
                task["agent"] = "codex"
            return self.mock_response(task)

        with patch.object(engine, "worker", side_effect=worker):
            result = engine.run_council(self.project, self.plan(read_only=True), self.root,
                                        {}, self.project.new_run("council-duplicate-unit"), self.qa(), lambda: None)
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(set(result["coverage"]["effective_agents"]), {"codex", "commandcode"})
        self.assertFalse(result["implementation_allowed"])

    def test_deliberation_cannot_smuggle_an_implementation_patch(self):
        def worker(project, plan, task, tree, history, settings):
            response = self.mock_response(task)
            if task["role"] == "council_proposal" and task["agent"] == "claude":
                response["changes"] = [{"path": "copy.txt", "before_sha256": digest(tree / "copy.txt"),
                                        "content": "unauthorized council write\n"}]
            return response

        with patch.object(engine, "worker", side_effect=worker):
            result = engine.run_council(self.project, self.plan(read_only=True), self.root,
                                        {}, self.project.new_run("council-no-write-unit"), self.qa(), lambda: None)
        participant = next(item for item in result["coverage"]["participants"] if item["requested_agent"] == "claude")
        self.assertNotEqual(participant["status"], "available")
        self.assertFalse(result["implementation_allowed"])
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_needs_evidence_and_conditions_are_not_unconditional_write_permission(self):
        cases = [("needs_evidence", ["Unexecuted browser measurement"]),
                 ("approved_with_conditions", ["Unexecuted browser measurement"]),
                 ("approved_with_conditions", [{"required": True, "status": "pending", "detail": "Browser measurement"}])]
        for status, conditions in cases:
            with self.subTest(status=status, conditions=conditions):
                adr = self.adr(status)
                adr["conditions"] = conditions
                if status == "approved_with_conditions":
                    # A contradictory allow flag cannot override pending conditions.
                    adr["implementation_allowed"] = True
                with patch.object(engine, "run_council", side_effect=self.controller_adr(adr)), \
                     patch.object(engine, "worker") as worker, \
                     patch.object(engine, "central_qa", side_effect=self.qa), \
                     patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
                    result = engine.execute(self.project, self.plan(), authorize=True)
                self.assertEqual(result["state"], "blocked")
                worker.assert_not_called()
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_approval_without_controller_binding_is_rejected(self):
        with patch.object(engine, "run_council", return_value=self.adr()), \
             patch.object(engine, "worker") as worker, \
             patch.object(engine, "central_qa", side_effect=self.qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, self.plan(), authorize=True)
        self.assertEqual(result["state"], "blocked")
        self.assertIn("binding", result.get("error", ""))
        worker.assert_not_called()
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_no_change_claim_does_not_skip_mandatory_post_checks(self):
        from ipanema.orchestration.council import alternative_fingerprint
        plan = self.plan()
        plan["council_post_checks"] = [{"id": "after-check", "kind": "file_contains", "file": "copy.txt",
                                         "value": "after", "alternative": "native", "constraint": "functional"}]
        adr = self.adr()
        alt = self.mock_response({"role": "council_proposal", "agent": "codex"})["analysis"]["alternatives"][0]
        adr["alternative_identities"] = {"native": alternative_fingerprint(alt)}

        def worker(project, plan, task, tree, history, settings):
            return {"decision": "proposed", "summary": "Synthetic claim already fixed", "changes": [], "evidence": []}

        with patch.object(engine, "run_council", side_effect=self.controller_adr(adr)), \
             patch.object(engine, "worker", side_effect=worker), \
             patch.object(engine, "central_qa", side_effect=self.qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, plan, authorize=True)
        self.assertEqual(result["state"], "blocked")
        receipt = result["council_post_checks"][0]
        self.assertEqual(receipt["method"], "file_contains")
        self.assertFalse(receipt["passed"])
        self.assertNotIn("identity_status", receipt)
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_real_policy_and_bound_receipts_allow_change_but_reject_noop(self):
        from ipanema.orchestration.council import CRITERIA
        for implement in (False, True):
            with self.subTest(implement=implement):
                plan = self.plan()
                plan["max_correction_attempts"] = 0
                # Each synthetic constraint in this fixture is deliberately the
                # same literal predicate. Receipts state that limited scope.
                plan["council_checks"] = [
                    {"id": "before-" + criterion.replace("_", "-"), "kind": "file_contains",
                     "file": "copy.txt", "value": "before", "alternative": "native", "constraint": criterion}
                    for criterion in CRITERIA]
                plan["council_post_checks"] = [
                    {"id": "after-check", "kind": "file_contains", "file": "copy.txt", "value": "after",
                     "alternative": "native", "constraint": "functional", "test": "check-after"}]

                def worker(project, plan, task, tree, history, settings):
                    if task["role"] in ("council_proposal", "council_objection"):
                        response = self.mock_response(task)
                        if task["role"] == "council_proposal":
                            response["analysis"]["tests"] = ["check-after"]
                            response["analysis"]["alternatives"][0]["tests"] = ["check-after"]
                        return response
                    if task["role"] == "implementation":
                        changes = ([{"path": "copy.txt", "before_sha256": digest(tree / "copy.txt"),
                                     "content": "after\n"}] if implement else [])
                        return {"decision": "proposed", "summary": "Synthetic implementation", "changes": changes}
                    return {"decision": "approve", "summary": "Synthetic independent reviewer", "changes": []}

                with patch.object(engine, "worker", side_effect=worker), \
                     patch.object(engine, "central_qa", side_effect=self.qa), \
                     patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
                    result = engine.execute(self.project, plan, authorize=True)
                self.assertEqual(result["council"]["status"], "approved")
                self.assertTrue(result["council"]["coverage"]["complete"])
                self.assertEqual(result["state"].startswith("reviewable"), implement, result.get("error"))
                self.assertEqual(result["council_post_checks"][0]["passed"], implement)
                self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_qa_rejects_proposal_even_if_council_approved(self):
        plan = self.plan()
        plan["max_correction_attempts"] = 0
        qa_calls = []

        def qa(project, plan, tree, settings):
            qa_calls.append((tree / "copy.txt").read_text())
            return {**self.qa(), "passed": len(qa_calls) == 1}

        def worker(project, plan, task, tree, history, settings):
            if task["role"] == "implementation":
                return {"decision": "proposed", "summary": "Synthetic faulty edit", "changes": [
                    {"path": "copy.txt", "before_sha256": digest(tree / "copy.txt"), "content": "broken\n"}]}
            return {"decision": "approve", "summary": "Synthetic reviewer", "changes": [], "evidence": []}

        with patch.object(engine, "run_council", side_effect=self.controller_adr()), \
             patch.object(engine, "worker", side_effect=worker), \
             patch.object(engine, "central_qa", side_effect=qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, plan, authorize=True)
        self.assertEqual(result["state"], "blocked")
        self.assertIn("broken\n", qa_calls)
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.head)

    def test_optional_unknown_cost_does_not_block_local_work(self):
        adr = self.adr("approved_with_conditions")
        adr["implementation_allowed"] = True
        adr["conditions"] = [{"required": False, "status": "unknown", "detail": "Monetary cost unavailable"}]

        def worker(project, plan, task, tree, history, settings):
            return {"decision": "approve" if task["role"] == "review" else "proposed",
                    "summary": "Synthetic no-change result", "changes": [], "evidence": []}

        with patch.object(engine, "run_council", side_effect=self.controller_adr(adr)), \
             patch.object(engine, "worker", side_effect=worker), \
             patch.object(engine, "central_qa", side_effect=self.qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, self.plan(), authorize=True)
        self.assertTrue(result["state"].startswith("reviewable"), result.get("error"))
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_snapshot_drift_invalidates_decision_before_implementation(self):
        def council(project, plan, snapshot, *args):
            # Simulate an unexpected writer despite the real council's RO boundary.
            decision = self.controller_adr()(project, plan, snapshot, *args)
            (snapshot / "copy.txt").write_text("unexpected drift\n")
            return decision

        with patch.object(engine, "run_council", side_effect=council), \
             patch.object(engine, "worker") as worker, \
             patch.object(engine, "central_qa", side_effect=self.qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, self.plan(), authorize=True)
        self.assertEqual(result["state"], "blocked")
        worker.assert_not_called()
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")

    def test_approved_scope_cannot_be_expanded_by_implementer(self):
        (self.root / "other.txt").write_text("unrelated data\n")
        plan = planner.make_plan(self.project, "Revisa componente compartido", files=["copy.txt", "other.txt"], scope="workspace")

        def worker(project, plan, task, tree, history, settings):
            if task["role"] == "implementation":
                return {"decision": "proposed", "summary": "Synthetic out-of-ADR edit", "changes": [
                    {"path": "other.txt", "before_sha256": digest(tree / "other.txt"), "content": "unapproved edit\n"}]}
            return {"decision": "approve", "summary": "Synthetic review", "changes": []}

        with patch.object(engine, "run_council", side_effect=self.controller_adr()), \
             patch.object(engine, "worker", side_effect=worker), \
             patch.object(engine, "central_qa", side_effect=self.qa), \
             patch("ipanema.orchestration.isolation.probe", return_value={"available": True}):
            result = engine.execute(self.project, plan, authorize=True)
        self.assertEqual(result["state"], "blocked")
        self.assertEqual((self.root / "copy.txt").read_text(), "before\n")
        self.assertEqual((self.root / "other.txt").read_text(), "unrelated data\n")

    def test_production_request_never_reaches_council(self):
        plan = planner.make_plan(self.project, "Publicar producción", files=["copy.txt"], scope="workspace")
        with patch.object(engine, "run_council") as council, patch.object(engine, "worker") as worker:
            with self.assertRaises(IpanemaError):
                engine.execute(self.project, plan, authorize=True)
        council.assert_not_called()
        worker.assert_not_called()

    def test_recomputed_high_risk_cannot_disable_council(self):
        plan = self.plan()
        plan["classification"] = {"level": "L1", "risk": "normal", "production_request": False}
        plan["council"] = {"enabled": False, "mode": "off", "max_rounds": 1}
        with patch.object(engine, "worker") as worker, patch.object(engine, "central_qa") as qa:
            with self.assertRaises(IpanemaError):
                engine.execute(self.project, plan, authorize=True)
        worker.assert_not_called()
        qa.assert_not_called()


if __name__ == "__main__":
    unittest.main()
