# main.py

import json
import yaml

from copy import deepcopy

from agents.parser_agent import ParserAgent
from agents.optimizer_agent import OptimizerAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.feedback_agent import FeedbackAgent
from agents.reflection_agent import ReflectionAgent
from agents.diff_agent import DiffAgent


# =========================
# Config
# =========================

with open(
    "configs/config.yaml",
    "r"
) as f:

    config = yaml.safe_load(f)


# =========================
# Agents
# =========================

parser_agent = ParserAgent(config)

optimizer_agent = OptimizerAgent(config)

evaluator_agent = EvaluatorAgent(config)

feedback_agent = FeedbackAgent(config)

reflection_agent = ReflectionAgent(config)

diff_agent = DiffAgent(config)


# =========================
# Load Resume
# =========================

with open(
    "data/raw/sample_resume.txt",
    "r",
    encoding="utf-8"
) as f:

    resume_text = f.read()


# =========================
# Parse Resume
# =========================

parsed_resume = parser_agent.run(
    resume_text
)


# =========================
# State
# =========================

state = {

    "current_resume": parsed_resume,

    "history": [],

    "scores": [],

    "resolved_issues": [],

    "unresolved_issues": []
}


# =========================
# Main Loop
# =========================

for iteration in range(
    config["max_iterations"]
):

    print(
        f"\n========== ITERATION {iteration+1} ==========\n"
    )

    current_resume = state[
        "current_resume"
    ]

    # =====================
    # Evaluate
    # =====================

    evaluation = evaluator_agent.run(
        current_resume
    )

    state["scores"].append(
        evaluation["overall_score"]
    )

    # =====================
    # Feedback
    # =====================

    feedback = feedback_agent.run(

        resume=current_resume,

        evaluation=evaluation,

        unresolved_issues=state[
            "unresolved_issues"
        ]
    )

    # =====================
    # Optimize
    # =====================

    optimized_resume = optimizer_agent.run(

        resume=current_resume,

        feedback=feedback,

        resolved_issues=state[
            "resolved_issues"
        ]
    )

    # =====================
    # Diff
    # =====================

    diff = diff_agent.run(

        old_resume=current_resume,

        new_resume=optimized_resume,

        previous_issues=state[
            "unresolved_issues"
        ]
    )

    state["resolved_issues"] = diff[
        "resolved"
    ]

    state["unresolved_issues"] = diff[
        "unresolved"
    ]

    # =====================
    # History
    # =====================

    state["history"].append({

        "iteration": iteration + 1,

        "score": evaluation[
            "overall_score"
        ],

        "evaluation": evaluation,

        "feedback": feedback,

        "diff": diff
    })

    # =====================
    # Reflection
    # =====================

    should_continue = (
        reflection_agent.run(

            scores=state["scores"],

            unresolved_issues=state[
                "unresolved_issues"
            ]
        )
    )

    state["current_resume"] = (
        optimized_resume
    )

    if not should_continue:

        print(
            "\nOptimization Converged.\n"
        )

        break


# =========================
# Save
# =========================

with open(
    "data/outputs/history.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        state["history"],
        f,
        indent=2,
        ensure_ascii=False
    )

with open(
    "data/outputs/optimized_resume.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        state["current_resume"],
        f,
        indent=2,
        ensure_ascii=False
    )

print("\nDone.\n")
