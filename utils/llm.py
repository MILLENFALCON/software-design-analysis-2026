from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def ask_llm(text):
    resp = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": text}]
    )
    return resp.choices[0].message.content
