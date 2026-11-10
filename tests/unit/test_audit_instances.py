"""Regresión del formato de instancias encontrado en Damar; datos sintéticos."""
import unittest
from tests.support import ROOT
import importlib.util

spec=importlib.util.spec_from_file_location('audit_source_instances',ROOT/'tools/audit_source.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

class TemplateInstances(unittest.TestCase):
    def test_empty_block_array_does_not_break_inventory(self):
        result=[]
        audit.instances({'sections':{'hero':{'type':'hero','blocks':[]}}},'home.json#',result)
        self.assertEqual([(r['kind'],r['type']) for r in result],[('section','hero')])

    def test_mixed_instance_containers_retain_locations(self):
        result=[]
        audit.instances({'sections':[{'type':'hero','blocks':{'title':{'type':'heading'}}}]},'home.json#',result)
        self.assertEqual([r['location'] for r in result],['home.json#/0','home.json#/0/title'])
        self.assertEqual([r['type'] for r in result],['hero','heading'])
