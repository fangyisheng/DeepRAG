import networkx as nx
from pyvis.network import Network
import random
import asyncio
import uuid
import igraph as ig

async def store_graph_data_to_html(entity_relationship):

    # 创建有向关系图
    G = nx.Graph()

    # 存储实体和实体之间的关系
    for entity in entity_relationship["entities"]:
        G.add_node(entity["id"], text=entity["text"], type=entity["type"])
    
    for relationship in entity_relationship["relations"]:
        G.add_edge(relationship["head"], relationship["tail"], type=relationship["type"])
    g = ig.Graph.from_networkx(G)
    print(g)
    # 使用 PyVis 可视化
    net = Network(notebook=True, cdn_resources="in_line", height="750px", width="100%",bgcolor="#222222", font_color="white")

    # 将 NetworkX 图转换为 PyVis 图
    net.from_nx(G)
   
    color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    # 自定义节点和边的显示
    for node in net.nodes:
        
        node["label"] = f"{node['text']} ({node['type']})"  # 设置节点标签
        node["color"] = color
    for edge in net.edges:
    
        edge["title"] = edge["type"]  # 设置边的提示信息
        edge["color"] = color
    
    prefix = str(uuid.uuid4())
    net.show(f"{prefix}_graph.html")

    return 


test_data = {'entities': [{'id': 'a7ab0c52-3068-4622-825a-4a4a1b6daaad', 'text': 'Microsoft', 'type': 'company'}, {'id': 'dc244362-7747-48f4-8a00-16fb39f273fc', 'text': 'Satya Nadella', 'type': ['person', 'manager']}, {'id': 'ca4c99bf-66e0-426b-a40c-2ffce62a4529', 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 'Satya Nadella', 'tail': 'Microsoft', 'type': 'CEO of', 'id': '7477a645-1ead-4c65-a9e2-36666fa9a239'}, {'head': 'Microsoft', 'tail': 'Azure AI', 'type': ['developed', 'product'], 'id': '19c83af7-a526-4e06-985e-e7df0a2f8eca'}]}
asyncio.run(store_graph_data_to_html(test_data))



