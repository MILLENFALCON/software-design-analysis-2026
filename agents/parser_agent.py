# agents/parser_agent.py

from agents.base_agent import BaseAgent


class ParserAgent(BaseAgent):

    def __init__(self, config):

        super().__init__(
            config,
            "prompts/parser_prompt.txt"
        )

    def run(self, resume_text):

        result = self.generate(
            resume_text,
            expect_json=True
        )

        return self.normalize(result)

    def normalize(self, result):

        if not isinstance(result, dict):
            return self.fallback()

        required = [
            "summary",
            "skills",
            "experience",
            "education"
        ]

        for field in required:

            if field not in result:
                result[field] = []

        return result

    def fallback(self):

        return {

            "summary": "",

            "skills": [],

            "experience": [],

            "education": []
        }
