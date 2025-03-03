import networkx as nx
import igraph as ig
import leidenalg
import asyncio


#在这里实现leiden算法之前，还需要将networkx图转换为igraph图，同时igraph图的id字段是整数，这个要非常注意，所以要做一个字典映射

# async def realize_leiden_community_algorithm(graph_data):
#     G = nx.DiGraph()
#     for relation in graph_data["relations"]:
#         G.add_edge(relation["head"],relation["tail"])
    
#     node_mapping = {node: idx for idx, node in enumerate(G.nodes())}
#     edges = [(node_mapping[u], node_mapping[v]) for u, v in G.edges()]
#     print(G)
#     print(G.edges)
#     print(G.nodes)
    # g = ig.Graph.from_networkx(G)
    # partition = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition)
    # community_membership = partition.membership

test_data = {'entities': [{'id': '1a320717-8765-451e-9c1c-6648519d5632', 'text': 'Microsoft', 'type': 'company'}, {'id': 'ea3432d9-972a-43da-9fab-89a2bb6b950f', 'text': 'Satya Nadella', 'type': ['person', 'manager']}, {'id': '0d98dd23-042e-4a28-8cbc-a8050b9d9366', 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 'ea3432d9-972a-43da-9fab-89a2bb6b950f', 'tail': '1a320717-8765-451e-9c1c-6648519d5632', 'type': 'CEO of', 'id': 'af28a2d6-a543-4254-914d-7bc7bdb4947f'}, {'head': '1a320717-8765-451e-9c1c-6648519d5632', 'tail': '0d98dd23-042e-4a28-8cbc-a8050b9d9366', 'type': ['developed', 'product'], 'id': '6c5720bd-03c1-4dba-be87-5bcd03856408'}]}


async def realize_leiden_community_algorithm(graph_data):
    G = nx.DiGraph()
    for entity in graph_data["entities"]:
        G.add_node(entity["id"], text = entity["text"], type = entity["type"])
    for relation in graph_data["relations"]:
        G.add_edge(relation["head"], relation["tail"], type = relation["type"])
    print(G)
asyncio.run(realize_leiden_community_algorithm(test_data))
   






















test_data = {'entities': [{'id': 'a7ab0c52-3068-4622-825a-4a4a1b6daaad', 'text': 'Microsoft', 'type': 'company'}, {'id': 'dc244362-7747-48f4-8a00-16fb39f273fc', 'text': 'Satya Nadella', 'type': ['person', 'manager']}, {'id': 'ca4c99bf-66e0-426b-a40c-2ffce62a4529', 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 'Satya Nadella', 'tail': 'Microsoft', 'type': 'CEO of', 'id': '7477a645-1ead-4c65-a9e2-36666fa9a239'}, {'head': 'Microsoft', 'tail': 'Azure AI', 'type': ['developed', 'product'], 'id': '19c83af7-a526-4e06-985e-e7df0a2f8eca'}]}

print(asyncio.run(realize_leiden_community_algorithm(test_data)))