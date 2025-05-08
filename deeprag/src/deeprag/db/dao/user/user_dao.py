from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import user, file

load_dotenv()
Prisma(auto_register=False)


class UserDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_user(self, id: str, user_name: str) -> user:
        if not self.db.is_connected():
            await self.db.connect()
        stored_user = await self.db.user.create(data={"id": id, "user_name": user_name})
        await self.db.disconnect()
        return stored_user

    async def get_user_name_by_id(self, id: str) -> user:
        if not self.db.is_connected():
            await self.db.connect()
        found_user = await self.db.user.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_user

    async def delete_user_by_id(self, id: str) -> user:
        if not self.db.is_connected():
            await self.db.connect()
        deleted_user = await self.db.user.delete(where={"id": id})
        await self.db.disconnect()
        return deleted_user

    async def get_all_users(self) -> list[user]:
        """
        这个函数可能需要进行分页查询的返回，因为可能用户数非常多
        """
        if not self.db.is_connected():
            await self.db.connect()
        all_users = await self.db.user.find_many()
        await self.db.disconnect()
        return all_users

    async def search_users_by_name(self, user_name: str) -> list[user]:
        """
        这个函数根据输入的用户名对表进行模糊搜索，返回所有匹配的用户
        """
        if not self.db.is_connected():
            await self.db.connect()
        searced_users = await self.db.user.find_many(
            where={"user_name": {"contains": user_name}}
        )
        await self.db.disconnect()
        return searced_users

    async def get_users_by_user_name(self, user_name: str) -> list[user]:
        """
        这个函数根据输入的用户名对表进行精确搜索，返回所有匹配的用户
        """

        if not self.db.is_connected():
            await self.db.connect()
        searced_users = await self.db.user.find_many(
            where={"user_name": user_name}, select={"id": True}
        )
        await self.db.disconnect()
        return searced_users

    async def update_user_by_id(self, id: str, user_name: str) -> user:
        if not self.db.is_connected():
            await self.db.connect()
        updated_user = await self.db.user.update(
            where={"id": id}, data={"user_name": user_name}
        )
        await self.db.disconnect()
        return updated_user

    async def get_all_files_under_user_knowledge_spaces(self, id: str) -> user:
        if not self.db.is_connected():
            await self.db.connect()
        files_under_user_knowledge_spaces = await self.db.user.find_unique(
            where={"id": id},
            include={"knowledge_spaces": {"include": {"files": True}}},
        )
        await self.db.disconnect()
        return files_under_user_knowledge_spaces


# # 做一下select方法的测试,可能在Python的prisma客户端里没有select方法，还要做一下human_readable_id的序列增加

# import asyncio

# asyncio.run()


# 测试一下update的功能方法


# 写一点测试代码
import asyncio

user_dao = UserDAO()


async def main():
    tasks = [
        user_dao.get_user_name_by_id(user_id)
        for user_id in [
            "e7a6aec2-f7d8-4911-be92-1947c8343975",
            "8cc0c135-135d-4355-a797-df82d4fca247",
        ]
    ]
    results = await asyncio.gather(*tasks)
    return results


print(asyncio.run(main()))
