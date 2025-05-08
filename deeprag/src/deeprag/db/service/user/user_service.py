from deeprag.db.dao.user.user_dao import UserDAO
import uuid
from prisma.models import user, file


class UserService:
    def __init__(self):
        self.dao = UserDAO()

    async def create_user(self, user_name: str) -> user:
        id = str(uuid.uuid4())
        stored_user = await self.dao.create_user(id, user_name)
        return stored_user

    async def get_user_name_by_id(self, id: str) -> user:
        found_user = await self.dao.get_user_name_by_id(id)
        return found_user

    async def get_all_users(self) -> list[user]:
        all_users = await self.dao.get_all_users()
        return [user for user in all_users]

    async def delete_user(self, id: str) -> user:
        deleted_user = await self.dao.delete_user_by_id(id)
        return deleted_user

    async def search_users_by_name(self, user_name: str) -> list[user]:
        found_users = await self.dao.search_users_by_name(user_name)
        return found_users

    async def get_users_by_user_name(self, user_name: str) -> list[user]:
        found_users = await self.dao.get_users_by_user_name(user_name)
        return found_users

    async def get_all_files_under_user_knowledge_spaces(self, id: str) -> list[file]:
        files_under_user_knowledge_spaces = (
            await self.dao.get_all_files_under_user_knowledge_spaces(id)
        )
        found_file_list = [
            file
            for knowledge_space in files_under_user_knowledge_spaces.knowledge_spaces
            for file in knowledge_space.files
        ]
        return found_file_list


# # 测试代码
# user_service = UserService()
# import asyncio

# print(
#     asyncio.run(
#         user_service.get_all_files_under_user_knowledge_spaces(
#             "e7a6aec2-f7d8-4911-be92-1947c8343975"
#         )
#     )
# )
