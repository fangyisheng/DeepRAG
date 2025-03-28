from pydantic import BaseModel, Field


class User(BaseModel):
    """
    用户信息模型。
    """

    id: int = Field(..., description="用户的唯一标识符")
    name: str = Field(..., description="用户的名称")
    email: str = Field(..., description="用户的邮箱地址")


def get_user() -> User:
    """
    获取用户信息。

    返回值：
        User: 用户信息模型。
    """
    return User(id=1, name="Alice", email="alice@example.com")
