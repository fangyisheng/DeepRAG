from prisma import Prisma

class FileDAO:
    def __init__(self):
        self.db = Prisma()
    
    async def upload_new_file_to_knowledge_space(self, id: str, human_readable_id: str, knowledge_space_id: str, doc_id: str, doc_title: str, doc_text: str):
        await self.db.connect()
        file = await self.db.file.create(
            data = {
                "id": id,
                "knowledge_space_id": knowledge_space_id,
                "doc_id": doc_id,
                "doc_title": doc_title,
                "doc_text": doc_text
            }
        )
        await self.db.disconnect()
        return file
    
    async def delete_file_in_knowledge_space(self, doc_id: str):
        await self.db.connect()
        file = await self.db.file.delete(where = {"doc_id":doc_id})
        await self.db.disconnect()
        return file
    
    async def update_existed_file_in_knowledge_space(self, doc_id: str, data: dict):
        await self.db.connect()
        file = await self.db.file.delete(where = {"doc_id":doc_id},
                                         data = data)
        await self.db.disconnect()
        return file
    
    async def get_file_in_knowledge_space_by_doc_id(self, doc_id: str):
        await self.db.connect()
        file = await self.db.file.find_unique(where = {"doc_id":doc_id})
        await self.db.disconnect()
        return file
    
    