from prisma import Prisma


class SubGraphDataDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_sub_graph_data(
        self,
        id: str,
        text_chunk_id: str,
        sub_graph_data: str,
        merged_graph_data_id: str,
    ):
        await self.db.connect()
        sub_graph_data = await self.db.sub_graph_data.create(
            data={
                "id": id,
                "text_chunk_id": text_chunk_id,
                "sub_graph_data": sub_graph_data,
                "merged_graph_data_id": merged_graph_data_id,
            }
        )
        await self.db.disconnect()
        return sub_graph_data

    async def get_sub_graph_data_by_id(self, id: str):
        await self.db.connect()
        sub_graph_data = await self.db.sub_graph_data.find_unique(where={"id": id})
        await self.db.connect()
        return sub_graph_data
