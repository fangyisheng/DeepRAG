import tiktoken
import os
from dotenv import load_dotenv
from loguru import logger
from deeprag.workflow.data_model import ChunkedTextUnit

load_dotenv()


class TextSplitter:
    def __init__(self):
        self.chunks = []
        self.tokens_by_chunk = []  # 和上面的chunk一一对应，存的是该chunk消耗的token数量

    # 在读取环境文件中的数字时，其实读到的是str
    async def split_text_by_token(
        self,
        text: str,
        max_tokens: int = int(os.getenv("EMBEDDING_MODEL_MAX_TOKEN")),
        model_name: str = "gpt-4o",
    ) -> ChunkedTextUnit:
        """
        利用 tiktoken 根据 token 数量来切分文本。

        Args:
            text: 要切分的文本 (str).
            max_tokens: 每个文本片段的最大 token 数量 (int).
            model_name: 使用的 OpenAI 模型名称 (str).  用于确定 tokenizer. 默认为 "gpt-4o".

        Returns:
            切分后的文本片段列表 (list[str]).
        """

        encoding = tiktoken.encoding_for_model(model_name)

        # 将文本编码为token
        tokens = encoding.encode(text)
        logger.info(f"文本的token数量为:{len(tokens)}")

        # 分块

        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i : i + max_tokens]
            chunk_text = encoding.decode(chunk_tokens)
            self.chunks.append(chunk_text)
            self.tokens_by_chunk.append(len(chunk_tokens))

        return ChunkedTextUnit(root=self.chunks)


# async def main():
#     text = """《北京市住宅设计规范》（编号：DB11/1740—2020）是一份针对**北京市**及**城镇**地区**住宅**建筑设计的重要文件。该规范详细**规定了设计要求**，旨在提升住宅的功能性、安全性和舒适性，同时推动建筑行业的可持续发展。

# 根据规范内容，其适用范围明确覆盖**北京市**和**城镇**区域，并特别强调了对**住宅**建筑的设计标准。此外，规范提倡在住宅设计中采用**全装修**的理念，以减少后期施工带来的资源浪费和环境污染。同时，为了适应现代生活的需求，规范指出住宅设计中**可包含**多种现代化设备，例如**智能家居系统**、**智能电表**、**电动汽车充电桩**、**信息管道**、**楼道综合配线箱**、**有线广播电视放大箱**、**终端综合配线箱**、**出线盒**以及**有线广播电视终端盒**等，从而提升居住体验和便利性。

# 在安全性方面，该规范还**涉及**了**安全等级**和**耐久性**的相关要求，确保住宅建筑在长期使用过程中能够保持结构稳定和功能可靠。同时，规范积极响应国家政策，提倡遵循**绿色、节能、生态、环保**的理念，推动建筑行业向低碳环保方向发展。

# 此外，《北京市住宅设计规范》明确要求住宅设计需**符合**现行的**消防技术标准**，以保障居民的生命财产安全。通过这一系列严格的标准和指导原则，该规范为北京市住宅建筑的设计和建设提供了全面的技术支持，助力打造更加宜居的城市生活环境。"""
#     max_tokens = 50  # 每块最多包含10个token
#     splitter = TextSplitter()
#     chunk = await splitter.split_text_by_token(text=text, max_tokens=max_tokens)
#     return chunk

# if __name__ == "__main__":
#     import asyncio
#     print(asyncio.run(main()))
