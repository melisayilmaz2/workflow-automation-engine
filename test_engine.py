import unittest
from engine import matches,run_workflows
class EngineTests(unittest.TestCase):
 def test_condition(self):
  self.assertTrue(matches([{'field':'amount','operator':'greater_than','value':10}],{'amount':20}))
  self.assertFalse(matches([{'field':'amount','operator':'less_than','value':10}],{'amount':20}))
 def test_rule_execution(self):
  events=[{'id':'1','event_type':'lead_created','amount':100}]
  rules=[{'name':'Route lead','trigger':'lead_created','conditions':[{'field':'amount','operator':'greater_than','value':50}],'actions':[{'type':'assign_owner','value':'Sales'},{'type':'create_task','value':'Call lead'}]}]
  out=run_workflows(events,rules)
  self.assertEqual(out['summary']['tasks_created'],1)
  self.assertEqual(out['tasks'][0]['owner'],'Sales')
  self.assertNotIn('owner',events[0]) # no input mutation
 def test_disabled_rule(self):
  out=run_workflows([{'id':'1','event_type':'lead_created'}],[{'name':'Disabled','enabled':False,'trigger':'lead_created','actions':[{'type':'create_task','value':'No'}]}])
  self.assertEqual(out['summary']['rules_triggered'],0)
 def test_duplicate_tag_not_added(self):
  out=run_workflows([{'id':'1','event_type':'lead_created','tags':['vip']}],[{'name':'Tag','trigger':'lead_created','actions':[{'type':'add_tag','value':'vip'}]}])
  self.assertEqual(out['processed_events'][0]['tags'],['vip'])
 def test_bad_operator(self):
  with self.assertRaises(ValueError):matches([{'field':'a','operator':'magic','value':1}],{'a':1})
if __name__=='__main__':unittest.main()
