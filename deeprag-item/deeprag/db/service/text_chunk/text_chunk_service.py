from prisma import Prisma
from deeprag.db.dao.text_chunk.text_chunk_dao import TextChunkDAO


class TextChunkService:
    def __init__(self):
        self.dao = TextChunkDAO()

    async def create_text_chunk_service(self, id: str , doc_id: str, text_chunk: str, text_chunk_id: str):
       
        text_chunk = await self.dao.create_text_chunk(
            id,
            doc_id,
            text_chunk,
            text_chunk_id
            
        )
        
        return text_chunk.__dict__
    
    async def get_text_chunk_by_text_chunk_id_service(self, text_chunk_id: str):
       
        text_chunk = await self.dao.get_text_chunk_by_text_chunk_id(where=text_chunk_id)
     
        return text_chunk.__dict__