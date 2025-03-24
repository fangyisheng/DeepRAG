# from pydantic import BaseModel
# from typing import Any


# class Test(BaseModel):
#     id: Any
#     number: Any


# a = [{"id": "1", "number": "1"}]


# def nihao(x: list[Test]):
#     print("nihao")


# nihao(a)
data_list = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]

key = 2
for dict in data_list:
    if key value in dict