import asyncio


# 今天3月7日要改完这个bug
async def describe_graph(graph: dict):
    graph_description_list = []
    for relation in graph["relations"]:
        relation_head_text = next(
            (
                entity["text"]
                for entity in graph["entities"]
                if entity["id"] == relation["head"]
            ),
            None,
        )
        relation_tail_text = next(
            (
                entity["text"]
                for entity in graph["entities"]
                if entity["id"] == relation["tail"]
            ),
            None,
        )

        if isinstance(relation["type"], str):
            graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{relation['type']}{relation_tail_text},{relation['description']}"
            graph_description_list.append(graph_description)
        else:
            for type in relation["type"]:
                graph_description = f"{relation_head_text}和{relation_tail_text}的关系是{relation_head_text}{type}{relation_tail_text},{relation['description']}"
                graph_description_list.append(graph_description)
    return graph_description_list


# test_data = {'entities': [{'id': '6bf47d6a-b2ad-4d44-bacf-abb99e9095b0', 'text': '深度求索（DeepSeek）', 'type': '组织'}, {'id': 'e64e6976-0b09-4e9a-aed8-c69b9aacca00', 'text': '全球 AI 领域', 'type': '领域'}, {'id': 'e0664b7b-f07f-4a8d-a6bc-ff8c8f651854', 'text': '2023 年', 'type': '时间'}, {'id': 'fea44ea1-9fb3-45be-aff5-2c5c9d969927', 'text': '美股市场', 'type': '地点'}, {'id': '83fb1ffc-e5d1-4a5d-ba2a-972a3a85e897', 'text': '1 月 27 日', 'type': '时间'}, {'id': '247279f0-fafe-46b7-9531-9c12a18263c5', 'text': '美股 AI、芯片股', 'type': '股票'}, {'id': '352860c5-0f59-4212-9243-05d64a2ad8a5', 'text': '英伟达', 'type': '组织'}, {'id': '800da448-15d9-42e0-adf1-c7fcd9c5d514', 'text': '美国股市', 'type': '地点'}], 'relations': [{'head': '6bf47d6a-b2ad-4d44-bacf-abb99e9095b0', 'tail': 'e64e6976-0b09-4e9a-aed8-c69b9aacca00', 'type': '在领域中崭露头角', 'description': '深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。', 'id': '5d89e03b-d883-4182-ba24-9c54ba5dd04b'}, {'head': '6bf47d6a-b2ad-4d44-bacf-abb99e9095b0', 'tail': 'e0664b7b-f07f-4a8d-a6bc-ff8c8f651854', 'type': '成立于', 'description': '深度求索（DeepSeek）成立于2023年。', 'id': 'b1c5cc8a-2bcf-42f2-9fc9-5f4ea2c6902e'}, {'head': '6bf47d6a-b2ad-4d44-bacf-abb99e9095b0', 'tail': 'fea44ea1-9fb3-45be-aff5-2c5c9d969927', 'type': '影响力体现在', 'description': '深度求索（DeepSeek）的影响力在美股市场有明显体现。', 'id': '1ac6d028-5783-4b36-a434-567d514ffea4'}, {'head': '83fb1ffc-e5d1-4a5d-ba2a-972a3a85e897', 'tail': '247279f0-fafe-46b7-9531-9c12a18263c5', 'type': '导致重挫', 'description': '1月27日，美股AI、芯片股重挫。', 'id': '5c30c479-0bce-4767-9937-d5473ead17aa'}, {'head': '247279f0-fafe-46b7-9531-9c12a18263c5', 'tail': '352860c5-0f59-4212-9243-05d64a2ad8a5', 'type': '影响公司股价', 'description': '英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。', 'id': '994c2c7a-bba9-4002-b17a-6c496ccb25ec'}, {'head': '352860c5-0f59-4212-9243-05d64a2ad8a5', 'tail': '800da448-15d9-42e0-adf1-c7fcd9c5d514', 'type': '创历史纪录', 'description': '创下美国股市历史上最高纪录。', 'id': 'f98c24b6-95e2-4dcb-bb0b-10b6d4c643b0'}, {'head': '6bf47d6a-b2ad-4d44-bacf-abb99e9095b0', 'tail': '247279f0-fafe-46b7-9531-9c12a18263c5', 'type': '被认为是重要因素', 'description': '深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。', 'id': '602cbe62-77a1-4672-8b15-c576f8b88dca'}]}


# print(asyncio.run(describe_graph(test_data)))
