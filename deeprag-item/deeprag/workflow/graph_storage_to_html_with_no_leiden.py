import networkx as nx
from pyvis.network import Network
import random
import asyncio
import uuid
import igraph as ig


async def store_graph_data_to_html_with_no_leiden(entity_relationship):
    # 创建有向关系图 如果是nx.Graph()则是创建了无向图，(u,v)和(v,u)等价
    G = nx.DiGraph()
    # 存储实体和实体之间的关系
    for entity in entity_relationship["entities"]:
        G.add_node(entity["id"], text=entity["text"], type=entity["type"])

    for relation in entity_relationship["relations"]:
        G.add_edge(relation["head"], relation["tail"], type=relation["type"])

    # G的数据格式没问题了

    # 使用 PyVis 可视化
    net = Network(
        notebook=True,
        cdn_resources="in_line",
        height="750px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=True,
    )
    net.set_options("""
    {
    "physics": {
        "enabled": true,
        "barnesHut": {
        "gravitationalConstant": -2000,
        "springLength": 400,
        "springConstant": 0.04
        },
        "minVelocity": 0.75,
        "stabilization": {
        "enabled": true,
        "iterations": 1000,
        "updateInterval": 100,
        "onlyDynamicEdges": false,
        "fit": true
        }
    }
    }
    """)

    # 将 NetworkX 图转换为 PyVis 图
    net.from_nx(G)

    color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    # # 自定义节点和边的显示
    for node in net.nodes:
        # 在pyvis中label字段用于节点的显示标签，如果没有这个label，就会取node的id字段，通常id字段都是uuid什么的，容易不太好看，所以设置一下label标签
        node["label"] = f"{node['text']} ({node['type']})"  # 设置节点标签
        node["color"] = color
    for edge in net.edges:
        if len(edge["type"]) > 1:
            edge["label"] = str(edge["type"])  # 设置边的提示信息
        else:
            edge["label"] = edge["type"]
        edge["color"] = color

    prefix = str(uuid.uuid4())
    # 这块net.show先保留了，方便以后做测试
    net.show(f"{prefix}_graph_with_no_leiden.html")
    html_content = net.generate_html()

    return html_content


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

asyncio.run(store_graph_data_to_html_with_no_leiden(test_data))
