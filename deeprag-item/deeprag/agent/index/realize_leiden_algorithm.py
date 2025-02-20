import networkx as nx
import igraph as ig
import leidenalg
import asyncio


async def realize_leiden_community_algorithm(graph_data):
    G = []
    for relation in graph_data["relations"]:
        G.append((relation["head"],relation["tail"]))
    g = ig.Graph.from_networkx(G)
    partition = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition)
    community_membership = partition.membership























test_data = {'entities': [{'id': 'a7ab0c52-3068-4622-825a-4a4a1b6daaad', 'text': 'Microsoft', 'type': 'company'}, {'id': 'dc244362-7747-48f4-8a00-16fb39f273fc', 'text': 'Satya Nadella', 'type': ['person', 'manager']}, {'id': 'ca4c99bf-66e0-426b-a40c-2ffce62a4529', 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 'Satya Nadella', 'tail': 'Microsoft', 'type': 'CEO of', 'id': '7477a645-1ead-4c65-a9e2-36666fa9a239'}, {'head': 'Microsoft', 'tail': 'Azure AI', 'type': ['developed', 'product'], 'id': '19c83af7-a526-4e06-985e-e7df0a2f8eca'}]}

print(asyncio.run(realize_leiden_community_algorithm(test_data)))