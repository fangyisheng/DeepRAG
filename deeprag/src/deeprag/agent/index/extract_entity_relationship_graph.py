from deeprag.rag_core_utils.llm_api.llm_api_client import (
    llm_service,
    llm_service_stream,
)
from importlib import resources
import asyncio
import json
from loguru import logger
from deeprag.workflow.data_model import (
    FirstExtractedGraphData,
    EntityIdInt,
    RelationsInt,
    ExtractEntityRelationshipAgentResponse,
)


with (
    resources.files("deeprag.prompts.fixed_prompts")
    .joinpath("extract_entity_relationship_prompt.txt")
    .open("r") as file
):
    system_prompt = file.read()

# cot_prompt_chain1 = [{"role":"user","content":"""请用JSON结构化生成内容。输出格式参考如下：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": "0, "tail": 2, "type": "developed" } ] }
# 注意，可能会有同名的实体，请关注上下文正确区分同名的实体。给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的"""}]
# cot_prompt_chain1 = [
#     {
#         "role": "user",
#         "content": """请按照参考下面的输出格式：{ "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of","description":"Satya Nadella serves as the Chief Executive Officer of Microsoft, leading the company's overall strategy and direction." }, { "head": 0, "tail": 2, "type": "developed","description":"Microsoft developed Azure AI, a suite of cloud-based artificial intelligence services and tools aimed at empowering developers and organizations." } ] }
# 给定语料如果是中文，那么提取的实体类型是中文的，提取的关系也是中文的。不要输出其余解释性内容。
# 注意事项:关系字段必须包含head/tail/type/description这四个字段。实体字段必须包含id/text/type这三个字段。""",
#     }
# ]

# cot_prompt_chain2 = [
#     {
#         "role": "user",
#         "content": """请仅输出紧凑格式Compact Format的JSON，不要输出其余解释性内容""",
#     }
# ]

# cot_prompt = cot_prompt_chain1


async def extract_entity_relationship_agent(
    user_prompt: str,
) -> ExtractEntityRelationshipAgentResponse:
    response = await llm_service(system_prompt=system_prompt, user_prompt=user_prompt)
    response_dict_data = json.loads(response.assistant_response)
    # logger.info(f"这是提取的关系：{response}")
    extracted_entity_relationship_graph = FirstExtractedGraphData(
        entities=[EntityIdInt(**entity) for entity in response_dict_data["entities"]],
        relations=[
            RelationsInt(**relation) for relation in response_dict_data["relations"]
        ],
    )
    return ExtractEntityRelationshipAgentResponse(
        first_extracted_graph_data=extracted_entity_relationship_graph,
        cost_tokens=response.cost_tokens,
    )


# # 测试代码
# user_prompt = """深度求索 DeepSeek：AI 领域的新兴力量
# 过去几周，深度求索（DeepSeek）在全球 AI 领域掀起了一场风暴，成为众人瞩目的焦点。这家成立于 2023 年的年轻大模型公司，宛如一匹黑马，迅速在行业中崭露头角，其影响力甚至在美股市场都有明显体现。1 月 27 日，美股 AI、芯片股重挫，英伟达收盘大跌超过 17%，单日市值蒸发 5890 亿美元 ，创下美国股市历史上最高纪录，这一波动背后，DeepSeek 被认为是重要因素之一。
# 在自媒体和公众的视野里，DeepSeek 有着诸多令人瞩目的 “爽点”，被视为 “2025 年最燃爽文主角”。其一，“神秘力量弯道超车”。作为一家出身私募量化投资公司幻方量化的 AI 企业，此前讨论度并不高，却一举成为中国领先的 AI 公司，让许多人惊叹 “乱拳打死老师傅”。其二，“小力出奇迹”。DeepSeek-V3 模型训练成本约为 558 万美元，不到 OpenAI GPT-4o 模型的十分之一，性能却已接近，这似乎颠覆了 AI 行业长期信奉的 “大力出奇迹” 的规模定律。其三，“英伟达护城河消失”。DeepSeek 在论文中提到采用定制的 PTX 语言编程，被解读为 “绕开英伟达 CUDA 运算平台”，冲击了英伟达在 AI 硬件运算平台的优势地位。其四，“老外被打服了”。1 月 31 日，英伟达、微软、亚马逊等海外 AI 巨头纷纷接入 DeepSeek，引发了 “中国 AI 反超美国” 等一系列热议。
# 然而，热潮之下，也存在诸多误读。幻方量化早在 2017 年底就已在量化策略中采用 AI 模型计算，2019 年其深度学习训练平台 “萤火二号” 就搭载了约 1 万张英伟达 A100 显卡，比许多互联网大厂更早踏入大模型领域，并非毫无技术积累。而 DeepSeek-V3 模型的实际成本，由于前期研究等成本未计算在 558 万美元内，所以实际花费更大，它并非打破行业规律，而是通过更聪明的算法和架构提高效率 。同时，PTX 语言属于英伟达 CUDA 生态一环，虽然能激发硬件性能，但更换任务需重写程序，工作量巨大。另外，海外巨头接入 DeepSeek，只是将其模型部署在自家云服务上，是一种双赢合作，并非代表被 “打败”。自 2 月 5 日起，华为云、腾讯云、百度云等国内云厂商也陆续上线了 DeepSeek 模型，这表明 DeepSeek 在云服务合作方面全面开花。
# 除了这些争议点，DeepSeek 也有不少创新亮点。在模型架构上，它提出了全新的 MLA（一种新的多头潜在注意力机制）架构，将内存使用降低到过去最常用的 MHA 架构的 5%-13%，其独创的 DeepSeek MoEs Parse 结构也将计算成本降至最低，实现了成本的有效控制，这也是其能以相对低的成本进行模型训练的关键。在硅谷，DeepSeek 被称为 “来自东方的神秘力量” ，其技术实力得到了部分认可。
# 从用户体验来看，DeepSeek-R1 模型别具一格。当用户使用其 App 或网页版时，点击 “深度思考（R1）” 按钮，能展现完整的思考过程，这与绝大部分直接输出回答的大模型不同。例如用户提问 “A 大学和清华大学哪个更好？”，第一次回答 “清华大学”，追问 “我是 A 大学生，请重新回答”，则会得到答案 “A 大学好”，这一 “懂人情世故” 的表现引发群体惊叹。2 月 2 日，DeepSeek 登顶全球 140 个国家及地区的应用市场，上千万用户得以体验这一独特的深度思考功能。不过，这种推理范式并非 DeepSeek 首创，OpenAI 的 o1 模型才是开创者，只是 OpenAI o1 模型不开源、不公布技术细节且收费高，导致其难以出圈，而 DeepSeek-R1 模型免费让全球用户体验，从而取得了全球性的成功。
# 在市场合作方面，DeepSeek 动作频频。2 月 12 日，周鸿祎在纳米 AI 搜索 “百车行动” 活动中提到，去年 8 月纳米 AI 搜索就和 DeepSeek 建立联系并进行了接入和本地化部署，搭建高速机房、采购上万块算力卡，集成了 DeepSeek 满血版和高速版。纳米 AI 搜索手机版加入 DeepSeek 后，在不到两周时间获得 2000 万用户。此外，包括华为、阿里、百度、腾讯、京东等在内的多家云平台宣布接入 DeepSeek 大模型，三家基础电信企业均全面接入，金融行业的多家券商、银行、公募基金等也纷纷接入。小鹏汽车董事长何小鹏也表示对于小鹏汽车接入 DeepSeek 大模型 “可以期待”。
# """


# print(asyncio.run(extract_entity_relationship_agent(user_prompt)))
