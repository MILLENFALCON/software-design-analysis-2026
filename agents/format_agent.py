# agents/format_agent.py

from llm.client import call_llm

class FormatAgent:

    def run(self, text, tasks=None, mode="default"):

        prompt = f"""
You are a professional resume formatting agent.

Tasks:
{tasks}

Resume:
{text}

Requirements:
- Improve formatting
- Generate sections/subsections
- Normalize bullet points
- Make it suitable for Word export
"""

        return call_llm(prompt)
