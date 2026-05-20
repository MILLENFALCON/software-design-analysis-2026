# agents/score_agent.py
from llm.client import call_llm
import json


class ScoreAgent:

    def run(self, text, tasks=None, mode="default"):

        prompt = f"""
You are a professional resume evaluation agent.

Evaluate the following resume.

Scoring dimensions:
1. ATS compatibility
2. Grammar and spelling
3. Content quality
4. Professional formatting
5. Technical relevance

Return ONLY JSON.

Resume:
{text}

Example:
{{
    "ats_score": 85,
    "grammar_score": 90,
    "content_score": 88,
    "format_score": 87,
    "overall_score": 87.5,
    "strengths": [
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "..."
    ],
    "suggestions": [
        "...",
        "..."
    ]
}}
"""

        response = call_llm(prompt)

        try:
            cleaned = response.replace(
                "```json", ""
            ).replace(
                "```", ""
            ).strip()

            return json.loads(cleaned)

        except Exception as e:

            print(
                f"Score parsing failed: {e}"
            )

            return {
                "ats_score": 0,
                "grammar_score": 0,
                "content_score": 0,
                "format_score": 0,
                "overall_score": 0,
                "strengths": [],
                "weaknesses": [],
                "suggestions": []
            }