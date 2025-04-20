from fastapi import APIRouter
from deeprag.db.service.text_chunk.text_chunk_service import TextChunkService

text_chunk_service = TextChunkService()


text_chunk_router = APIRouter(tags=["text_chunk"])


@text_chunk_router.get("/{id}")
async def get_text_chunk(id):
    text_chunk = await text_chunk_service.get_text_chunk_by_id(id)
    return {"msg": "get text_chunk successfully", "data": text_chunk, "code": 200}
