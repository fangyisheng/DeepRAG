from prisma import Prisma
from dotenv import load_dotenv

load_dotenv()


class MergedGraphDataDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_merged_graph_data(
        self,
        id: str,
        sub_graph_data_id: str,
        merged_graph_data: str,
        merged_graph_data_visualization_html: str,
    ):
        await self.db.connect()
        stored_merged_graph_data = await self.db.merged_graph_data.create(
            data={
                "id": id,
                "sub_graph_data_id": sub_graph_data_id,
                "merged_graph_data": merged_graph_data,
                "merged_graph_data_visualization_html": merged_graph_data_visualization_html,
            }
        )
        await self.db.disconnect()
        return stored_merged_graph_data.model_dump()

    async def get_merged_graph_data_by_id(self, id: str):
        await self.db.connect()
        found_merged_graph_data = await self.db.merged_graph_data.find_unique(
            where={"id": id}
        )
        await self.db.connect()
        return found_merged_graph_data.model_dump()
