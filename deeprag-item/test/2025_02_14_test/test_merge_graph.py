test_data_1 = { "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": 0, "tail": 2, "type": "developed" } ] }
print(test_data_1)

test_data_2 ={'entities': [{'id': 0, 'text': 'Microsoft', 'type': 'company'}, {'id': 1, 'text': 'Satya Nadella', 'type': 'person'}, {'id': 2, 'text': 'Azure AI', 'type': 'product'}], 'relations': [{'head': 1, 'tail': 0, 'type': 'CEO of'}, {'head': 0, 'tail': 2, 'type': 'protect'}]} 


merged_graph = {
    "entities":[],
    "relations":[]
}

for entity in test_data_1["entities"]+test_data_2["entities"]:
    
