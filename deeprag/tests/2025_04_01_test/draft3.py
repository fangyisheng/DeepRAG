# a = """data: {"choices":[{"delta":{"content":"","role":"assistant"},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1744945444,"system_fingerprint":null,"model":"qwen-plus-latest","id":"chatcmpl-4246cb78-9e0e-943c-8b6a-4d8e0a40297d"}"""
# import json

# real_dict_data = a.split(":", 1)[1].strip()
# print(json.loads(real_dict_data)[""])
from datetime import datetime

from datetime import datetime

# 获取当前时间
now = datetime.now()

# 将时间格式化为字符串
time_str = now.strftime("%Y-%m-%d %H:%M:%S")  # 自定义格式

print("当前时间 (str 格式):", time_str)
