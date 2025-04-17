from deeprag.deeprag import DeepRAG
import asyncio

deeprag = DeepRAG()


async def main():
    created_user = await deeprag.create_user("test_user")
