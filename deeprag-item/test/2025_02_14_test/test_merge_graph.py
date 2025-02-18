test_data_1 = { "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": 0, "tail": 2, "type": "developed" } ] }

test_data_2 ={'entities': [{'id': 0, 'text': 'Microsoft', 'type': 'company'}, {'id': 1, 'text': 'Satya Nadella', 'type': 'manager'}, {'id': 2, 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 1, 'tail': 0, 'type': 'CEO of'}, {'head': 0, 'tail': 2, 'type': 'protect'}]} 

merged_graph = {
    "entities":[],
    "relations":[]
}

a = test_data_1["entities"]+test_data_2["entities"]
b = test_data_1["relations"]+test_data_2["relations"]

for relation in test_data_1["relations"]:
    relation["head"] = next((item["text"] for item in test_data_1["entities"] if item["id"] == relation["head"]),None)
    relation["tail"] = next((item["text"] for item in test_data_1["entities"] if item["id"] == relation["head"]),None)







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

# for relation in b:
    
# print(merged_graph)
        

    


    
