# from pydantic import RootModel


# class User(RootModel):
#     root: str


# a = "你好啊，大家好"
# print(a[:5])

# from transformers import AutoModelForCausalLM, AutoTokenizer

# # 加载模型
# model_name = "Qwen/Qwen2.5-0.5B"


# # 加载分词器
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# # 编码输入文本
# input_text = "这是一个测试文本"
# inputs = tokenizer(input_text, return_tensors="pt")

# # 生成文本
# print(inputs)


# import tempfile
# import os

# # 获取临时目录路径
# temp_dir = tempfile.gettempdir()
# print("临时目录路径:", temp_dir)

# # 列出临时目录中的文件（需要权限）
# try:
#     print("临时目录内容:", os.listdir(temp_dir))
# except PermissionError:
#     print("无权限访问临时目录内容")


from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional, AsyncGenerator
import asyncio
from loguru import logger

load_dotenv()
llm_base_url = os.getenv("LLM_BASE_URL")
llm_api_key = os.getenv("LLM_API_KEY")
llm_model = os.getenv("LLM_MODEL")

client = OpenAI(base_url=llm_base_url, api_key=llm_api_key)


def test(messages: list):
    chat_completion = client.chat.completions.create(
        model=llm_model,
        messages=messages,
        stream=True,
    )
    for chunk in chat_completion:
        print(chunk.choices[0].delta.content)


messages = [
    {
        "role": "system",
        "content": "请从根据给定的语料中提取实体及其之间的关系。语料可能包含人物、地点、组织、事件、时间等实体，以及它们之间的关联（如隶属、参与、发生等）。请按照以下格式输出结果：\n\n1. **实体**：列出所有识别出的实体，并标注其类型（如人物、地点、组织等）。\n2. **关系**：描述实体之间的关系，格式为“[实体1] - [关系类型] - [实体2]”。\n\n**示例语料：**\n“2023年10月，阿里巴巴集团在杭州举办了全球技术峰会，CEO张勇发表了主题演讲。”\n\n**示例输出：**\n1. **实体**：\n   - 阿里巴巴集团（组织）\n   - 杭州（地点）\n   - 全球技术峰会（事件）\n   - 2023年10月（时间）\n   - 张勇（人物）\n   - CEO（职位）\n\n2. **关系**：\n   - 阿里巴巴集团 - 举办 - 全球技术峰会\n   - 全球技术峰会 - 发生地点 - 杭州\n   - 全球技术峰会 - 发生时间 - 2023年10月\n   - 张勇 - 担任 - CEO\n   - 张勇 - 参与 - 全球技术峰会",
    },
    {
        "role": "user",
        "content": "过去几周，深度求索（DeepSeek）在全球 AI 领域掀起了一场风暴，成为众人瞩目的焦点。",
    },
    {
        "role": "user",
        "content": '请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of","description":"Satya Nadella serves as the Chief Executive Officer of Microsoft, leading the company\'s overall strategy and direction." }, { "head": "0, "tail": 2, "type": "developed","description":"Microsoft developed Azure AI, a suite of cloud-based artificial intelligence services and tools aimed at empowering developers and organizations." } ] }\n给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的',
    },
    {
        "role": "user",
        "content": "请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容",
    },
]
print(test(messages))
