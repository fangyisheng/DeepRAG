import asyncio

async def describe_graph(graph):
    graph_description_list = []
    for relation in graph["relations"]:
        if isinstance(relation["type"],str):
            graph_description = f"{relation["head"]}和{relation["tail"]}的关系是{relation["head"]}{relation["type"]}{relation["tail"]}"
            graph_description_list.append(graph_description)
        else:
            for type in relation["type"]:
                graph_description = f"{relation["head"]}和{relation["tail"]}的关系是{relation["head"]}{type}{relation["tail"]}"
                graph_description_list.append(graph_description)
    return graph_description_list

# 测试通过
# test_data = {'entities': [{'id': 'fd24920c-b025-474f-b2db-c962a9cffe33', 'text': 'Microsoft', 'type': 'company'}, {'id': 'd0cf5587-b703-48b7-a75b-3729c93c6f61', 'text': 'Satya Nadella', 'type': ['person', 'manager']}, {'id': '6adef422-5f7f-43f5-8770-e4bf930073b6', 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 'Satya Nadella', 'tail': 'Microsoft', 'type': 'CEO of', 'id': 'b6cb2adf-540d-448a-b198-8e841ba92c96'}, {'head': 'Microsoft', 'tail': 'Azure AI', 'type': ['developed', 'product'], 'id': 'b28a1ddc-4d69-4948-9f7f-e8eb5863c4ff'}]}
# print(asyncio.run(describe_graph(test_data)))

