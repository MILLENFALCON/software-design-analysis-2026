# agents/diff_agent.py

import json

from agents.base_agent import BaseAgent


class DiffAgent(BaseAgent):

    def __init__(self, config):

        super().__init__(
            config,
            "prompts/diff_prompt.txt"
        )

    def run(
        self,
        old_resume,
        new_resume,
        previous_issues=None
    ):

        payload = {

            "old_resume": old_resume,

            "new_resume": new_resume,

            "previous_issues": (
                previous_issues or []
            )
        }

        result = self.generate(
            json.dumps(payload, indent=2)
        )

        return self.normalize(result)

    def normalize(self, result):

        fields = [
            "resolved",
            "unresolved",
            "new_issues"
        ]

        for field in fields:

            values = result.get(field, [])

            if not isinstance(values, list):
                values = []

            result[field] = list(set([
                str(v).lower().strip().replace(" ", "_")
                for v in values
            ]))

        return result

    def fallback(self):

        return {

            "resolved": [],
            "unresolved": [],
            "new_issues": [
                "diff_failure"
            ]
        }
