"""rca-assistant-lite 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rca import analyze, report  # noqa: E402


class TestRCA(unittest.TestCase):
    def test_known_symptom(self):
        r = analyze("线上服务宕机了")
        self.assertEqual(len(r["five_whys"]), 5)
        self.assertTrue(len(r["possible_causes"]) >= 2)

    def test_oom_cause(self):
        r = analyze("服务宕机")
        self.assertTrue(any("OOM" in c for c in r["possible_causes"]))

    def test_unknown_symptom_fallback(self):
        r = analyze("一个从没见过的奇怪现象xyz")
        self.assertTrue(len(r["five_whys"]) == 5)
        self.assertTrue(len(r["possible_causes"]) >= 3)

    def test_report(self):
        self.assertIn("5 Why", report("响应慢"))


if __name__ == "__main__":
    unittest.main()
