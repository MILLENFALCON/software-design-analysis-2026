# agents/content_agent.py

from llm.client import call_llm

class ContentAgent:

    def run(self, text, tasks=None, mode="default"):

        prompt = f"""
You are an advanced resume enhancement agent.

Tasks:
{tasks}

Mode:
{mode}

Resume:
{text}

Requirements:
- Expand project descriptions
- Generate STAR-format experience
- Add quantified achievements
- Improve ATS keyword matching
"""

        return call_llm(prompt)
