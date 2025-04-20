# from pydantic import BaseModel
# from typing import Any


# class Parameter(BaseModel):
#     id: Any


# def func(data: Parameter):
#     return "你好"


# # 实践者出真知啊，确实可以用dict结合pydantic来做数据验证
# print(func({"number": "1", "id": "2"}))


# 测试成功
# def nihao(id: str):
#     id_class = Parameter(id=id)
#     return id_class.model_dump()


# print(nihao("shide"))

from pydantic import BaseModel, Field
from typing import Any


class Parameter(BaseModel):
    id: str = Field(description="这个是用户id")
    number: str


def nihao(nihao) -> Parameter:
    return Parameter(id=str(nihao), number="1")


print(nihao(2))
# from typing import TypedDict, Optional


# class User(TypedDict):
#     id: int
#     name: str
#     email: Optional[str]  # 可选字段


# def process_user(user: User):
#     print(f"Processing user: {user['name']}")


# user_data: User = {"id": 1, "name": "Alice", "email": "alice@example.com"}
# process_user(user_data)

# 类型检查器 (MyPy/Pyright) 会检测到以下错误:
# invalid_user_data: User = {"id": "one", "name": "Bob"}  # id is a string instead of int
# 但在运行时不会报错
