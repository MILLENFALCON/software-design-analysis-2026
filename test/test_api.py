from dotenv import load_dotenv
from openai import OpenAI
import os

# 读取 .env
load_dotenv()

# 获取 API Key
api_key = os.getenv("OPENAI_API_KEY")

print("========== API KEY CHECK ==========")

if api_key is None:
    print("❌ 没有读取到 API Key")
    exit()

print("✅ 成功读取 API Key")
print("Key 前缀:", api_key[:10])

print("\n========== TESTING API ==========")

try:
    client = OpenAI(
        api_key=api_key
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    )

    print("✅ API 调用成功！")
    print("\n模型回复：")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ API 调用失败")
    print(e)
