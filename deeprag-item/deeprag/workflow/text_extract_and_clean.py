import re
from data_model import

async def process_text(file_path: str) -> str:
    """_summary_

    Args:
        file_path (str): 文件路径

    Returns:
        str: 清洗好的文本字符串
    """
    # 将文本按行分割
    with open(file_path, "r") as file:
        content = file.read()
    # lines = content.splitlines()
    # # 过滤掉空行，并将非空行合并为一个连续的字符串
    # continuous_text = "".join(line.strip().replace(" ", "") for line in lines if line.strip())
    # return continuous_text
    content = content.replace("\n", "")
    cleaned_content = re.sub(
        r"(?<=[\u4e00-\u9fff\d])\s+|\s+(?=[\u4e00-\u9fff\d])", "", content
    )
    return cleaned_content


# import asyncio
# print(asyncio.run(process_text("/home/easonfang/DeepRAG/deeprag-item/deeprag/knowledge_file/test.txt")))
