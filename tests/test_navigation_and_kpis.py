import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Collect(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.destinations=[];self.current=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if tag=='a' and 'data-nav' in d:
   self.destinations.append(d['data-nav'])
   if d.get('aria-current')=='location':self.current.append(d['data-nav'])
class NavigationAndKpiTests(unittest.TestCase):
 def setUp(self):
  self.html=(ROOT/'examples/copilot-overview.html').read_text(encoding='utf-8')
  self.parsed=Collect();self.parsed.feed(self.html)
 def test_ten_unique_valid_destinations(self):
  nav=self.parsed.destinations
  self.assertEqual(len(nav),10)
  self.assertEqual(len(nav),len(set(nav)))
  self.assertTrue(all(id in self.parsed.ids for id in nav))
  self.assertEqual(len(self.parsed.ids),len(set(self.parsed.ids)))
 def test_first_section_active(self):
  self.assertEqual(self.parsed.current,['inicio'])
 def test_metrics_have_explanations_and_missing_is_not_zero(self):
  for name in ('Chamados não encerrados','PRs abertos','Ações em destaque','Execuções com erro (24h)'):
   self.assertIn(name,self.html)
  self.assertEqual(self.html.count('<strong>—</strong>'),4)
  self.assertIn('Como ler os indicadores?',self.html)
 def test_security_and_scope_remain_visible(self):
  for value in ('n8n.naturezaapp','Naturezavet/','Bearer ','webhook/','token_hash','api.github.com'):
   self.assertNotIn(value,self.html)
if __name__=='__main__':unittest.main()
