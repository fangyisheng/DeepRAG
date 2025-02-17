from deeprag.rag_core_utils.embedding_api.embedding_api_client import text_to_vector
import asyncio
from deeprag.text_extract_and_clean import process_text
from deeprag.text_chunk_based_by_token import split_text_by_token
from deeprag.batch_text_chunk_generate_embeddings import batch_text_chunk_generate_embeddings_process

import random

def generate_chinese_string(length=5):
    """
    生成一个指定长度的随机中文字符串。
    :param length: 字符串的长度
    :return: 随机生成的中文字符串
    """
    # 中文字符的 Unicode 范围：\u4e00-\u9fff
    chinese_characters = [chr(random.randint(0x4e00, 0x9fff)) for _ in range(length)]
    return ''.join(chinese_characters)

def generate_chinese_array(size=20, string_length=5):
    """
    生成一个包含指定数量中文字符串的数组。
    :param size: 数组的大小（元素数量）
    :param string_length: 每个中文字符串的长度
    :return: 包含中文字符串的数组
    """
    return [generate_chinese_string(string_length) for _ in range(size)]

# 生成包含 20 个中文字符串的数组
chinese_array = generate_chinese_array(size=22, string_length=800)

async def text_chunk():
      text = await process_text("../deeprag/knowledge_file/test.txt") #这边其实以后可以做好batch_file的优化
      chunk = await split_text_by_token(text=text)
      return chunk

# 在主程序中调用异步函数
async def main():
    vector_array = await batch_text_chunk_generate_embeddings_process(chinese_array)
    print(vector_array)
    print(len(vector_array))


asyncio.run(main())




