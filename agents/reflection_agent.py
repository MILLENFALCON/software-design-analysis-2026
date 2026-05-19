# agents/reflection_agent.py

from agents.base_agent import BaseAgent


class ReflectionAgent(BaseAgent):

    def __init__(self, config):

        super().__init__(
            config,
            "prompts/reflection_prompt.txt"
        )

        self.score_threshold = config.get(
            "score_improvement_threshold",
            0.3
        )

        self.patience = config.get(
            "reflection_patience",
            2
        )

    def run(
        self,
        scores,
        unresolved_issues
    ):

        """
        Decide whether optimization should continue.

        Stop conditions:
        1. score improvement too small
        2. no remaining unresolved issues
        3. score stagnation
        """

        # =========================
        # Condition 1:
        # No unresolved issues
        # =========================

        if len(unresolved_issues) == 0:

            print(
                "[Reflection] No unresolved issues remaining."
            )

            return False

        # =========================
        # Condition 2:
        # Not enough iterations yet
        # =========================

        if len(scores) < 2:
            return True

        # =========================
        # Score improvement
        # =========================

        latest_score = scores[-1]
        previous_score = scores[-2]

        improvement = latest_score - previous_score

        print(
            f"[Reflection] Score Improvement: {improvement:.2f}"
        )

        # =========================
        # Condition 3:
        # Improvement too small
        # =========================

        if improvement < self.score_threshold:

            print(
                "[Reflection] Improvement below threshold."
            )

            return False

        # =========================
        # Condition 4:
        # Score stagnation
        # =========================

        if len(scores) >= self.patience + 1:

            recent_scores = scores[-(self.patience + 1):]

            deltas = []

            for i in range(1, len(recent_scores)):

                delta = (
                    recent_scores[i]
                    - recent_scores[i - 1]
                )

                deltas.append(delta)

            avg_delta = sum(deltas) / len(deltas)

            print(
                f"[Reflection] Average Delta: {avg_delta:.2f}"
            )

            if avg_delta < self.score_threshold:

                print(
                    "[Reflection] Optimization stagnated."
                )

                return False

        return True
