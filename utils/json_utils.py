import json
import re


def safe_json_loads(text):
    """
    安全解析 JSON
    """

    # 已经是 dict
    if isinstance(text, dict):
        return text

    if text is None:
        return {}

    # 非字符串转字符串
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    if not text:
        return {}

    try:
        return json.loads(text)
    except Exception:
        return {}


def extract_json_from_text(text):
    """
    从 LLM 输出中提取 JSON
    """

    # 已经是 dict
    if isinstance(text, dict):
        return text

    if text is None:
        return {}

    # 非字符串转字符串
    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    if not text:
        return {}

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return {}

    try:
        return json.loads(match.group())
    except Exception:
        return {}
