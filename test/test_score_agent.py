import unittest
from agents.score_agent import ScoreAgent

class TestScoreAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ScoreAgent()

    def test_run_returns_dict(self):
        # 用一个极简简历测试，实际会调用 LLM，需联网
        result = self.agent.run("Name: Test\nSkills: Python")
        self.assertIsInstance(result, dict)
        self.assertIn("overall_score", result)

    def test_parse_malformed_json(self):
        # 模拟 call_llm 返回乱码的情况
        original_call = __import__("agents.score_agent", fromlist=["call_llm"]).call_llm
        def fake_call(prompt):
            return "not json at all"
        # 注入 mock（此处简化，实际可用 unittest.mock）
        # 建议直接测试 run 方法的异常处理分支
        pass

if __name__ == "__main__":
    unittest.main()