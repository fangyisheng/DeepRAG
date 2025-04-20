import networkx as nx
import igraph as ig
import leidenalg
import asyncio
from pyvis.network import Network
import random
import uuid


async def realize_leiden_community_algorithm(graph_data):
    G = nx.DiGraph()
    for entity in graph_data["entities"]:
        G.add_node(entity["id"], text=entity["text"], type=entity["type"])
    for relation in graph_data["relations"]:
        G.add_edge(relation["head"], relation["tail"], type=relation["type"])
        # type作为这条边的属性 attribute
    g = ig.Graph.from_networkx(G)
    partition = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition)
    community_membership = partition.membership

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

    # 做好不同社区的颜色映射

    community_color = {}
    for community in community_membership:
        community_color[community] = (
            f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        )

    for i, community in enumerate(community_membership):
        color = community_color[community]
        community = community_membership[i]
        net.nodes[i]["label"] = (
            f"{net.nodes[i]['text']} ({net.nodes[i]['type']})"  # 设置节点标签
        )
        net.nodes[i]["title"] = f"Community {community}"
        net.nodes[i]["color"] = color

    for edge in net.edges:
        color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        if len(edge["type"]) > 1:
            edge["label"] = str(edge["type"])  # 设置边的提示信息
        else:
            edge["label"] = edge["type"]
        edge["color"] = color

    prefix = str(uuid.uuid4())
    net.show(f"{prefix}_graph_with_leiden.html")

    return


# test_data = {"entities": [{"id": "1a320717-8765-451e-9c1c-6648519d5632", "text": "Microsoft", "type": "company"}, {"id": "ea3432d9-972a-43da-9fab-89a2bb6b950f", "text": "Satya Nadella", "type": ["person", "manager"]}, {"id": "0d98dd23-042e-4a28-8cbc-a8050b9d9366", "text": "Azure AI", "type": "product"}], "relations": [{"head": "ea3432d9-972a-43da-9fab-89a2bb6b950f", "tail": "1a320717-8765-451e-9c1c-6648519d5632", "type": "CEO of", "id": "af28a2d6-a543-4254-914d-7bc7bdb4947f"}, {"head": "1a320717-8765-451e-9c1c-6648519d5632", "tail": "0d98dd23-042e-4a28-8cbc-a8050b9d9366", "type": ["developed", "product"], "id": "6c5720bd-03c1-4dba-be87-5bcd03856408"}]}
# asyncio.run(realize_leiden_community_algorithm(test_data))
