from typing import TypedDict


class User(TypedDict):
    name: str
    age: int
    email: str


# 用户传入字典
user_dict = {"name": "Alice", "age": 30, "email": "alice@example.com"}
user = User(**user_dict)
print(user.age)
