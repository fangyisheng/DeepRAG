from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
from importlib import resources
import asyncio
import json
from loguru import logger

with (
    resources.files("deeprag.prompts.fixed_prompts")
    .joinpath("extract_entity_relationship_prompt.txt")
    .open("r") as file
):
    system_prompt = file.read()

# cot_prompt_chain1 = [{"role":"user","content":"""请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": "0, "tail": 2, "type": "developed" } ] }
# 注意，可能会有同名的实体，请关注上下文正确区分同名的实体。给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的"""}]
cot_prompt_chain1 = [
    {
        "role": "user",
        "content": """请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of","description":"Satya Nadella serves as the Chief Executive Officer of Microsoft, leading the company's overall strategy and direction." }, { "head": "0, "tail": 2, "type": "developed","description":"Microsoft developed Azure AI, a suite of cloud-based artificial intelligence services and tools aimed at empowering developers and organizations." } ] }
给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的""",
    }
]

cot_prompt_chain2 = [
    {
        "role": "user",
        "content": """请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容""",
    }
]

cot_prompt = cot_prompt_chain1 + cot_prompt_chain2


async def extract_entity_relationship_agent(user_prompt: str) -> dict:
    response = await llm_service(
        system_prompt=system_prompt, user_prompt=user_prompt, cot_prompt=cot_prompt
    )
    logger.info(f"这是提取的图结构：{response}")
    return json.loads(response)


# user_prompt = """过去几周，深度求索（DeepSeek）在全球 AI 领域掀起了一场风暴，成为众人瞩目的焦点。这家成立于 2023 年的年轻大模型公司，宛如一匹黑马，迅速在行业中崭露头角，其影响力甚至在美股市场都有明显体现。1 月 27 日，美股 AI、芯片股重挫，英伟达收盘大跌超过 17%，单日市值蒸发 5890 亿美元 ，创下美国股市历史上最高纪录，这一波动背后，DeepSeek 被认为是重要因素之一。"""

# print(asyncio.run(extract_entity_relationship_agent(user_prompt)))
