# from pydantic import BaseModel, Field


# class User(BaseModel):
#     """
#     用户信息模型。
#     """

#     id: int = Field(..., description="用户的唯一标识符")
#     name: str = Field(..., description="用户的名称")
#     email: str = Field(..., description="用户的邮箱地址")


# def get_user() -> User:
#     """
#     获取用户信息。

#     返回值：
#         User: 用户信息模型。
#     """
#     return User(id=1, name="Alice", email="alice@example.com")

# a = 2

# if a == 2:
#     b = 2

# print(b)
from beeprint import pp


class Entity:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

    def __repr__(self):
        return f"Entity(id={self.id}, name={self.name}, type={self.type})"


# 创建实例
entity = Entity(id="12345", name="深度求索", type="组织")

# 使用 beeprint 打印
pp(entity.__dict__)
