import re


class WorkflowParser:

    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath, "r") as f:
            lines = f.readlines()

        workflow = {
            "config": {},
            "steps": []
        }

        current_step = None

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith("STEP"):
                if current_step:
                    workflow["steps"].append(current_step)

                step_number = re.findall(r"\d+", line)[0]

                current_step = {
                    "step": int(step_number),
                    "tasks": []
                }

            elif line.startswith("AGENT:"):
                current_step["agent"] = line.split(":")[1].strip()

            elif line.startswith("TASK:"):
                current_step["tasks"].append(
                    line.split(":")[1].strip()
                )

            elif line.startswith("MODE:"):
                current_step["mode"] = line.split(":")[1].strip()

            elif line.startswith("INPUT:"):
                current_step["input"] = line.split(":")[1].strip()

            elif line.startswith("OUTPUT:"):
                current_step["output"] = line.split(":")[1].strip()

            elif line.startswith("CONFIG:"):
                # 跳过
                pass
            
            elif ":" in line and not line.startswith(("STEP", "AGENT", "TASK", "MODE", "INPUT", "OUTPUT")):
                key, val = line.split(":", 1)
                if key.strip() in ("SCORE_THRESHOLD", "MAX_ITERATION"):
                    workflow["config"][key.strip()] = int(val.strip())
                    
        if current_step:
            workflow["steps"].append(current_step)

        return workflow
