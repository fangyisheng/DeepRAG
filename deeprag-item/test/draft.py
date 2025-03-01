# import tiktoken

# # 选择编码器，例如 gpt-3.5-turbo 或 gpt-4
# encoding = tiktoken.encoding_for_model("gpt-4o")
# text = "这是一个测试文本。"
# tokens = encoding.encode(text)
# print(tokens)
# token_count = len(tokens)
# print(type(token_count))
# print(f"文本中的 token 数量: {token_count}")

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
chinese_array = generate_chinese_array(size=20, string_length=8000)

# 打印结果
print(chinese_array)