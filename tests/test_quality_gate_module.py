import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
class QualityGateUiTests(unittest.TestCase):
    def test_module_has_three_distinct_tabs(self):
        page = (ROOT / "examples" / "quality-gate-module.html").read_text()
        for name in ("summary", "audits", "help"):
            self.assertIn('id="tab-' + name + '"', page)
            self.assertIn('id="panel-' + name + '"', page)

    def test_no_fictitious_values_as_live_metrics(self):
        page = (ROOT / "examples" / "quality-gate-module.html").read_text()
        self.assertEqual(page.count("<strong>—</strong>"), 3)
        self.assertIn("Nenhuma auditoria foi carregada", page)

    def test_no_private_links_or_configuration(self):
        page = (ROOT / "examples" / "quality-gate-module.html").read_text()
        for secret in ("webhook/", "n8n.naturezaapp", "Naturezavet/", "Bearer ", "api.github.com/", "dataTableId"):
            self.assertNotIn(secret, page)

    def test_privacy_rollout_is_documented(self):
        text = (ROOT / "docs" / "quality-gate-module.md").read_text()
        self.assertIn("Autenticação perimetral", text)
        self.assertIn("não", text.lower())
        self.assertIn("Somente", text)

if __name__ == "__main__":
    unittest.main()
