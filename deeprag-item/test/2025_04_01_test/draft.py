from pydantic import RootModel


class User(RootModel):
    root: str
