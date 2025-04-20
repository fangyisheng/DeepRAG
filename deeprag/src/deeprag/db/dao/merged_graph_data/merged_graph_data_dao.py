from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import merged_graph_data

load_dotenv()


class MergedGraphDataDAO:
    def __init__(self):
        self.db = Prisma()

    async def create_merged_graph_data(
        self,
        id: str,
        merged_graph_data: str,
        merged_graph_data_visualization_html: str,
    ) -> merged_graph_data:
        await self.db.connect()
        stored_merged_graph_data = await self.db.merged_graph_data.create(
            data={
                "id": id,
                "merged_graph_data": merged_graph_data,
                "merged_graph_data_visualization_html": merged_graph_data_visualization_html,
            }
        )
        await self.db.disconnect()
        return stored_merged_graph_data

    async def get_merged_graph_data_by_id(self, id: str) -> merged_graph_data:
        await self.db.connect()
        found_merged_graph_data = await self.db.merged_graph_data.find_unique(
            where={"id": id}
        )
        await self.db.connect()
        return found_merged_graph_data
