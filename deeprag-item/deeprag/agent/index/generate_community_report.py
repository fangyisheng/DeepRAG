from deeprag.prompts.dynamic_prompts.generate_community_report_prompt import (
    generate_community_report_prompt_content,
)
from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
import json
from pydantic import BaseModel
from loguru import logger


class CommunityReportStructedData(BaseModel):
    title: str
    origin_description: str
    summary: str


class GenerateCommunityReportResponse(BaseModel):
    community_report: str
    community_report_structed_data: CommunityReportStructedData


# 使用了思维链的提示词工程方法
# 根据输入的属于某个特定社区的关系描述，得到社区检测报告
async def generate_community_report_agent(
    entity_relation_description: list,
) -> dict[str, str]:
    entity_relation_description_string = "。".join(entity_relation_description)

    system_prompt = generate_community_report_prompt_content(
        entity_relation_description_string
    )

    response = await llm_service(system_prompt=system_prompt)
    context_history = [{"role": "user", "content": """请输出社区检测报告"""}] + [
        {"role": "assistant", "content": f"""{response}"""}
    ]
    user_prompt = """请用JSON结构化生成内容。输出格式参考如下：{"title":"","origin_description":"","summary":""}"""
    cot_prompt = [
        {
            "role": "user",
            "content": """请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容""",
        }
    ]
    final_response = await llm_service(
        system_prompt=system_prompt,
        context_histroy=context_history,
        user_prompt=user_prompt,
        cot_prompt=cot_prompt,
    )
    logger.info(f"这是community_report_agent的输出：{final_response}")
    final_response_dict = json.loads(final_response)
    community_report = f"""社区标题：{final_response_dict["title"]}，原来的知识图谱描述：{final_response_dict["origin_description"]}，总结：{final_response_dict["summary"]}"""
    return GenerateCommunityReportResponse(
        community_report=community_report,
        community_report_structed_data=final_response_dict,
    )


# # 现在测试一下这个功能

# import asyncio

# entity_relation_description = ["微软的CEO是印度人", "印度人之间的关系很好"]

# print(asyncio.run(generate_community_report_agent(entity_relation_description)))
