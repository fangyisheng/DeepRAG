from prisma import Prisma
from prisma.models import file
from dotenv import load_dotenv
from deeprag.db.data_model import UpdatedFile

load_dotenv()


class FileDAO:
    def __init__(self):
        self.db = Prisma()

    async def upload_new_file_to_knowledge_space(
        self,
        id: str,
        knowledge_space_id: str,
        doc_title: str,
        doc_text: str,
        minio_bucket_name: str,
        minio_object_name: str,
        # indexed: bool = False,
        # deep_indexed: bool = False,
        # file_embedding_zilliz_collection_name: str | None = None,
    ) -> file:
        await self.db.connect()
        stored_file = await self.db.file.create(
            data={
                "id": id,
                "knowledge_space_id": knowledge_space_id,
                "doc_title": doc_title,
                "doc_text": doc_text,
                "minio_bucket_name": minio_bucket_name,
                "minio_object_name": minio_object_name,
            },
            include={
                "KnowledgeSpaceFile": True,
            },
        )
        await self.db.disconnect()
        return stored_file

    async def delete_file_in_knowledge_space(self, id: str) -> file:
        await self.db.connect()
        deleted_file = await self.db.file.delete(where={"id": id})
        await self.db.disconnect()
        return deleted_file

    async def update_existed_file_in_knowledge_space(self, id: str, data: dict) -> file:
        await self.db.connect()
        updated_file = await self.db.file.update(where={"id": id}, data=data)
        await self.db.disconnect()
        return updated_file

    async def get_file_in_knowledge_space_by_doc_id(self, id: str) -> file:
        await self.db.connect()
        found_file = await self.db.file.find_unique(
            where={"id": id},
            include={
                "text_chunks": {
                    "include": {
                        "sub_graph_datas": {
                            "include": {
                                "SubGraphDataMergedGraphData": True  # 注意这里是正确的 include 语法
                            }
                        }
                    }
                }
            },
        )
        await self.db.disconnect()
        return found_file

    async def get_file_in_knowledge_space_by_knowledge_space_id(self, id: str) -> file:
        await self.db.connect()
        found_file_list = await self.db.file.find_many(where={"knowledge_space_id": id})
        await self.db.disconnect()
        return found_file_list

    async def get_zilliz_collection_name_by_file_id(self, id: str) -> str:
        await self.db.connect()
        found_file = await self.db.file.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_file.file_embedding_zilliz_collection_name

    async def get_index_status_by_file_id(self, id: str) -> bool:
        await self.db.connect()
        found_file = await self.db.file.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_file.indexed

    async def get_deep_index_status_by_file_id(self, id: str) -> bool:
        await self.db.connect()
        found_file = await self.db.file.find_unique(where={"id": id})
        await self.db.disconnect()
        return found_file.deep_indexed


# # 撰写测试代码
# import asyncio

# file_dao = FileDAO()


# async def test():
#     data = await file_dao.upload_new_file_to_knowledge_space(
#         id="1", knowledge_space_id="1", doc_title="test", doc_text="test"
#     )
#     print(data)
#     print(type(data))


# print(asyncio.run(test()))
