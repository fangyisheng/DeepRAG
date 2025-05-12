import uuid
import json
from deeprag.workflow.data_model import (
    BatchTextChunkGenerateGraphsResponse,
    CompleteGraphData,
    FirstExtractedGraphData,
    RelationsInt,
    RelationsStr,
    EntityIdInt,
    EntityIdStr,
)


import uuid
import json
from deeprag.workflow.data_model import (
    BatchTextChunkGenerateGraphsResponse,
    CompleteGraphData,
)
from loguru import logger


async def merge_sub_entity_relationship_graph(
    entity_relationship_graphs: BatchTextChunkGenerateGraphsResponse,
) -> CompleteGraphData:
    """_summary_

    Args:
        entity_relationship_graphs (list): 子图元素组成的列表

    Returns:
        dict: 完整图的字典
    """
    merged_graph = {"entities": [], "relations": []}
    entity_relationship_graphs_to_list = [
        graph_data.model_dump() for graph_data in entity_relationship_graphs.root
    ]

    # 下面两段for循环的作用是将提取的图结构中的语义不明确的关系的实体的id填充完整，head和tail

    # 这段循环的作用是先把字典列表中的每一个dict的relation的head和tail用真正的text填充了
    for graph in entity_relationship_graphs_to_list:
        for relation in graph["relations"]:
            relation["head"] = next(
                (
                    item["text"]
                    for item in graph["entities"]
                    if item["id"] == relation["head"]
                ),
                None,
            )
            relation["tail"] = next(
                (
                    item["text"]
                    for item in graph["entities"]
                    if item["id"] == relation["tail"]
                ),
                None,
            )

    for dict in entity_relationship_graphs_to_list:
        for entity in dict["entities"]:
            existing_text = next(
                (
                    item
                    for item in merged_graph["entities"]
                    if item.get("text") == entity["text"]
                ),
                None,
            )
            if existing_text:
                existing_text["id"] = str(uuid.uuid4())
                if existing_text["type"] != entity["type"]:
                    existing_types = existing_text["type"]
                    new_types = entity["type"]

                    if not isinstance(existing_types, list):
                        existing_types = [existing_types]
                    if not isinstance(new_types, list):
                        new_types = [new_types]

                    existing_text["type"] = list(set(existing_types + new_types))

            else:
                entity["id"] = str(uuid.uuid4())
                merged_graph["entities"].append(entity)
        for relation in dict["relations"]:
            existing_relation = next(
                (
                    item
                    for item in merged_graph["relations"]
                    if item.get("head") == relation["head"]
                    and item.get("tail") == relation["tail"]
                ),
                None,
            )
            logger.info(f"{existing_relation}")
            if existing_relation:
                if existing_relation["type"] != relation["type"]:
                    existing_types = existing_relation["type"]
                    new_types = relation["type"]

                    if not isinstance(existing_types, list):
                        existing_types = [existing_types]
                    if not isinstance(new_types, list):
                        new_types = [new_types]

                    existing_relation["type"] = list(set(existing_types + new_types))

            else:
                relation["id"] = str(uuid.uuid4())
                merged_graph["relations"].append(relation)

    for relation in merged_graph["relations"]:
        relation["head"] = next(
            (
                entity["id"]
                for entity in merged_graph["entities"]
                if entity["text"] == relation["head"]
            ),
            None,
        )
        relation["tail"] = next(
            (
                entity["id"]
                for entity in merged_graph["entities"]
                if entity["text"] == relation["tail"]
            ),
            None,
        )
    logger.info(f"{merged_graph}")

    return CompleteGraphData(**merged_graph)


# # 编写测试代码
# import asyncio

# # 下面这个test_data是大模型生成的子图列表的mock数据
# test_data = BatchTextChunkGenerateGraphsResponse(
#     root=[
#         FirstExtractedGraphData(
#             entities=[
#                 EntityIdInt(text="深度求索", type="组织", id=0),
#                 EntityIdInt(text="DeepSeek", type="产品", id=1),
#                 EntityIdInt(text="AI领域", type="领域", id=2),
#                 EntityIdInt(text="美股市场", type="地点", id=3),
#                 EntityIdInt(text="英伟达", type="组织", id=4),
#                 EntityIdInt(text="幻方量化", type="组织", id=5),
#                 EntityIdInt(text="OpenAI", type="组织", id=6),
#                 EntityIdInt(text="GPT-4o", type="产品", id=7),
#                 EntityIdInt(text="华为云", type="产品", id=8),
#                 EntityIdInt(text="腾讯云", type="产品", id=9),
#                 EntityIdInt(text="百度云", type="产品", id=10),
#                 EntityIdInt(text="MLA架构", type="技术", id=11),
#                 EntityIdInt(text="MHA架构", type="技术", id=12),
#                 EntityIdInt(text="DeepSeek MoEs Parse结构", type="技术", id=13),
#                 EntityIdInt(text="DeepSeek-R1模型", type="产品", id=14),
#                 EntityIdInt(text="清华大学", type="地点", id=15),
#                 EntityIdInt(text="A大学", type="地点", id=16),
#                 EntityIdInt(text="硅谷", type="地点", id=17),
#             ],
#             relations=[
#                 RelationsInt(
#                     type="开发", description="深度求索开发了DeepSeek。", head=0, tail=1
#                 ),
#                 RelationsInt(
#                     type="属于", description="DeepSeek属于AI领域。", head=1, tail=2
#                 ),
#                 RelationsInt(
#                     type="影响",
#                     description="DeepSeek在美股市场产生影响。",
#                     head=1,
#                     tail=3,
#                 ),
#                 RelationsInt(
#                     type="上市", description="英伟达在美股市场上市。", head=4, tail=3
#                 ),
#                 RelationsInt(
#                     type="孵化", description="幻方量化孵化了深度求索。", head=5, tail=0
#                 ),
#                 RelationsInt(
#                     type="开发", description="OpenAI开发了GPT-4o。", head=6, tail=7
#                 ),
#                 RelationsInt(
#                     type="合作", description="华为云与DeepSeek合作。", head=8, tail=1
#                 ),
#                 RelationsInt(
#                     type="合作", description="腾讯云与DeepSeek合作。", head=9, tail=1
#                 ),
#                 RelationsInt(
#                     type="合作", description="百度云与DeepSeek合作。", head=10, tail=1
#                 ),
#                 RelationsInt(
#                     type="提出", description="深度求索提出了MLA架构。", head=11, tail=0
#                 ),
#                 RelationsInt(
#                     type="采用",
#                     description="深度求索采用了DeepSeek MoEs Parse结构。",
#                     head=13,
#                     tail=0,
#                 ),
#                 RelationsInt(
#                     type="开发",
#                     description="深度求索开发了DeepSeek-R1模型。",
#                     head=14,
#                     tail=0,
#                 ),
#                 RelationsInt(
#                     type="对比",
#                     description="DeepSeek-R1模型对清华大学和A大学进行对比。",
#                     head=15,
#                     tail=16,
#                 ),
#                 RelationsInt(
#                     type="认可",
#                     description="硅谷认可了深度求索的技术实力。",
#                     head=17,
#                     tail=0,
#                 ),
#             ],
#         ),
#         FirstExtractedGraphData(
#             entities=[
#                 EntityIdInt(text="OpenAI", type=["组织,公司"], id=0),
#                 EntityIdInt(text="o1", type="模型", id=1),
#                 EntityIdInt(text="DeepSeek-R1", type="模型", id=2),
#                 EntityIdInt(text="周鸿祎", type="人物", id=3),
#                 EntityIdInt(text="纳米 AI 搜索", type="产品", id=4),
#                 EntityIdInt(text="DeepSeek", type="组织", id=5),
#                 EntityIdInt(text="小鹏汽车", type="组织", id=6),
#                 EntityIdInt(text="何小鹏", type="人物", id=7),
#                 EntityIdInt(text="华为", type="组织", id=8),
#                 EntityIdInt(text="阿里", type="组织", id=9),
#                 EntityIdInt(text="百度", type="组织", id=10),
#                 EntityIdInt(text="腾讯", type="组织", id=11),
#                 EntityIdInt(text="京东", type="组织", id=12),
#             ],
#             relations=[
#                 RelationsInt(
#                     type="隶属于", description="o1模型由OpenAI开发", head=1, tail=0
#                 ),
#                 RelationsInt(
#                     type="隶属于",
#                     description="DeepSeek-R1模型由DeepSeek发布",
#                     head=2,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="参与",
#                     description="周鸿祎参与纳米AI搜索活动并提到与DeepSeek的合作",
#                     head=3,
#                     tail=4,
#                 ),
#                 RelationsInt(
#                     type="合作",
#                     description="纳米AI搜索与DeepSeek建立联系并进行本地化部署",
#                     head=4,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="可能合作",
#                     description="小鹏汽车可能接入DeepSeek大模型",
#                     head=6,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="担任", description="何小鹏担任小鹏汽车董事长", head=7, tail=6
#                 ),
#                 RelationsInt(
#                     type="合作",
#                     description="华为宣布接入DeepSeek大模型",
#                     head=8,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="合作",
#                     description="阿里宣布接入DeepSeek大模型",
#                     head=9,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="合作",
#                     description="百度宣布接入DeepSeek大模型",
#                     head=10,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="合作",
#                     description="腾讯宣布接入DeepSeek大模型",
#                     head=11,
#                     tail=5,
#                 ),
#                 RelationsInt(
#                     type="合作",
#                     description="京东宣布接入DeepSeek大模型",
#                     head=12,
#                     tail=5,
#                 ),
#             ],
#         ),
#     ]
# )

# data = asyncio.run(merge_sub_entity_relationship_graph(test_data))
# print(data)
