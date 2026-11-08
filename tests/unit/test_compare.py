from pathlib import Path
import tempfile
import unittest

from tests.support import put
from ipanema.compare import metrics, read_png, visual, write_png
from ipanema.core import IpanemaError


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.a, self.b = self.root / "a.png", self.root / "b.png"
        write_png(self.a, 10, 10, bytes([255, 255, 255, 255])*100)

    def tearDown(self):
        self.tmp.cleanup()

    def test_identical_passes_and_pixel_regression_fails(self):
        self.b.write_bytes(self.a.read_bytes())
        self.assertEqual(visual(self.a, self.b)["status"], "passed")
        pixels = bytearray(read_png(self.b)[2])
        pixels[0:4] = bytes([0, 0, 0, 255])
        write_png(self.b, 10, 10, pixels)
        result = visual(self.a, self.b)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["changed_pixels"], 1)

    def test_dynamic_mask_and_tolerance(self):
        pixels = bytearray(read_png(self.a)[2])
        pixels[0:4] = bytes([0, 0, 0, 255])
        write_png(self.b, 10, 10, pixels)
        self.assertEqual(visual(self.a, self.b, masks=[[0, 0, 1, 1]])["status"], "passed")
        self.assertEqual(visual(self.a, self.b, max_changed_ratio=.02)["status"], "passed")
        with self.assertRaises(IpanemaError):
            visual(self.a, self.b, masks=[[0, 0, 10, 10]])

    def test_dimensions_and_corrupt_file(self):
        write_png(self.b, 2, 2, bytes([255, 255, 255, 255])*4)
        self.assertEqual(visual(self.a, self.b)["reason"], "dimensions_changed")
        self.b.write_bytes(b"not a PNG")
        with self.assertRaises(IpanemaError):
            read_png(self.b)

    def test_metrics_profiles_and_regression(self):
        a, b = self.root / "a.json", self.root / "b.json"
        put(a, {"profile": "mobile", "page": "home", "metrics": {"lcp_ms": 1000}})
        put(b, {"profile": "mobile", "page": "home", "metrics": {"lcp_ms": 1500}})
        self.assertEqual(metrics(a, b)["status"], "failed")
        put(b, {"profile": "desktop", "page": "home", "metrics": {"lcp_ms": 1000}})
        with self.assertRaises(IpanemaError):
            metrics(a, b)

    def test_unmeasured_metrics_do_not_pass(self):
        a,b=self.root/'a.json',self.root/'b.json'
        put(a,{'profile':'mobile','page':'home','metrics':{}})
        put(b,{'profile':'mobile','page':'home','metrics':{}})
        self.assertEqual(metrics(a,b)['status'],'not_measured')

    def test_missing_context_or_different_lighthouse_config_rejected(self):
        a,b=self.root/'a.json',self.root/'b.json'
        put(a,{'metrics':{'lcp_ms':1000}});put(b,{'metrics':{'lcp_ms':800}})
        with self.assertRaises(IpanemaError):metrics(a,b)
        put(a,{'profile':'mobile','page':'home','config':{'cpu':4},'metrics':{'lcp_ms':1000}})
        put(b,{'profile':'mobile','page':'home','config':{'cpu':1},'metrics':{'lcp_ms':800}})
        with self.assertRaises(IpanemaError):metrics(a,b)
