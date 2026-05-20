import unittest
from dsl.parser import WorkflowParser

class TestWorkflowParser(unittest.TestCase):
    def setUp(self):
        self.parser = WorkflowParser("dsl/workflow.dsl")

    def test_parse_returns_steps(self):
        workflow = self.parser.parse()
        self.assertIn("steps", workflow)
        self.assertGreater(len(workflow["steps"]), 0)

    def test_first_step_is_grammar_agent(self):
        workflow = self.parser.parse()
        first_step = workflow["steps"][0]
        self.assertEqual(first_step["agent"], "GrammarAgent")

    def test_output_keys_exist(self):
        workflow = self.parser.parse()
        outputs = [s.get("output") for s in workflow["steps"]]
        self.assertIn("grammar_report", outputs)
        self.assertIn("formatted_resume", outputs)
        self.assertIn("final_resume", outputs)

if __name__ == "__main__":
    unittest.main()