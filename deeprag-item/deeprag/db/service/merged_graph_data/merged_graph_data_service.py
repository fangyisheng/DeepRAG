from prisma import Prisma
from deeprag.db.dao.merged_graph_data.merged_graph_data_dao import MergedGraphDataDAO
import uuid


class MergedGraphDataService:
    def __init__(self):
        self.dao = MergedGraphDataDAO()

    # 对于merged_service的创建是存疑的？这应该是程序内部创建的
    async def create_merged_graph_data(
        self,
        merged_graph_data: str,
        merged_graph_data_visualization_html: str,
    ) -> id:
        id = str(uuid.uuid4())
        stored_merged_graph_data = await self.dao.create_merged_graph_data(
            id,
            merged_graph_data,
            merged_graph_data_visualization_html,
        )

        return id

    # 这可能才是外部的开发者和用户真正需要的servie服务
    async def get_merged_graph_data_by_id(self, id: str) -> dict:
        found_merged_graph_data = await self.dao.get_merged_graph_data_by_id(id)

        return found_merged_graph_data.model_dump()
