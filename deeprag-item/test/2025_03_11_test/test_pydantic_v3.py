from pydantic import BaseModel
from typing import Any


class Test(BaseModel):
    id: Any
    number: Any


a = [{"id": "1", "number": "1"}]


def nihao(x: list[Test]):
    print("nihao")


nihao(a)
