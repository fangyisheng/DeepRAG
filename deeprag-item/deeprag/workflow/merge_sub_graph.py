import uuid
import json


async def merge_sub_entity_relationship_graph(entity_relationship_graphs: list):
    """
    entity_relationship_graphs是一个关于字典的列表[{},{},{}]

    """
    merged_graph = {"entities": [], "relations": []}

    # 下面两段for循环的作用是将提取的图结构中的语义不明确的关系的实体的id填充完整，head和tail

    # 这段循环的作用是先把字典列表中的每一个dict的relation的head和tail用真正的text填充了
    for graph in entity_relationship_graphs:
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

    for dict in entity_relationship_graphs:
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
                    existing_text["type"] = [existing_text["type"], entity["type"]]

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
            if existing_relation:
                if existing_relation["type"] != relation["type"]:
                    existing_relation["type"] = [
                        existing_relation["type"],
                        entity["type"],
                    ]
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

    return merged_graph


# import asyncio

# # 下面这个test_data是大模型生成的子图列表的mock数据
# test_data = [
#     {
#         "entities": [
#             {"id": 0, "text": "深度求索（DeepSeek）", "type": "组织"},
#             {"id": 1, "text": "全球 AI 领域", "type": "领域"},
#             {"id": 2, "text": "2023 年", "type": "时间"},
#             {"id": 3, "text": "美股市场", "type": "地点"},
#             {"id": 4, "text": "1 月 27 日", "type": "时间"},
#             {"id": 5, "text": "美股 AI、芯片股", "type": "股票"},
#             {"id": 6, "text": "英伟达", "type": "组织"},
#             {"id": 7, "text": "美国股市", "type": "地点"},
#         ],
#         "relations": [
#             {
#                 "head": 0,
#                 "tail": 1,
#                 "type": "在领域中崭露头角",
#                 "description": "深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。",
#             },
#             {
#                 "head": 0,
#                 "tail": 2,
#                 "type": "成立于",
#                 "description": "深度求索（DeepSeek）成立于2023年。",
#             },
#             {
#                 "head": 0,
#                 "tail": 3,
#                 "type": "影响力体现在",
#                 "description": "深度求索（DeepSeek）的影响力在美股市场有明显体现。",
#             },
#             {
#                 "head": 4,
#                 "tail": 5,
#                 "type": "导致重挫",
#                 "description": "1月27日，美股AI、芯片股重挫。",
#             },
#             {
#                 "head": 5,
#                 "tail": 6,
#                 "type": "影响公司股价",
#                 "description": "英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。",
#             },
#             {
#                 "head": 6,
#                 "tail": 7,
#                 "type": "创历史纪录",
#                 "description": "创下美国股市历史上最高纪录。",
#             },
#             {
#                 "head": 0,
#                 "tail": 5,
#                 "type": "被认为是重要因素",
#                 "description": "深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
#             },
#         ],
#     }
# ]
# print(asyncio.run(merge_sub_entity_relationship_graph(test_data)))
