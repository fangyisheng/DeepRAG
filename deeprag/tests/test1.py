import requests

url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
text = '''深度求索 DeepSeek：AI 领域的新兴力量过去几周,深度求索（DeepSeek）在全球 AI 领域掀起了一场风暴,成为众人瞩目的焦点。这家成立于 2023 年的年轻大模型公司,宛如一匹黑马,迅速在行业中崭露头角,其影响力甚至在美股市场都有明显体现。1 月 27 日,美股 AI、芯片股重挫,英伟达收盘大跌超过 17%,单日市值蒸发 5890 亿美元 ,创下美国股市历史上最高纪录,这一波动背后,DeepSeek 被认为是重要因素之一。在自媒体和公众的视野里,DeepSeek 有着诸多令人瞩目的 "爽点",被视为 "2025 年最燃爽文主角"。其一,"神秘力量弯道超车"。作为一家出身私募量化投资公司幻方量化的 AI 企业,此前讨论度并不高,却一举成为中国领先的 AI 公司,让许多人惊叹 "乱拳打死老师傅"。其二,"小力出奇迹"。DeepSeek-V3 模型训练成本约为 558 万美元,不到 OpenAI GPT-4o 模型的十分之一,性能却已接近,这似乎颠覆了 AI 行业长期信奉的 "大力出奇迹" 的规模定律。其三,"英伟达护城河消失"。'''
data = {
    "model": "qwen-turbo",
    "messages": [
        {"role": "system", "content": "请帮我总结一下"},
        {"role": "user", "content": text},
    ],
    "stream": False,
}


headers = {"Authorization": "Bearer sk-ad848abd86f04a19a958071301071b1b"}

print("好像卡在这里")
response = requests.post(url, json=data, headers=headers)

print(response.json())


