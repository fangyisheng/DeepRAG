# meta_data_list = None
# if isinstance(meta_data_list, None):
#     print("meta_data_list is none")
# else:
#     print("meta_data_list is not str")

# from pydantic import BaseModel


# class my_data(BaseModel):
#     text: str
#     meta_data: str


# class my_data_2(BaseModel):
#     text: str
#     another_information: dict[str, my_data]


# a = my_data_2(
#     text="hello", another_information={"a": my_data(text="hello", meta_data="world")}
# )

# print(a.another_information["a"].text)


# 这样做是绝对不可以的
# import asyncio
# from pydantic import BaseModel


# class my_data(BaseModel):
#     text: str
#     meta_data: str


# async def test():
#     return my_data(text="hello", meta_data="world")


# async def main():
#     a = await test().text
#     return a


# print(asyncio.run(main()))


# a = {"a": 1, "b": 2, "c": 3}
# print(len(a))

# from loguru import logger

# a = "file_id"
# logger.info(f"""knowlege_scope["{a}"] == "uuid" """)


# print(len(b"hello world"))
