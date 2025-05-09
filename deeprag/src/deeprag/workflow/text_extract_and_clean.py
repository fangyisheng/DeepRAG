import re
from deeprag.workflow.data_model import CompleteTextUnit
from deeprag.rag_core_utils.s3_api.s3_api_client import create_minio_client
from pathlib import Path


async def process_text(bucket_name: str, object_name: str) -> CompleteTextUnit:
    """_summary_

    Args:
        bucket_name (str): minio桶的名字
        object_name (str): minio的文件对象名字

    Returns:
        str: 清洗好的文本字符串
    """
    # 将文本按行分割
    # with open(file_path, "r") as file:
    #     content = file.read()
    client = await create_minio_client()
    file = client.get_object(bucket_name, object_name)
    # lines = content.splitlines()
    # # 过滤掉空行，并将非空行合并为一个连续的字符串
    # continuous_text = "".join(line.strip().replace(" ", "") for line in lines if line.strip())
    # return continuous_text
    content = file.read().decode("utf-8")
    # print(type(content))
    if Path(object_name).suffix != ".csv":
        content = content.replace("\n", "")
        cleaned_content = re.sub(
            r"(?<=[\u4e00-\u9fff\d])\s+|\s+(?=[\u4e00-\u9fff\d])", "", content
        )
        return CompleteTextUnit(root=cleaned_content)
    else:
        return CompleteTextUnit(root=content)


# # 单元化功能测试成功
# import asyncio
# import csv
# import io
# import traceback
# from loguru import logger


# async def get_csv_content(bucket_name, object_name):
#     client = await create_minio_client()

#     response = client.get_object(bucket_name, object_name)

#     text_stream = io.StringIO(response.read().decode("utf-8"))
#     # text_stream = io.TextIOWrapper(response, encoding="utf-8")
#     reader = csv.reader(text_stream)
#     header = next(reader)
#     print("Header:", header)
#     for row in reader:
#         logger.info(f"Row: {row}")


# asyncio.run(get_csv_content("mybucket", "test.csv"))

# # 将响应内容（bytes）转为字符串流 StringIO
# # data = response.read().decode("utf-8")  # 假设是 utf-8 编码
# # text_stream = io.StringIO(data)
# text_stream = io.TextIOWrapper(response, encoding="utf-8")

# # 使用 csv.DictReader 解析文本流
# reader = csv.DictReader(text_stream)
# for row in reader:
#     print(row)  # 每一行是一个字典
