# agents/base_agent.py

from utils.json_utils import (
    safe_json_loads,
    extract_json_from_text
)

from utils.llm import call_llm


class BaseAgent:

    def __init__(
        self,
        config,
        prompt_path
    ):
        self.config = config

        with open(
            prompt_path,
            "r",
            encoding="utf-8"
        ) as f:
            self.system_prompt = f.read()

    # =========================
    # Main API
    # =========================

    def run(self, *args, **kwargs):
        raise NotImplementedError

    # =========================
    # LLM Generation
    # =========================

    def generate(
        self,
        user_input,
        expect_json=True,
        retries=None,
        temperature=None
    ):
        if retries is None:
            retries = self.config.get(
                "retries",
                2
            )

        if temperature is None:
            temperature = self.config.get(
                "temperature",
                0.7
            )

        last_error = None

        for attempt in range(retries + 1):

            try:
                response = call_llm(
                    system_prompt=self.system_prompt,
                    user_input=user_input,
                    model=self.config["model"],
                    temperature=temperature
                )

                # 不需要 JSON，直接返回原始文本
                if not expect_json:
                    return response

                # 提取 JSON
                cleaned = extract_json_from_text(
                    response
                )

                # 安全解析（不会抛异常）
                result = safe_json_loads(
                    cleaned
                )

                # 如果解析失败，返回 {}
                if not isinstance(result, dict):
                    result = {}

                # 解析成功则直接返回
                if result:
                    return result

                # 解析失败则触发重试
                raise ValueError(
                    "Failed to parse valid JSON from LLM response."
                )

            except Exception as e:
                last_error = e

                print(
                    f"[{self.__class__.__name__}] "
                    f"Attempt {attempt + 1} failed"
                )

                print(e)

        # 所有重试失败后调用 fallback
        return self.on_failure(last_error)

    # =========================
    # Failure Hook
    # =========================

    def on_failure(self, error):
        print(
            f"[{self.__class__.__name__}] Final Failure"
        )

        print(error)

        return self.fallback()

    # =========================
    # Fallback
    # =========================

    def fallback(self):
        return {}
