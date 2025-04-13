import re
from deeprag.workflow.data_model import CompleteTextUnit
from deeprag.rag_core_utils.s3_api.s3_api_client import create_minio_client


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
    content = content.replace("\n", "")
    cleaned_content = re.sub(
        r"(?<=[\u4e00-\u9fff\d])\s+|\s+(?=[\u4e00-\u9fff\d])", "", content
    )
    return CompleteTextUnit(root=cleaned_content)


# 测试成功
import asyncio

print(asyncio.run(process_text("mybucket", "test2.txt")))
