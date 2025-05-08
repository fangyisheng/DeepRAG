from prisma import Prisma
from deeprag.db.dao.file.file_dao import FileDAO
from deeprag.workflow.upload_file_to_minio import upload_file_to_minio_func
import uuid
from deeprag.workflow.data_model import UploadFileToMinioResponse, MinioObjectReference
from prisma.models import file
from io import BytesIO
import asyncio


class FileService:
    def __init__(self):
        self.dao = FileDAO()

    async def upload_new_file_to_minio(
        self,
        bucket_name: str,
        object_name: str,
        string_data: str | None = None,
        metadata: dict | None = None,
        file_path: str | None = None,
        io_data: BytesIO | None = None,
    ) -> UploadFileToMinioResponse:
        uploaded_file = await upload_file_to_minio_func(
            bucket_name=bucket_name,
            file_path=file_path,
            object_name=object_name,
            string_data=string_data,
            metadata=metadata,
            io_data=io_data,
        )
        return uploaded_file

    async def bath_upload_new_file_to_minio(
        self,
        bucket_name_list: list[str],
        object_name_list: list[str],
        string_data_list: list[str] | None = None,
        metadata_list: list[dict] | None = None,
        file_path_list: list[str] | None = None,
        io_data_list: list[BytesIO] | None = None,
    ) -> list[UploadFileToMinioResponse]:
        tasks = []
        tasks = [
            upload_file_to_minio_func(
                bucket_name=bucket_name,
                file_path=file_path,
                object_name=object_name,
                string_data=string_data,
                metadata=metadata,
                io_data=io_data,
            )
            for bucket_name, file_path, object_name, string_data, metadata, io_data in zip(
                bucket_name_list,
                file_path_list,
                object_name_list,
                string_data_list,
                metadata_list,
                io_data_list,
            )
        ]
        results = await asyncio.gather(*tasks)
        return results

    # 这里的dict[str,str]还是改一下吧，结合pydantic做好具体的键值对的数据验证，方便大型项目的开发
    async def upload_new_file_to_knowledge_space(
        self,
        knowledge_space_id: str,
        doc_title: str,
        doc_text: str,
        minio_bucket_name: str,
        minio_object_name: str,
    ) -> file:
        id = str(uuid.uuid4())
        new_file = await self.dao.upload_new_file_to_knowledge_space(
            id=id,
            knowledge_space_id=knowledge_space_id,
            doc_title=doc_title,
            doc_text=doc_text,
            minio_bucket_name=minio_bucket_name,
            minio_object_name=minio_object_name,
        )

        return new_file

    async def batch_upload_file_in_knowledge_space(
        self,
        knowledge_space_id_list: list[str],
        doc_title_list: list[str],
        doc_text_list: list[str],
        minio_bucket_name_list: list[str],
        minio_object_name_list: list[str],
    ) -> list[str]:
        """
        返回文件的id列表，方便我后续调用的时候打日志
        调用的dao层的batch_upload_file_in_knowledge_space方法中使用了create_many方法，这个函数方法返回的是一个int整数，表示count数量
        """
        id_list = [str(uuid.uuid4()) for _ in range(len(doc_title_list))]
        stored_file_list_count = await self.dao.batch_upload_file_in_knowledge_space(
            id_list=id_list,
            knowledge_space_id_list=knowledge_space_id_list,
            doc_title_list=doc_title_list,
            doc_text_list=doc_text_list,
            minio_bucket_name_list=minio_bucket_name_list,
            minio_object_name_list=minio_object_name_list,
        )
        return id_list

    async def get_minio_reference_by_id(self, id: str) -> MinioObjectReference:
        found_file = await self.dao.get_file_in_knowledge_space_by_doc_id(id)
        return MinioObjectReference(
            bucket_name=found_file.minio_bucket_name,
            object_name=found_file.minio_object_name,
        )

    async def delete_file_in_knowledge_space(self, id: str) -> file:
        file = await self.dao.delete_file_in_knowledge_space(id)

        return file

    async def update_existed_file_in_knowledge_space(self, id: str, data: dict) -> file:
        file = await self.dao.update_existed_file_in_knowledge_space(id, data)

        return file

    async def get_file_in_knowledge_space_by_doc_id(self, id: str) -> file:
        file = await self.dao.get_file_in_knowledge_space_by_doc_id(id)

        return file

    async def get_file_in_knowledge_space_by_knowledge_space_id(
        self, knowledge_space_id: str
    ) -> list[file]:
        found_file_list = (
            await self.dao.get_file_in_knowledge_space_by_knowledge_space_id(
                knowledge_space_id
            )
        )

        return found_file_list

    async def get_zilliz_collection_name_by_file_id(self, id: str) -> str:
        zilliz_collection_name = await self.dao.get_zilliz_collection_name_by_file_id(
            id
        )
        return zilliz_collection_name

    async def get_index_status_by_file_id(self, id: str) -> bool:
        index_status = await self.dao.get_index_status_by_file_id(id)
        return index_status

    async def get_deep_index_status_by_file_id(self, id: str) -> bool:
        deep_index_status = await self.dao.get_deep_index_status_by_file_id(id)
        return deep_index_status
