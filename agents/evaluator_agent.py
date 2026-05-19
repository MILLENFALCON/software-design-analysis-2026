# agents/evaluator_agent.py

from agents.base_agent import BaseAgent


class EvaluatorAgent(BaseAgent):

    SCORE_FIELDS = [
        "clarity",
        "impact",
        "ats",
        "professionalism"
    ]

    def __init__(self, config):

        super().__init__(
            config,
            "prompts/evaluator_prompt.txt"
        )

    def run(self, resume):

        result = self.generate(resume)

        return self.normalize(result)

    def normalize(self, evaluation):

        if not isinstance(evaluation, dict):
            return self.fallback()

        scores = []

        for field in self.SCORE_FIELDS:

            try:
                value = float(
                    evaluation.get(field, 5)
                )

            except:
                value = 5

            value = max(0, min(10, value))

            evaluation[field] = round(value, 1)

            scores.append(value)

        evaluation["overall_score"] = round(
            sum(scores) / len(scores),
            2
        )

        issues = evaluation.get("issues", [])

        if not isinstance(issues, list):
            issues = []

        evaluation["issues"] = list(set([
            str(i).lower().strip().replace(" ", "_")
            for i in issues
        ]))

        return evaluation

    def fallback(self):

        return {

            "clarity": 5,
            "impact": 5,
            "ats": 5,
            "professionalism": 5,

            "overall_score": 5.0,

            "issues": [
                "evaluation_failure"
            ]
        }
