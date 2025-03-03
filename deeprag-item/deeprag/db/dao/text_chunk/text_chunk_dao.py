from prisma import Prisma

class TextChunkDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_text_chunk(self, id: str , doc_id: str, text_chunk: str, text_chunk_id: str, n_tokens:str):
        await self.db.connect()
        text_chunk = await self.db.knowledge_space.create(
            data = {
                "id": id,
                "doc_id": doc_id,
                "text_chunk": text_chunk,
                "text_chunk_id": text_chunk_id,
                "n_tokens":n_tokens
            }
        )
        await self.db.disconnect()
        return text_chunk
    
    async def get_text_chunk_by_text_chunk_id(self, text_chunk_id: str):
        await self.db.connect()
        text_chunk = await self.db.knowledge_space.find_unique(where={"text_chunk_id":text_chunk_id})
        await self.db.connect()
        return text_chunk
    

    