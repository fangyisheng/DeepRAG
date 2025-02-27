from prisma import Prisma

class MergedGraphDataDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_merged_graph_data(self, id: str ,sub_graph_data_id: str, merged_graph_data: str, merged_graph_data_id: str):
        await self.db.connect()
        merged_graph_data = await self.db.merged_graph_data.create(
            data = {
                "id": id,
                "sub_graph_data_id": sub_graph_data_id,
                "merged_graph_data":merged_graph_data,
                "merged_graph_data_id":merged_graph_data_id
            }
        )
        await self.db.disconnect()
        return merged_graph_data
    
    async def get_merged_graph_data_by_merged_graph_data_id(self, merged_graph_data_id: str):
        await self.db.connect()
        merged_graph_data = await self.db.sub_graph_data.find_unique(where={"merged_graph_data_id":merged_graph_data_id})
        await self.db.connect()
        return merged_graph_data