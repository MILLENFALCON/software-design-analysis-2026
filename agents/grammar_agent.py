# agents/grammar_agent.py

from llm.client import call_llm

class GrammarAgent:

    def run(self, text, tasks=None, mode="default"):

        prompt = f"""
You are a professional grammar correction agent.

Tasks:
{tasks}

Mode:
{mode}

Resume:
{text}

Please:
1. Correct grammar
2. Improve spelling
3. Keep professional tone
"""

        return call_llm(prompt)
