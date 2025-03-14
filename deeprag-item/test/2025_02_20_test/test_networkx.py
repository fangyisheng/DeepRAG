import networkx as nx

# 创建一个图
G = nx.Graph()

# 添加边
G.add_edge(1, 2, weight=4)
G.add_edge(2, 3, weight=5)

# 打印 G.edges
print(G.edges)  # 输出 EdgeView 对象
# print(list(G.edges))  # 转换为列表输出

# # 访问边属性
# print(G.edges[(1, 2)])  # 输出边 (1, 2) 的属性
