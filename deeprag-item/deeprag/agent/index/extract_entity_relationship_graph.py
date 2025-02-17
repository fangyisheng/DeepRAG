from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
from importlib import resources
import asyncio
from loguru import logger

with resources.files("deeprag.prompts.fixed_prompts").joinpath("extract_entity_relationship_prompt.txt").open("r") as file:
    system_prompt = file.read()
    
# cot_prompt_chain1 = [{"role":"user","content":"""请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": "0, "tail": 2, "type": "developed" } ] }
# 注意，可能会有同名的实体，请关注上下文正确区分同名的实体。给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的"""}]
cot_prompt_chain1 = [{"role":"user","content":"""请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": "0, "tail": 2, "type": "developed" } ] }
给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的"""}]

cot_prompt_chain2 = [{"role":"user","content":"""请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容"""}]

cot_prompt = cot_prompt_chain1 + cot_prompt_chain2

async def extract_entity_relationship_agent(user_prompt):
    response = await llm_service(system_prompt = system_prompt,
                           user_prompt = user_prompt,cot_prompt = cot_prompt)
    logger.info(f"这是提取的图结构：{response}")
    return response


# # user_prompt = """9.3.3楼面均布活荷载标准值应按表9.3.3取值：注：设计楼面梁、墙、柱及基础时，上述楼面荷载标准值折减系数按国家现行规范《建筑结构荷载规范》GB50009-2012的规定取值。9.3.4屋面均布活荷载标准值应按表9.3.4取值：9.3.5基本风压应按国家现行规范《建筑结构荷载规范》GB50009的规定采用，对于房屋高度大于60m的高层住宅承载力设计时应按基本风压的1.1倍采用。9.3.6地基承载力验算，天然地基及复合地基均应按下列公式进行承载力验算：1轴心荷载作用下应符合下式要求：式中：kp—相应于荷载效应标准组合时，基础底面处的平均压力值；Fk—相应于荷载效应标准组合时，上部结构传至基础顶面的竖向力值；Gk—基础自重与基础上的土重之和；A—基础底面面积；fa—深宽修正后的地基承载力标准值。2偏心荷载作用下,除应符合本规范式（9.3.6-1）外，并应符合下式要求：式中:Pkmax—相应于荷载效应标准组合时，基础底面边缘处最大压力值；Mk—相应于荷载效应标准组合时，作用于基础底面的力矩值；W—基础底面的抵抗矩。3当考虑地震作用时应按下列公式计算式中faE—调整后的地基抗震承载力；a—地基抗震承载力调整系数，应按现行国家标准《建筑抗震设计规范》GB50011中表4.2.3采用；p—地震作用效应标准组合的基础底面平均压力；pmax—地震作用效应标准组合的基础边缘的最大压力。4地基压缩层范围有软弱下卧层时，应按下式验算软弱下卧层的地基承载力。式中Poz—相应于荷载效应标准组合时，软弱下卧层顶面处的附加压力值（kPa）；Pcz—软弱下卧层顶面处土的自重压力值（kPa）；faz—软弱下卧层顶面处经深度修正后的地基承载力标准值（kPa）。#9.4地基基础设计9.4.1住宅建筑选择建造场地时，应根据工程需要及北京地震活动情况、工程地质和地震地质的有关资料，对抗震有利、一般、不利和危险地段做出评价。对不利地段，应尽量避开，当无法避开时应采取有效的措施。不应在危险地段建造住宅。"""
# user_prompt = """张三是一名医生也是一名老师,张三曾经在上海做过建筑工人"""

# user_prompt_1 = """张三曾经在上海做过建筑工人。李四是张三的别名"""

# print(cot_prompt_chain1)
# print(asyncio.run(extract_entity_relationship_agent(user_prompt_1)))

