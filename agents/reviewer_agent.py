# agents/reviewer_agent.py
from llm.client import call_llm

class ReviewerAgent:

    def run(self, data, tasks=None, mode="default"):
        """
        使用 LLM 审核简历一致性、重复内容和逻辑问题
        """

        prompt = f"""
You are a professional resume reviewer.

Tasks:
{tasks}

Resume:
{data}

Requirements:
- Check for consistency across sections
- Detect duplicate entries
- Identify possible factual errors
- Suggest improvements
"""

        review_result = call_llm(prompt)

        return {
            "review_status": "PASS",  # 可以改成根据 LLM 输出解析
            "data": review_result
        }
