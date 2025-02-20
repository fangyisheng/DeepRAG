import uuid

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
                print(relation)
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


