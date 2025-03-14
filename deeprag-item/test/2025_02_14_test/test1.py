# test_data_1 = { "entities": [ { "id": 0, "text": "Microsoft", "type": "company" }, { "id": 1, "text": "Satya Nadella", "type": "person" }, { "id": 2, "text": "Azure AI", "type": "product", } ], "relations": [ { "head": 1, "tail": 0, "type": "CEO of" }, { "head": 0, "tail": 2, "type": "developed" } ] }
# # for i in range(0,5):
# #      a = next((b for b in range(0,5) if b == 2),None)
# for relation in test_data_1["relations"]:
#     #   relation["head"] = next((item["text"] for item in test_data_1["entities"] if item["id"] == relation["head"]),None)
#       relation["tail"] = next((item["text"] for item in test_data_1["entities"] if item["id"] == relation["head"]),None)

merged_graph = {"entities": [], "relations": []}
print(
    next(
        (item["text"] for item in merged_graph["entities"] if item["text"] == "nihao"),
        None,
    )
)
