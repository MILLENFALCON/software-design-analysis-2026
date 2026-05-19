# agents/optimizer_agent.py

import json

from agents.base_agent import BaseAgent


class OptimizerAgent(BaseAgent):

    def __init__(self, config):

        super().__init__(
            config,
            "prompts/optimizer_prompt.txt"
        )

    def run(
        self,
        resume,
        feedback,
        resolved_issues=None
    ):

        payload = {

            "resume": resume,

            "feedback": feedback,

            "resolved_issues": (
                resolved_issues or []
            )
        }

        result = self.generate(
            json.dumps(payload, indent=2)
        )

        return self.validate(
            result,
            resume
        )

    def validate(
        self,
        optimized,
        original
    ):

        if not isinstance(optimized, dict):
            return original

        required = [
            "summary",
            "skills",
            "experience",
            "education"
        ]

        for field in required:

            if field not in optimized:
                optimized[field] = original.get(
                    field,
                    []
                )

        return optimized

    def fallback(self):

        return {}
