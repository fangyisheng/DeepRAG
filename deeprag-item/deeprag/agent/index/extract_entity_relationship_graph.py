from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
from importlib import resources
import asyncio
import json
from loguru import logger

with resources.files("deeprag.prompts.fixed_prompts").joinpath("extract_entity_relationship_prompt.txt").open("r") as file:
    system_prompt = file.read()
    
# cot_prompt_chain1 = [{"role":"user","content":"""请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": "0, "tail": 2, "type": "developed" } ] }
# 注意，可能会有同名的实体，请关注上下文正确区分同名的实体。给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的"""}]
cot_prompt_chain1 = [{"role":"user","content":"""请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of","description":"" }, { "head": "0, "tail": 2, "type": "developed","description":"" } ] }
给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的"""}]

cot_prompt_chain2 = [{"role":"user","content":"""请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容"""}]

cot_prompt = cot_prompt_chain1 + cot_prompt_chain2

async def extract_entity_relationship_agent(user_prompt):
    response = await llm_service(system_prompt = system_prompt,
                           user_prompt = user_prompt,cot_prompt = cot_prompt)
    logger.info(f"这是提取的图结构：{response}")
    return json.loads(response)


# user_prompt = """9.3.3楼面均布活荷载标准值应按表9.3.3取值：注：设计楼面梁、墙、柱及基础时，上述楼面荷载标准值折减系数按国家现行规范《建筑结构荷载规范》GB50009-2012的规定取值。9.3.4屋面均布活荷载标准值应按表9.3.4取值：9.3.5基本风压应按国家现行规范《建筑结构荷载规范》GB50009的规定采用，对于房屋高度大于60m的高层住宅承载力设计时应按基本风压的1.1倍采用。9.3.6地基承载力验算，天然地基及复合地基均应按下列公式进行承载力验算：1轴心荷载作用下应符合下式要求：式中：kp—相应于荷载效应标准组合时，基础底面处的平均压力值；Fk—相应于荷载效应标准组合时，上部结构传至基础顶面的竖向力值；Gk—基础自重与基础上的土重之和；A—基础底面面积；fa—深宽修正后的地基承载力标准值。"""

# print(asyncio.run(extract_entity_relationship_agent(user_prompt)))

