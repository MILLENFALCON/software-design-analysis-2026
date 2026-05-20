from llm.client import call_llm


def direct_llm_optimize(resume_text):

    prompt = f"""
You are an elite resume optimization assistant.

Your job is to directly improve the following resume.

Requirements:
- Fix grammar and spelling
- Improve professionalism
- Improve ATS compatibility
- Enhance project descriptions
- Use STAR-style descriptions when possible
- Improve formatting
- Keep output concise and clean
- Output ONLY the optimized resume text

Resume:
{resume_text}
"""

    return call_llm(prompt)
