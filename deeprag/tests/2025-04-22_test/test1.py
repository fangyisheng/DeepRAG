from deeprag.rag_core_utils.llm_api.llm_api_client import (
    llm_service,
    llm_service_stream,
)


system_prompt = """帮我总结全文"""


with open(
    "/root/project/DeepRAG/deeprag/src/deeprag/knowledge_file/deepseek.txt", "r"
) as f:
    user_prompt = f.read()
import re

# 在这里定义要输出的文本
text = """深度求索 DeepSeek：AI 领域的新兴力量# 过去几周，深度求索（DeepSeek）在全球 AI 领域掀起了一场风暴，成为众人瞩目的焦点。这家成立于 2023 年的年轻大模型公司，宛如一匹黑马，迅速在行业中崭露头角，其影响力甚至在美股市场都有明显体现。1 月 27 日，美股 AI、芯片股重挫，英伟达收盘大跌超过 17%，单日市值蒸发 5890 亿美元 ，创下美国股市历史上最高纪录，这一波动背后，DeepSeek 被认为是重要因素之一。# 在自媒体和公众的视野里，DeepSeek 有着诸多令人瞩 目的 "爽点"，被视为 "2025 年最燃爽文主角"。其一，"神秘力量弯道超车"。作为一家出身私募量化投资公司幻方量化的 AI 企业，此前讨论度并不高，却一举成为中国领先的 AI 公司，让许多人惊叹 "乱拳打死老师傅"。其二，"小力出奇迹"。DeepSeek-V3 模型训练成本约为 558 万美元，不到 OpenAI GPT-4o 模型的十分之一，性能却已接近，这似乎颠覆了 AI 行业长期信奉的 "大力出奇迹" 的规模定律。其三，"英伟达护城 河消失"。DeepSeek 在论文中提到采用定制的 PTX 语言编程，被解读为 "绕开英伟达 CUDA 运算平台<>"""


def filter_special_chars(text):
    # 保留中文、英文、数字和空格，去除其他特殊字符
    filtered_text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff\s]", "", text)
    # 将多个空格替换为单个空格
    filtered_text = re.sub(r"\s+", " ", filtered_text)
    return filtered_text.strip()


def print_text():
    print("原始文本：")
    print("-" * 50)
    print(text)
    print("\n过滤特殊字符后的文本：")
    print("-" * 50)
    print(filter_special_chars(text))


if __name__ == "__main__":
    print_text()


async def main(user_prompt: str):
    async for answer in llm_service_stream(
        system_prompt=system_prompt, user_prompt=user_prompt
    ):
        print(answer)


import asyncio

asyncio.run(main(filter_special_chars(text)))
