from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import text_chunk
import uuid

load_dotenv()


class TextChunkDAO:
    def __init__(self):
        pass

    async def create_text_chunk(
        self, id: str, doc_id: str, text_chunk: str, n_tokens: str
    ) -> text_chunk:
        async with Prisma() as db:
            stored_text_chunk = await db.text_chunk.create(
                data={
                    "id": id,
                    "doc_id": doc_id,
                    "text_chunk": text_chunk,
                    "n_tokens": n_tokens,
                }
            )

        return stored_text_chunk

    async def batch_create_text_chunk(
        self,
        id_list: str,
        doc_id: str,
        text_chunk_list: list[str],
        n_tokens_list: list[int],
    ) -> int:
        async with Prisma() as db:
            stored_text_chunk_count = await db.text_chunk.create_many(
                data=[
                    {
                        "id": id,
                        "doc_id": doc_id,
                        "text_chunk": text_chunk,
                        "n_tokens": n_tokens,
                    }
                    for (id, text_chunk, n_tokens) in zip(
                        id_list, text_chunk_list, n_tokens_list
                    )
                ]
            )

        return stored_text_chunk_count

    async def get_text_chunk_by_id(self, id: str) -> text_chunk:
        async with Prisma() as db:
            found_text_chunk = await db.text_chunk.find_unique(where={"id": id})

        return found_text_chunk
