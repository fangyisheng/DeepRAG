from deeprag.prompts.dynamic_prompts.generate_community_report_prompt import generate_community_report_prompt_content
from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
import json


#使用了思维链的提示词工程方法
async def generate_community_agent(entity_relation_description:list):
    entity_relation_description_string = "。".join(entity_relation_description)
    
    system_prompt = generate_community_report_prompt_content(entity_relation_description_string)
  
    
    response = await llm_service(system_prompt=system_prompt)
    print(response)
    context_history = [{"role":"user","content":"""请输出社区检测报告"""}]+[{"role":"assistant","content":f"""{response}"""}]
    user_prompt = """请用JSON结构化生成内容。输出格式参考如下：{"title":"","origin_description":"","summary":""}"""
    cot_prompt = [{"role":"user","content":"""请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容"""}]
    final_response = await llm_service(system_prompt=system_prompt,context_histroy=context_history,user_prompt=user_prompt,cot_prompt=cot_prompt)
    return json.loads(final_response)

# #现在测试一下这个功能

# import asyncio
# entity_relation_description = ["微软的CEO是印度人","印度人之间的关系很好"]

# print(asyncio.run(generate_community_agent(entity_relation_description)))