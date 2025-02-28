from prisma import Prisma
from deeprag.db.dao.file.file_dao import FileDAO

class FileService:
    def __init__(self):
        self.dao = FileDAO()
    
    async def upload_new_file_to_knowledge_space_service(self, id: str, knowledge_space_id: str, doc_id: str, doc_title: str, doc_text: str):
 
        file = await self.dao.upload_new_file_to_knowledge_space(
        id,
        knowledge_space_id,
        doc_id,
        doc_title,
        doc_text
        )
  
        return file.__dict__
    
    async def delete_file_in_knowledge_space_service(self, doc_id: str):
  
        file = await self.dao.delete_file_in_knowledge_space(doc_id)

        return file.__dict__
    
    async def update_existed_file_in_knowledge_space_service(self, doc_id: str, data: dict):

        file = await self.dao.update_existed_file_in_knowledge_space(doc_id,
                                       data)

        return file.__dict__
    
    async def get_file_in_knowledge_space_by_doc_id_service(self, doc_id: str):

        file = await self.dao.get_file_in_knowledge_space_by_doc_id(doc_id)

        return file.__dict__
    
    