import uuid


def add_community_id(data, community_ids):
    """
    给知识图谱数据中的 entities 添加 community_id。

    Args:
        data: 知识图谱数据 (字典).
        community_ids: 社区划分结果 (列表).

    Returns:
        修改后的知识图谱数据 (字典).
    """

    if len(data["entities"]) != len(community_ids):
        raise ValueError("entities 的数量必须与 community_ids 的长度相等")

    community_id_map = {}  # 存储社区ID到 UUID 的映射，确保相同社区ID对应相同 UUID

    for i, entity in enumerate(data["entities"]):
        community_id = community_ids[i]

        if community_id not in community_id_map:
            community_id_map[community_id] = str(uuid.uuid4())  # 为新的社区ID生成 UUID

        entity["community_id"] = community_id_map[community_id]  # 从映射中获取 UUID

    return data


# 示例用法
community_ids = [0, 0, 1]
test_data = {
    "entities": [
        {
            "id": "1a320717-8765-451e-9c1c-6648519d5632",
            "text": "Microsoft",
            "type": "company",
        },
        {
            "id": "ea3432d9-972a-43da-9fab-89a2bb6b950f",
            "text": "Satya Nadella",
            "type": ["person", "manager"],
        },
        {
            "id": "0d98dd23-042e-4a28-8cbc-a8050b9d9366",
            "text": "Azure AI",
            "type": "product",
        },
    ],
    "relations": [
        {
            "head": "ea3432d9-972a-43da-9fab-89a2bb6b950f",
            "tail": "1a320717-8765-451e-9c1c-6648519d5632",
            "type": "CEO of",
            "id": "af28a2d6-a543-4254-914d-7bc7bdb4947f",
        },
        {
            "head": "1a320717-8765-451e-9c1c-6648519d5632",
            "tail": "0d98dd23-042e-4a28-8cbc-a8050b9d9366",
            "type": ["developed", "product"],
            "id": "6c5720bd-03c1-4dba-be87-5bcd03856408",
        },
    ],
}

print(add_community_id(test_data, community_ids))
