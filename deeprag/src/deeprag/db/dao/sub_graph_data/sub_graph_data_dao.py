from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import sub_graph_data

load_dotenv()


class SubGraphDataDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_sub_graph_data(
        self,
        id: str,
        text_chunk_id: str,
        sub_graph_data: str,
        merged_graph_data_id: str,
    ) -> sub_graph_data:
        await self.db.connect()
        stored_sub_graph_data = await self.db.sub_graph_data.create(
            data={
                "id": id,
                "text_chunk_id": text_chunk_id,
                "graph_data": sub_graph_data,
                "merged_graph_data_id": merged_graph_data_id,
            }
        )
        await self.db.disconnect()
        return stored_sub_graph_data

    async def batch_create_sub_graph_data(
        self,
        id_list: str,
        text_chunk_id_list: list[str],
        sub_graph_data_list: list[str],
        merged_graph_data_id: str,
    ) -> int:
        await self.db.connect()
        stored_sub_graph_data_count = await self.db.sub_graph_data.create_many(
            data=[
                {
                    "id": id,
                    "text_chunk_id": text_chunk_id,
                    "graph_data": graph_data,
                    "merged_graph_data_id": merged_graph_data_id,
                }
                for (id, text_chunk_id, graph_data) in zip(
                    id_list, text_chunk_id_list, sub_graph_data_list
                )
            ]
        )
        await self.db.disconnect()
        return stored_sub_graph_data_count

    async def get_sub_graph_data_by_id(self, id: str) -> sub_graph_data:
        await self.db.connect()
        found_sub_graph_data = await self.db.sub_graph_data.find_unique(
            where={"id": id}
        )
        await self.db.connect()
        return found_sub_graph_data
