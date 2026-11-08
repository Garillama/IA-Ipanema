from pathlib import Path
import unittest

from tests.support import ROOT
from ipanema.core import Project
from ipanema.coordinator import route, safety
from ipanema.knowledge import Knowledge


class KnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = Knowledge(Project(ROOT, "ipanema"))

    def test_hero_wins_over_generic_request_words(self):
        result = self.k.search("Quiero un hero usando componentes nativos, sin otra librería.")
        self.assertEqual(result[0]["path"], "sections/hero.tpl")

    def test_card_consumers_and_settings(self):
        card = self.k.search("tarjeta de producto", 1)[0]
        self.assertEqual(card["path"], "snippets/product-list/product-item/item.tpl")
        self.assertTrue(card["consumers"]["templates"])
        self.assertGreater(len(card["consumers"]["direct"]), 1)

    def test_unknown_configuration_does_not_become_capability(self):
        self.assertEqual(self.k.search("¿Existe quantum-layout-999? Investiga antes de afirmar que está disponible."), [])
        self.assertEqual(route("¿Existe quantum-layout-999?")["skills"], ["ipanema-architect"])

    def test_file_search_and_freshness(self):
        hit = self.k.search("snippets/image.tpl", 1)[0]
        self.assertEqual(hit["path"], "snippets/image.tpl")
        self.assertIn("observed_at", hit["freshness"])
        self.assertFalse(hit["freshness"]["remote_reverified"])

    def test_findings_not_verified_solutions(self):
        findings = self.k.findings("H1 duplicado")
        self.assertTrue(any(x["id"] == "IPN-007" for x in findings))
        self.assertTrue(all(x["knowledge_kind"] == "finding_with_proposal" for x in findings))

    def test_commerce_and_seo_routing_are_selective(self):
        skills = route("Google no encuentra categorías de mi carrusel")["skills"]
        self.assertIn("ipanema-seo-expert", skills)
        self.assertNotIn("ipanema-commerce", skills)
        self.assertFalse(safety("production", authorized_local=True)["allowed"])
        self.assertFalse(safety("local-change")["allowed"])
        self.assertTrue(safety("local-change", authorized_local=True)["allowed"])
