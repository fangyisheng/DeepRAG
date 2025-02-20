import networkx as nx
import igraph as ig
import leidenalg
import matplotlib.pyplot as plt

# Step 1: 创建NetworkX图
G = nx.Graph()
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 4)]
G.add_edges_from(edges)
print(G.nodes)
# Step 2: 转换为igraph图
g = ig.Graph.from_networkx(G)

# Step 3: 使用Leiden算法进行社区检测
partition = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition)
community_membership = partition.membership

# Step 4: 将社区信息存储为节点属性
for node, community in enumerate(community_membership):
    G.nodes[node]['community'] = community

# Step 5: 可视化
colors = [G.nodes[node]['community'] for node in G.nodes]
pos = nx.spring_layout(G)
nx.draw(
    G,
    pos,
    node_color=colors,
    with_labels=True,
    cmap=plt.cm.Set1,
    node_size=300
)
plt.title("Community Detection using Leiden Algorithm")
plt.show()