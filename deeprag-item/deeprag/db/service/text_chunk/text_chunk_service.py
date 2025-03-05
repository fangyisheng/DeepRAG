from prisma import Prisma
from deeprag.db.dao.text_chunk.text_chunk_dao import TextChunkDAO


class TextChunkService:
    def __init__(self):
        self.dao = TextChunkDAO()

    async def create_text_chunk(self, id: str , doc_id: str, text_chunk: str, text_chunk_id: str, n_tokens):
       
        text_chunk = await self.dao.create_text_chunk(
            id,
            doc_id,
            text_chunk,
            text_chunk_id,
            n_tokens
        )
        
        return text_chunk.__dict__
    
    async def get_text_chunk_by_id(self, id: str):
       
        text_chunk = await self.dao.get_text_chunk_by_id(where={"id":id})
     
        return text_chunk.__dict__