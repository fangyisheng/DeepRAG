import random

community_colors = {}
community_membership = [0,1,1]
unique_communities = set(community_membership)

for comm in unique_communities:
    # 为每个社区生成唯一的颜色
    community_colors[comm] = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

print(community_colors)