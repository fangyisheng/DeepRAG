from prisma import Prisma
import uuid


async def main():
    db = Prisma()
    await db.connect()

    users = await db.knowledge_space.create(
        data={
            "id": str(uuid.uuid4()),
            "knowledge_space_id": str(uuid.uuid4()),
            "knowledge_space_title": "测试知识库4",
        }
    )

    await db.disconnect()

    print(users)
    print(type(users))
    print(users.__dict__)


# 运行异步函数
import asyncio

asyncio.run(main())
