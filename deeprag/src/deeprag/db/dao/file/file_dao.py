from prisma import Prisma
from prisma.models import file
from dotenv import load_dotenv
from deeprag.db.data_model import UpdatedFile

load_dotenv()


class FileDAO:
    def __init__(self):
        pass

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
        async with Prisma() as db:
            stored_file = await db.file.create(
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

        return stored_file

    async def batch_upload_file_in_knowledge_space(
        self,
        id_list: list[str],
        knowledge_space_id_list: list[str],
        doc_title_list: list[str],
        doc_text_list: list[str],
        minio_bucket_name_list: list[str],
        minio_object_name_list: list[str],
    ) -> int:
        async with Prisma() as db:
            stored_file_list_count = await db.file.create_many(
                data=[
                    {
                        "id": id,
                        "knowledge_space_id": knowledge_space_id,
                        "doc_title": doc_title,
                        "doc_text": doc_text,
                        "minio_bucket_name": minio_bucket_name,
                        "minio_object_name": minio_object_name,
                    }
                    for (
                        id,
                        knowledge_space_id,
                        doc_title,
                        doc_text,
                        minio_bucket_name,
                        minio_object_name,
                    ) in zip(
                        id_list,
                        knowledge_space_id_list,
                        doc_title_list,
                        doc_text_list,
                        minio_bucket_name_list,
                        minio_object_name_list,
                    )
                ],
            )

        return stored_file_list_count

    async def delete_file_in_knowledge_space(self, id: str) -> file:
        async with Prisma() as db:
            deleted_file = await db.file.delete(where={"id": id})

        return deleted_file

    async def update_existed_file_in_knowledge_space(self, id: str, data: dict) -> file:
        async with Prisma() as db:
            updated_file = await db.file.update(where={"id": id}, data=data)

        return updated_file

    async def get_file_in_knowledge_space_by_doc_id(self, id: str) -> file:
        async with Prisma() as db:
            found_file = await db.file.find_unique(
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

        return found_file

    async def get_file_in_knowledge_space_by_knowledge_space_id(self, id: str) -> file:
        async with Prisma() as db:
            found_file_list = await db.file.find_many(where={"knowledge_space_id": id})

        return found_file_list

    async def get_zilliz_collection_name_by_file_id(self, id: str) -> str:
        async with Prisma() as db:
            found_file = await db.file.find_unique(where={"id": id})

        return found_file.file_embedding_zilliz_collection_name

    async def get_index_status_by_file_id(self, id: str) -> bool:
        async with Prisma() as db:
            found_file = await db.file.find_unique(where={"id": id})

        return found_file.indexed

    async def get_deep_index_status_by_file_id(self, id: str) -> bool:
        async with Prisma() as db:
            found_file = await db.file.find_unique(where={"id": id})

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
