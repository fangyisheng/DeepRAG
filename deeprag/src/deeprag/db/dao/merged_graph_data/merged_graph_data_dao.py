from prisma import Prisma
from dotenv import load_dotenv
from prisma.models import merged_graph_data

load_dotenv()


class MergedGraphDataDAO:
    def __init__(self):
        pass

    async def create_merged_graph_data(
        self,
        id: str,
        merged_graph_data: str,
        merged_graph_data_visualization_html: str,
    ) -> merged_graph_data:
        async with Prisma() as db:
            stored_merged_graph_data = await db.merged_graph_data.create(
                data={
                    "id": id,
                    "graph_data": merged_graph_data,
                    "merged_graph_data_visualization_html": merged_graph_data_visualization_html,
                }
            )

        return stored_merged_graph_data

    async def get_merged_graph_data_by_id(self, id: str) -> merged_graph_data:
        async with Prisma() as db:
            found_merged_graph_data = await db.merged_graph_data.find_unique(
                where={"id": id}
            )

        return found_merged_graph_data
