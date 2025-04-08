import networkx as nx
import igraph as ig
import leidenalg
import asyncio
import uuid
import networkx as nx
import igraph as ig
import leidenalg
import asyncio
from pyvis.network import Network
import random
import uuid
from typing import Tuple

# 在这里实现leiden算法之前，还需要将networkx图转换为igraph图，同时igraph图的id字段是整数，这个要非常注意，所以要做一个字典映射
from deeprag.workflow.data_model import (
    GraphDataAddCommunityWithVisualization,
    CompleteGraphData,
)


async def realize_leiden_community_algorithm(
    graph_data: CompleteGraphData,
) -> GraphDataAddCommunityWithVisualization:
    """

    将leiden算法应用于
    """
    G = nx.DiGraph()
    for entity in graph_data["entities"]:
        G.add_node(entity["id"], text=entity["text"], type=entity["type"])

    for relation in graph_data["relations"]:
        G.add_edge(relation["head"], relation["tail"], type=relation["type"])
        # type作为这条边的属性 attribute
    # for node, attributes in G.nodes(data=True):
    #     print(f"Node: {node}, Attributes: {attributes}")
    g = ig.Graph.from_networkx(G)
    partition = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition)
    community_membership = partition.membership

    community_id_map = {}  # 存储community_id,例如community_membership:[0,0,1]到uuid的映射，相同的数字是一样的uuid字符串
    for i, entity in enumerate(graph_data["entities"]):
        community_membership_id = community_membership[i]
        if community_membership_id not in community_id_map:
            community_id_map[community_membership_id] = str(uuid.uuid4())

        entity["community_id"] = community_id_map[community_membership_id]

    # 使用 PyVis 可视化社区分布

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

        net.nodes[i]["label"] = (
            f"{net.nodes[i]['text']} ({net.nodes[i]['type']})"  # 设置节点标签
        )
        net.nodes[i]["title"] = f"Community {community}"
        net.nodes[i]["color"] = color

    for edge in net.edges:
        color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        if len(edge["type"]) > 1:
            edge["label"] = str(edge["type"])  # 设置边的提示信息
            edge["label"] = str(edge["type"])  # 设置边的提示信息
        else:
            edge["label"] = edge["type"]
        edge["color"] = color

    prefix = str(uuid.uuid4())
    # 这块net.show先暂时保留了，方便做测试
    net.show(f"{prefix}_graph_with_leiden.html")
    html_content = net.generate_html()

    return GraphDataAddCommunityWithVisualization(
        graph_data=graph_data, html_content=html_content
    )
    # 这里函数的返回建议是个html的字符串
    # 然后也返回了添加community_id的graph_data


# test_data = {"entities": [{"id": "1a320717-8765-451e-9c1c-6648519d5632", "text": "Microsoft", "type": "company"}, {"id": "ea3432d9-972a-43da-9fab-89a2bb6b950f", "text": "Satya Nadella", "type": ["person", "manager"]}, {"id": "0d98dd23-042e-4a28-8cbc-a8050b9d9366", "text": "Azure AI", "type": "product"}], "relations": [{"head": "ea3432d9-972a-43da-9fab-89a2bb6b950f", "tail": "1a320717-8765-451e-9c1c-6648519d5632", "type": "CEO of", "id": "af28a2d6-a543-4254-914d-7bc7bdb4947f"}, {"head": "1a320717-8765-451e-9c1c-6648519d5632", "tail": "0d98dd23-042e-4a28-8cbc-a8050b9d9366", "type": ["developed", "product"], "id": "6c5720bd-03c1-4dba-be87-5bcd03856408"}]}
# asyncio.run(realize_leiden_community_algorithm(test_data))


# test_data = {
#     "entities": [
#         {
#             "id": "6bf47d6a-b2ad-4d44-bacf-abb99e9095b0",
#             "text": "深度求索（DeepSeek）",
#             "type": "组织",
#         },
#         {
#             "id": "e64e6976-0b09-4e9a-aed8-c69b9aacca00",
#             "text": "全球 AI 领域",
#             "type": "领域",
#         },
#         {
#             "id": "e0664b7b-f07f-4a8d-a6bc-ff8c8f651854",
#             "text": "2023 年",
#             "type": "时间",
#         },
#         {
#             "id": "fea44ea1-9fb3-45be-aff5-2c5c9d969927",
#             "text": "美股市场",
#             "type": "地点",
#         },
#         {
#             "id": "83fb1ffc-e5d1-4a5d-ba2a-972a3a85e897",
#             "text": "1 月 27 日",
#             "type": "时间",
#         },
#         {
#             "id": "247279f0-fafe-46b7-9531-9c12a18263c5",
#             "text": "美股 AI、芯片股",
#             "type": "股票",
#         },
#         {
#             "id": "352860c5-0f59-4212-9243-05d64a2ad8a5",
#             "text": "英伟达",
#             "type": "组织",
#         },
#         {
#             "id": "800da448-15d9-42e0-adf1-c7fcd9c5d514",
#             "text": "美国股市",
#             "type": "地点",
#         },
#     ],
#     "relations": [
#         {
#             "head": "6bf47d6a-b2ad-4d44-bacf-abb99e9095b0",
#             "tail": "e64e6976-0b09-4e9a-aed8-c69b9aacca00",
#             "type": "在领域中崭露头角",
#             "description": "深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。",
#             "id": "5d89e03b-d883-4182-ba24-9c54ba5dd04b",
#         },
#         {
#             "head": "6bf47d6a-b2ad-4d44-bacf-abb99e9095b0",
#             "tail": "e0664b7b-f07f-4a8d-a6bc-ff8c8f651854",
#             "type": "成立于",
#             "description": "深度求索（DeepSeek）成立于2023年。",
#             "id": "b1c5cc8a-2bcf-42f2-9fc9-5f4ea2c6902e",
#         },
#         {
#             "head": "6bf47d6a-b2ad-4d44-bacf-abb99e9095b0",
#             "tail": "fea44ea1-9fb3-45be-aff5-2c5c9d969927",
#             "type": "影响力体现在",
#             "description": "深度求索（DeepSeek）的影响力在美股市场有明显体现。",
#             "id": "1ac6d028-5783-4b36-a434-567d514ffea4",
#         },
#         {
#             "head": "83fb1ffc-e5d1-4a5d-ba2a-972a3a85e897",
#             "tail": "247279f0-fafe-46b7-9531-9c12a18263c5",
#             "type": "导致重挫",
#             "description": "1月27日，美股AI、芯片股重挫。",
#             "id": "5c30c479-0bce-4767-9937-d5473ead17aa",
#         },
#         {
#             "head": "247279f0-fafe-46b7-9531-9c12a18263c5",
#             "tail": "352860c5-0f59-4212-9243-05d64a2ad8a5",
#             "type": "影响公司股价",
#             "description": "英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。",
#             "id": "994c2c7a-bba9-4002-b17a-6c496ccb25ec",
#         },
#         {
#             "head": "352860c5-0f59-4212-9243-05d64a2ad8a5",
#             "tail": "800da448-15d9-42e0-adf1-c7fcd9c5d514",
#             "type": "创历史纪录",
#             "description": "创下美国股市历史上最高纪录。",
#             "id": "f98c24b6-95e2-4dcb-bb0b-10b6d4c643b0",
#         },
#         {
#             "head": "6bf47d6a-b2ad-4d44-bacf-abb99e9095b0",
#             "tail": "247279f0-fafe-46b7-9531-9c12a18263c5",
#             "type": "被认为是重要因素",
#             "description": "深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
#             "id": "602cbe62-77a1-4672-8b15-c576f8b88dca",
#         },
#     ],
# }
# print(asyncio.run(realize_leiden_community_algorithm(test_data)))
