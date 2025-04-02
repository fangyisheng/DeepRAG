from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import user

load_dotenv()


class UserDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_user(self, id: str, user_name: str) -> user:
        await self.db.connect()
        stored_user = await self.db.user.create(data={"id": id, "user_name": user_name})
        await self.db.disconnect()
        return stored_user

    async def get_user_name_by_id(self, id: str) -> user:
        await self.db.connect()
        found_user = await self.db.user.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_user

    async def delete_user_by_id(self, id: str) -> user:
        await self.db.connect()
        deleted_user = await self.db.user.delete(where={"id": id})
        await self.db.disconnect()
        return deleted_user

    async def get_all_users(self) -> list[user]:
        """
        这个函数可能需要进行分页查询的返回，因为可能用户数非常多
        """
        await self.db.connect()
        all_users = await self.db.user.find_many()
        await self.db.disconnect()
        return all_users

    async def search_users_by_name(self, user_name: str) -> list[user]:
        """
        这个函数根据输入的用户名对表进行模糊搜索，返回所有匹配的用户
        """
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

        await self.db.connect()
        searced_users = await self.db.user.find_many(where={"user_name": user_name})
        await self.db.disconnect()
        return searced_users
