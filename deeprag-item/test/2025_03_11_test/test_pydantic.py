from pydantic import BaseModel
from typing import Any


class Parameter(BaseModel):
    number: Any
    id: Any


def func(data: Parameter):
    return "你好"


# 实践者出真知啊，确实可以用dict结合pydantic来做数据验证
print(func({"number": "1", "id": "2"}))
