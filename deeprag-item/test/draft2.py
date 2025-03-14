import networkx as nx
import matplotlib.pyplot as plt

# 定义知识图谱数据
data = {
    "entities": [
        {"id": 0, "text": "Microsoft", "type": "company"},
        {"id": 1, "text": "Satya Nadella", "type": "person"},
        {"id": 2, "text": "Azure AI", "type": "product"},
    ],
    "relations": [
        {"head": "Satya Nadella", "tail": "Microsoft", "type": "CEO of"},
        {"head": "Microsoft", "tail": "Azure AI", "type": "developed"},
    ],
}

# 创建一个有向图
G = nx.DiGraph()

# 添加节点（实体）
for entity in data["entities"]:
    G.add_node(entity["text"], type=entity["type"])

# 添加边（关系）
for relation in data["relations"]:
    G.add_edge(relation["head"], relation["tail"], relation=relation["type"])

# 查看图的信息
print("Nodes:", G.nodes(data=True))
print("Edges:", G.edges(data=True))

# 绘制图
pos = nx.spring_layout(G)  # 定义布局
plt.figure(figsize=(8, 6))

# 绘制节点
node_colors = {"company": "lightblue", "person": "lightgreen", "product": "salmon"}
node_color = [node_colors[G.nodes[node]["type"]] for node in G.nodes()]
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_color,
    node_size=3000,
    font_size=10,
    font_weight="bold",
)

# 绘制边的标签
edge_labels = nx.get_edge_attributes(G, "relation")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Knowledge Graph")
plt.show()

# 保存图到文件（可选）
nx.write_gexf(G, "knowledge_graph.gexf")
