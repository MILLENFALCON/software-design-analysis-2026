# llm/client.py

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("ZHIPU_API_KEY", "e4cebc27672b4050aa3326a66394ff65.6aU5CbpxtWEH68YF"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def call_llm(prompt):
    response = client.chat.completions.create(
        model="glm-4-flash",   # 根据你的智谱账号可用模型选择
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content