try:
    from ollama import chat, ChatResponse
    print("ollama模块导入成功")
except ImportError as e:
    print(f"ollama模块导入失败: {e}")

from openai import OpenAI

MODEL_NAME1 = "deepseek-r1:1.5b"

def ollama(s, t):
    # ollama调用大模型
    response: ChatResponse = chat(model=MODEL_NAME1, messages=[
        {
            'role': 'user',
            'content': f'{s}。{t}',
        },
    ])
    s3 = response.message.content.split("</think>")[1]
    # s3 = s3.replace("\n", "<br>")
    s3 = s3.split("```")[1]
    return s3

# sk-7dce4a31d1a148808287aecab23a3d2a
def deepseek(s, t):
    client = OpenAI(api_key="sk-88d31d7acfdb4a37a437d85e73bb59ea", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        # DeepSeek-V3-0324
        model="deepseek-reasoner",
        # # DeepSeek-R1-0528
        # model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": s},
            {"role": "user", "content": t},
        ],
        stream=False
    )
    s3 = response.choices[0].message.content
    return s3

print(deepseek("你是一名中学教师","请对王明学生做一个生成报告：语文100、数学130、英语110。生成html页面"))