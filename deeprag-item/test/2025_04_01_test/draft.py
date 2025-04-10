# from pydantic import RootModel


# class User(RootModel):
#     root: str


# a = "你好啊，大家好"
# print(a[:5])

# from transformers import AutoModelForCausalLM, AutoTokenizer

# # 加载模型
# model_name = "Qwen/Qwen2.5-0.5B"


# # 加载分词器
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# # 编码输入文本
# input_text = "这是一个测试文本"
# inputs = tokenizer(input_text, return_tensors="pt")

# # 生成文本
# print(inputs)
import tempfile
import os

# 获取临时目录路径
temp_dir = tempfile.gettempdir()
print("临时目录路径:", temp_dir)

# 列出临时目录中的文件（需要权限）
try:
    print("临时目录内容:", os.listdir(temp_dir))
except PermissionError:
    print("无权限访问临时目录内容")
