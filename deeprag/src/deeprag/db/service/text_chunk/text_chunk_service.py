from deeprag.db.dao.text_chunk.text_chunk_dao import TextChunkDAO
import uuid
from deeprag.workflow.data_model import ChunkedTextUnit, TokenListByTextChunk


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
        self,
        doc_id: str,
        text_chunk_list: ChunkedTextUnit,
        n_tokens_list: TokenListByTextChunk,
    ):
        id_list = [str(uuid.uuid4()) for _ in text_chunk_list]
        stored_text_chunks_count = await self.dao.batch_create_text_chunk(
            id_list, doc_id, text_chunk_list.root, n_tokens_list.root
        )
        return id_list

    async def get_text_chunk_by_id(self, id: str):
        found_text_chunk = await self.dao.get_text_chunk_by_id(id)

        return found_text_chunk
