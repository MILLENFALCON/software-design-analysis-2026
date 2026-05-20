# agents/export_agent.py
import os
from llm.client import call_llm

class ExportAgent:

    def run(self, data, tasks=None, mode="default"):
        """
        使用 LLM 优化导出文本，然后写入 output/final_resume.txt
        """

        prompt = f"""
You are an expert in exporting resumes.

Tasks:
{tasks}

Resume:
{data}

Requirements:
- Generate a polished version suitable for Word or PDF
- Keep formatting clean
- Output as plain text
"""

        final_text = call_llm(prompt)

        os.makedirs("output", exist_ok=True)
        output_path = "output/final_resume.txt"

        with open(output_path, "w") as f:
            f.write(final_text)

        print(f"Resume exported to {output_path}")

        return output_path
