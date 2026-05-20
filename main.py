from dsl.parser import WorkflowParser
from dsl.executor import WorkflowExecutor
from llm.direct_llm import direct_llm_optimize
from agents.score_agent import ScoreAgent   # 新增：导入 ScoreAgent 用于单独评分

from docx import Document
import os


def load_resume(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def save_to_word(text, filename):
    doc = Document()
    for line in str(text).split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)
    print(f"Saved: {filename}")


def main():
    # ========= Load Resume =========
    resume = load_resume("data/raw/sample_resume.txt")

    # ========= Parse Workflow =========
    parser = WorkflowParser("dsl/workflow.dsl")
    workflow = parser.parse()

    # ========= Multi-Agent =========
    executor = WorkflowExecutor(workflow)
    multi_agent_result = executor.execute(resume)

    # ========= Handle Result =========
    if isinstance(multi_agent_result, str) and os.path.exists(multi_agent_result):
        with open(multi_agent_result, "r", encoding="utf-8") as f:
            multi_agent_resume = f.read()
    else:
        multi_agent_resume = str(multi_agent_result)

    # ========= Direct LLM =========
    direct_resume = direct_llm_optimize(resume)

    # ========= Score both resumes =========
    scorer = ScoreAgent()

    # 评分 multi-agent 结果（从 context 中取已有的评分，避免重复调用 API）
    multi_score = executor.context.get("score_report")
    if not multi_score or not isinstance(multi_score, dict):
        print("Multi-agent score not found, re-scoring...")
        multi_score = scorer.run(multi_agent_resume)

    # 评分 direct LLM 结果
    print("\nScoring Direct LLM resume...")
    direct_score = scorer.run(direct_resume)

    # ========= Print =========
    print("\n=== Multi-Agent Resume ===\n")
    print(multi_agent_resume)

    print("\n=== Direct LLM Resume ===\n")
    print(direct_resume)

    # ========= Print Scores =========
    print("\n========== Score Comparison ==========")
    print(f"{'Multi-Agent':<20} | {'Direct LLM':<20}")
    print("-" * 42)
    print(f"ATS Score:        {multi_score.get('ats_score', 0):<6}      | {direct_score.get('ats_score', 0):<6}")
    print(f"Grammar Score:    {multi_score.get('grammar_score', 0):<6}      | {direct_score.get('grammar_score', 0):<6}")
    print(f"Content Score:    {multi_score.get('content_score', 0):<6}      | {direct_score.get('content_score', 0):<6}")
    print(f"Format Score:     {multi_score.get('format_score', 0):<6}      | {direct_score.get('format_score', 0):<6}")
    print(f"Overall Score:    {multi_score.get('overall_score', 0):<6}      | {direct_score.get('overall_score', 0):<6}")
    print("-" * 42)

    # ========= Save =========
    os.makedirs("output", exist_ok=True)
    save_to_word(multi_agent_resume, "output/multi_agent_resume.docx")
    save_to_word(direct_resume, "output/direct_resume.docx")

    print("\nDone.")


if __name__ == "__main__":
    main()