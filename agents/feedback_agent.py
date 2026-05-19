# agents/feedback_agent.py

import json

from agents.base_agent import BaseAgent


class FeedbackAgent(BaseAgent):

    def __init__(self, config):

        super().__init__(
            config,
            "prompts/feedback_prompt.txt"
        )

    def run(
    self,
    resume,
    evaluation,
    unresolved_issues=None
    ):

        if unresolved_issues is None:
            unresolved_issues = []


        user_input = f"""
Resume:
{resume}

Evaluation:
{json.dumps(evaluation, indent=2)}
"""

        raw_result = self.generate(user_input)

        feedback = self._parse_result(raw_result)

        feedback = self._normalize_feedback(
            feedback
        )

        return feedback

    # =========================
    # Parse JSON
    # =========================

    def _parse_result(self, raw_result):

        print("\n[Feedback Raw Result]")
        print(raw_result)

        try:

            raw_result = raw_result.strip()

            if raw_result.startswith("```json"):
                raw_result = raw_result.replace(
                    "```json",
                    ""
                )

            if raw_result.endswith("```"):
                raw_result = raw_result[:-3]

            raw_result = raw_result.strip()

            result = json.loads(raw_result)

            return result

        except Exception as e:

            print(
                "[Feedback] JSON Parse Error:"
            )

            print(e)

            return self._fallback_feedback()

    # =========================
    # Normalize Feedback
    # =========================

    def _normalize_feedback(
        self,
        feedback
    ):

        required_fields = [
            "priority_issues",
            "recommended_actions",
            "section_targets"
        ]

        for field in required_fields:

            if field not in feedback:
                feedback[field] = []

            if not isinstance(
                feedback[field],
                list
            ):
                feedback[field] = []

        # Normalize issue names
        normalized_issues = []

        for issue in feedback[
            "priority_issues"
        ]:

            issue = (
                issue
                .lower()
                .strip()
                .replace(" ", "_")
            )

            normalized_issues.append(issue)

        feedback[
            "priority_issues"
        ] = list(set(normalized_issues))

        # Remove duplicates
        feedback[
            "recommended_actions"
        ] = list(
            dict.fromkeys(
                feedback[
                    "recommended_actions"
                ]
            )
        )

        feedback[
            "section_targets"
        ] = list(
            dict.fromkeys(
                feedback[
                    "section_targets"
                ]
            )
        )

        return feedback

    # =========================
    # Fallback
    # =========================

    def _fallback_feedback(self):

        return {

            "priority_issues": [
                "feedback_generation_failure"
            ],

            "recommended_actions": [
                "Regenerate feedback plan"
            ],

            "section_targets": []
        }
