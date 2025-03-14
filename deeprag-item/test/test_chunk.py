import asyncio
from deeprag.workflow.text_extract_and_clean import process_text
from deeprag.workflow.text_chunk_based_by_token import split_text_by_token


async def main():
    text = await process_text("../knowledge_file/test.txt")
    chunk = await split_text_by_token(text=text)
    return chunk


print(asyncio.run(main()))
# import os
# print(os.getcwd())
