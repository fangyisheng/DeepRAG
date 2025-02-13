import networkx as nx
from pyvis.network import Network
import random
import asyncio
import uuid


async def store_graph_data_to_html(entity_relationship):
    import networkx as nx

    # 创建有向的多关系图
    G = nx.MultiDiGraph()


    # 存储实体和实体之间的关系
    for entity in entity_relationship["entities"]:
        G.add_node(entity["id"], text=entity["text"], type=entity["type"])
    
    for relationship in entity_relationship["relations"]:
        G.add_edge(relationship["head"], relationship["tail"], type=relationship["type"])

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



# test_data = {
#     "entities": [
#         {"id": 0, "text": "张三", "type": "人物"},
#         {"id": 1, "text": "上海", "type": "地点"},
#         {"id": 2, "text": "建筑工人", "type": "职业"},
#         {"id": 3, "text": "李四", "type": "人物"}
#     ],
#     "relations": [
#         {"head": 0, "tail": 1, "type": "工作地点"},
#         {"head": 0, "tail": 2, "type": "从事职业"},
#         {"head": 3, "tail": 0, "type": "别名"}
#     ]
# }
# asyncio.run(store_graph_data_to_html(test_data))



