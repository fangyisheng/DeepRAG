import tiktoken
import os 
from dotenv import load_dotenv
from loguru import logger
load_dotenv()
from loguru import logger

class TextSplitter:
    def __init__(self):
        self.chunks = []
        self.tokens_by_chunk = [] # 和上面的token一一对应

    #在读取环境文件中的数字时，其实读到的是str
    async def split_text_by_token(self, text: str, max_tokens: int = int(os.getenv("EMBEDDING_MODEL_MAX_TOKEN")), model_name: str = "gpt-4o") -> list[str]:
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
            chunk_tokens = tokens[i:i + max_tokens]
            chunk_text = encoding.decode(chunk_tokens)
            self.chunks.append(chunk_text)
            self.tokens_by_chunk.append(len(chunk_tokens))
        
        return self.chunks


# # test code
# async def main():
#     text = "这是一个示例文本，用于演示如何根据token进行分块。我们将这段文本分成多个小块，每块包含一定数量的token。"
#     max_tokens = 10  # 每块最多包含10个token
#     chunk = await split_text_by_token(text=text, max_tokens=max_tokens)
#     return chunk

# if __name__ == "__main__":
#     import asyncio
#     print(asyncio.run(main()))


