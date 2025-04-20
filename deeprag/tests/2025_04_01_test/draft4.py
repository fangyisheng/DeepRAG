from deeprag import samples
import asyncio

deeprag = DeepRAG()


async def main(file_path: str):
    created_user = await deeprag.create_user("test_user")


asyncio.run(main("111"))
