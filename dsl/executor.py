from agents.grammar_agent import GrammarAgent
from agents.content_agent import ContentAgent
from agents.format_agent import FormatAgent
from agents.score_agent import ScoreAgent
from agents.reviewer_agent import ReviewerAgent
from agents.export_agent import ExportAgent


class WorkflowExecutor:

    def __init__(self, workflow):
        self.workflow = workflow

        self.agent_map = {
            "GrammarAgent": GrammarAgent(),
            "ContentAgent": ContentAgent(),
            "FormatAgent": FormatAgent(),
            "ScoreAgent": ScoreAgent(),
            "ReviewerAgent": ReviewerAgent(),
            "ExportAgent": ExportAgent()
        }

        self.context = {}

    def execute(self, resume_text):
        current_data = resume_text
        steps = self.workflow["steps"]
        i = 0
        while i < len(steps):
            step = steps[i]
            agent_name = step["agent"]
            agent = self.agent_map[agent_name]

            # 处理输入
            input_key = step.get("input")
            if input_key and input_key in self.context:
                input_data = self.context[input_key]
            else:
                input_data = current_data

            print(f"\nRunning {agent_name}...")
            result = agent.run(input_data, step["tasks"])

            output_key = step.get("output")
            if output_key:
                self.context[output_key] = result

            current_data = result

            # 检查条件跳转（紧跟在评分步骤之后）
            if agent_name == "ScoreAgent":
                threshold = self.workflow.get("config", {}).get("SCORE_THRESHOLD", 85)
                overall = self.context["score_report"].get("overall_score", 0)
                if overall < threshold:
                    print(f"Score {overall} < {threshold}, looping back to STEP 2...")
                    i = 1  # 回到 STEP 2 (index 1)
                    continue
            i += 1
        return current_data