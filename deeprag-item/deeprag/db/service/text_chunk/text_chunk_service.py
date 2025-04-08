from deeprag.db.dao.text_chunk.text_chunk_dao import TextChunkDAO
import uuid


class TextChunkService:
    def __init__(self):
        self.dao = TextChunkDAO()

    async def create_text_chunk(self, doc_id: str, text_chunk: str, n_tokens):
        id = str(uuid.uuid4())
        stored_text_chunk = await self.dao.create_text_chunk(
            id, doc_id, text_chunk, n_tokens
        )

        return stored_text_chunk.model_dump()

    async def batch_create_text_chunk(
        self, doc_id: str, text_chunk_list: list[str], n_tokens_list: list[int]
    ):
        id_list = [str(uuid.uuid4()) for _ in text_chunk_list]
        stored_text_chunks_count = await self.dao.batch_create_text_chunk(
            id_list, doc_id, text_chunk_list, n_tokens_list
        )
        return id_list

    async def get_text_chunk_by_id(self, id: str):
        found_text_chunk = await self.dao.get_text_chunk_by_id(id)

        return found_text_chunk.model_dump()
