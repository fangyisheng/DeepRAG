from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
from importlib import resources
import asyncio

with (
    resources.files("deeprag.prompts")
    .joinpath("sentence_agent_pattern_prompt.txt")
    .open("r") as file
):
    system_prompt = file.read()

cot_prompt = [
    {
        "role": "user",
        "content": """请用JSON结构化生成内容。输出格式：{"retrival_type":""}""",
    }
]


async def sentence_agent_pattern_agent(user_prompt):
    response = await llm_service(
        system_prompt=system_prompt, user_prompt=user_prompt, cot_prompt=cot_prompt
    )
    return response


# print(asyncio.run(sentence_agent_pattern_agent("我刚刚上传的文档的宗旨是什么？")))
