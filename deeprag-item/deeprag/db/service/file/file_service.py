from prisma import Prisma
from deeprag.db.dao.file.file_dao import FileDAO


class FileService:
    def __init__(self):
        self.dao = FileDAO()

    # 这里的dict[str,str]还是改一下吧，结合pydantic做好具体的键值对的数据验证，方便大型项目的开发
    async def upload_new_file_to_knowledge_space(
        self, id: str, knowledge_space_id: str, doc_title: str, doc_text: str
    ) -> dict[str, str]:
        file = await self.dao.upload_new_file_to_knowledge_space(
            id, knowledge_space_id, doc_title, doc_text
        )

        return file.__dict__

    async def delete_file_in_knowledge_space(self, id: str) -> dict[str, str]:
        file = await self.dao.delete_file_in_knowledge_space(id)

        return file.__dict__

    async def update_existed_file_in_knowledge(
        self, id: str, data: dict
    ) -> dict[str, str]:
        file = await self.dao.update_existed_file_in_knowledge_space(id, data)

        return file.__dict__

    async def get_file_in_knowledge_space_by_doc_id(self, id: str) -> dict[str, str]:
        file = await self.dao.get_file_in_knowledge_space_by_doc_id(id)

        return file.__dict__
