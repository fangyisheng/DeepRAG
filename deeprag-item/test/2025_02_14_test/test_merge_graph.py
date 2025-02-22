test_data_1 = { "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": 0, "tail": 2, "type": "developed" } ] }

test_data_2 ={'entities': [{'id': 0, 'text': 'Microsoft', 'type': 'company'}, {'id': 1, 'text': 'Satya Nadella', 'type': 'manager'}, {'id': 2, 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 1, 'tail': 0, 'type': 'CEO of'}, {'head': 0, 'tail': 2, 'type': 'protect'}]} 

merged_graph = {
    "entities":[],
    "relations":[]
}

test_data_list = [test_data_1,test_data_2]

import uuid

#下面两段for循环的作用是将提取的图结构中的语义不明确的关系的实体的id填充完整，head和tail
for test_data in test_data_list:
    for relation in test_data["relations"]:
        relation["head"] = next((item["text"] for item in test_data["entities"] if item["id"] == relation["head"]),None)
        relation["tail"] = next((item["text"] for item in test_data["entities"] if item["id"] == relation["tail"]),None)
      
for dict in test_data_list:
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

print(merged_graph)

print

#恭喜，测试通过！！！！


        
        









# a = test_data_1["entities"] + test_data_2["entities"]
# import uuid
# for entity in a:
#     text = entity["text"]
#     type = entity["type"]
#     existing_graph = next((e for e in merged_graph["entities"] if e["text"] == text), None)
#     if existing_graph:
#         existing_graph["id"] = str(uuid.uuid4())
#         if existing_graph["type"] != type:
#             existing_graph["type"]= [existing_graph["type"],type]
#     else:
#         new_data = {
#             "id": str(uuid.uuid4()),
#             "text": text,
#             "type": type
#         }
#         merged_graph["entities"].append(new_data)
# print(a)



        

    


    
