async def my_generator():
    yield "hello"
    yield "world"


async def main():
    async for item in my_generator():
        print(item)


import asyncio

asyncio.run(main())
