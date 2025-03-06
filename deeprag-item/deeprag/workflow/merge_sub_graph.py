import uuid
import json


async def merge_sub_entity_relationship_graph(entity_relationship_graphs: list):
        merged_graph = {
            "entities":[],
            "relations":[]
        }    


        #下面两段for循环的作用是将提取的图结构中的语义不明确的关系的实体的id填充完整，head和tail
        for graph in entity_relationship_graphs:
            for relation in graph["relations"]:
                relation["head"] = next((item["text"] for item in graph["entities"] if item["id"] == relation["head"]),None)
                relation["tail"] = next((item["text"] for item in graph["entities"] if item["id"] == relation["tail"]),None)
            
        for dict in entity_relationship_graphs:
            for entity in dict["entities"]:
                
                existing_text = next((item for item in merged_graph["entities"] if item.get("text") == entity["text"]),None)
                if existing_text:
                    existing_text["id"] =  str(uuid.uuid4())
                    if existing_text["type"] != entity["type"]:
                       existing_text["type"] = [existing_text["type"], entity["type"]]
                
                else:
                    entity["id"] = str(uuid.uuid4())
                    merged_graph["entities"].append(entity)
            for relation in dict["relations"]:
                existing_relation = next(( item for item in merged_graph["relations"] if item.get("head") == relation["head"] and item.get("tail") == relation["tail"]),None)
                if existing_relation:
                    if existing_relation["type"] != relation["type"]:
                        existing_relation["type"] = [existing_relation["type"], entity["type"]]
                else:
                    relation["id"] = str(uuid.uuid4())
                    merged_graph["relations"].append(relation)
            for relation in merged_graph["relations"]:
                relation["head"] = next((entity["id"] for entity in merged_graph["entities"] if entity["text"] == relation["head"]),None)
                relation["tail"] = next((entity["id"] for entity in merged_graph["entities"] if entity["text"] == relation["tail"]),None)
                    
        return merged_graph


# import asyncio
# test_data = [{"entities":[{"id":0,"text":"深度求索","type":"公司"},{"id":1,"text":"DeepSeek","type":"公司"},{"id":2,"text":"AI领域","type":"领域"},{"id":3,"text":"美股市场","type":"市场"},{"id":4,"text":"英伟达","type":"公司"},{"id":5,"text":"OpenAI","type":"公司"},{"id":6,"text":"GPT-4o","type":"产品"},{"id":7,"text":"幻方量化","type":"公司"},{"id":8,"text":"萤火二号","type":"产品"},{"id":9,"text":"华为云","type":"产品"},{"id":10,"text":"腾讯云","type":"产品"},{"id":11,"text":"百度云","type":"产品"},{"id":12,"text":"MLA架构","type":"技术"},{"id":13,"text":"MHA架构","type":"技术"},{"id":14,"text":"DeepSeek MoEs Parse结构","type":"技术"},{"id":15,"text":"硅谷","type":"地点"},{"id":16,"text":"DeepSeek-R1模型","type":"产品"},{"id":17,"text":"OpenAI o1模型","type":"产品"},{"id":18,"text":"纳米AI搜索","type":"产品"},{"id":19,"text":"周鸿祎","type":"人物"},{"id":20,"text":"小鹏汽车","type":"公司"},{"id":21,"text":"何小鹏","type":"人物"},{"id":22,"text":"阿里巴巴","type":"公司"},{"id":23,"text":"京东","type":"公司"},{"id":24,"text":"清华大学","type":"机构"},{"id":25,"text":"A大学","type":"机构"},{"id":26,"text":"微软","type":"公司"},{"id":27,"text":"亚马逊","type":"公司"}],"relations":[{"head":0,"tail":1,"type":"别名"},{"head":0,"tail":2,"type":"属于"},{"head":3,"tail":0,"type":"受影响"},{"head":4,"tail":3,"type":"影响"},{"head":5,"tail":6,"type":"开发"},{"head":7,"tail":0,"type":"投资"},{"head":8,"tail":7,"type":"属于"},{"head":9,"tail":0,"type":"合作"},{"head":10,"tail":0,"type":"合作"},{"head":11,"tail":0,"type":"合作"},{"head":12,"tail":0,"type":"使用"},{"head":13,"tail":12,"type":"对比"},{"head":14,"tail":0,"type":"开发"},{"head":15,"tail":0,"type":"评价"},{"head":16,"tail":0,"type":"开发"},{"head":17,"tail":16,"type":"对比"},{"head":18,"tail":0,"type":"合作"},{"head":19,"tail":18,"type":"提及"},{"head":20,"tail":0,"type":"计划合作"},{"head":21,"tail":20,"type":"担任"},{"head":22,"tail":0,"type":"合作"},{"head":23,"tail":0,"type":"合作"},{"head":16,"tail":24,"type":"互动"},{"head":16,"tail":25,"type":"互动"},{"head":26,"tail":27,"type":"合作"}]}]
# print(asyncio.run(merge_sub_entity_relationship_graph(test_data)))
