from prisma import Prisma
from deeprag.db.dao.file.file_dao import FileDAO
from deeprag.workflow.upload_file_to_minio import upload_file_to_minio_func
import uuid
from deeprag.workflow.data_model import UploadFileToMinioResponse, MinioObjectReference
from prisma.models import file


class FileService:
    def __init__(self):
        self.dao = FileDAO()

    async def upload_new_file_to_minio(
        self, bucket_name: str, file_path: str, object_name: str
    ) -> UploadFileToMinioResponse:
        uploaded_file = await upload_file_to_minio_func(
            bucket_name, file_path, object_name
        )
        return uploaded_file

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
            id,
            knowledge_space_id,
            doc_title,
            doc_text,
            minio_bucket_name,
            minio_object_name,
        )

        return new_file

    async def get_minio_reference_by_id(self, id: str) -> MinioObjectReference:
        found_file = await self.dao.get_file_in_knowledge_space_by_doc_id(id)
        return MinioObjectReference(
            bucket_name=found_file.minio_bucket_name,
            object_name=found_file.minio_object_name,
        )

    async def delete_file_in_knowledge_space(self, id: str) -> dict[str, str]:
        file = await self.dao.delete_file_in_knowledge_space(id)

        return file.model_dump()

    async def update_existed_file_in_knowledge(
        self, id: str, data: dict
    ) -> dict[str, str]:
        file = await self.dao.update_existed_file_in_knowledge_space(id, data)

        return file.model_dump()

    async def get_file_in_knowledge_space_by_doc_id(self, id: str) -> dict[str, str]:
        file = await self.dao.get_file_in_knowledge_space_by_doc_id(id)

        return file.model_dump()

    async def get_file_in_knowledge_space_by_knowledge_space_id(
        self, knowledge_space_id: str
    ) -> list[file]:
        found_file_list = (
            await self.dao.get_file_in_knowledge_space_by_knowledge_space_id(
                knowledge_space_id
            )
        )

        return found_file_list
