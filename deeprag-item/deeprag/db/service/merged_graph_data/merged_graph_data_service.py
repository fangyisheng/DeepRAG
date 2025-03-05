from prisma import Prisma
from deeprag.db.dao.merged_graph_data.merged_graph_data_dao import MergedGraphDataDAO


class MergedGraphDataService:
    def __init__(self):
        self.dao = MergedGraphDataDAO()

    async def create_merged_graph_data(self, id: str ,sub_graph_data_id: str, merged_graph_data: str, merged_graph_data_visualization_html:str):
    
        merged_graph_data = await self.dao.create_merged_graph_data(
        
            id,
            sub_graph_data_id,
            merged_graph_data,
            merged_graph_data_visualization_html
        )
    
        return merged_graph_data.__dict__
    
    async def get_merged_graph_data_by_id(self, id: str):
  
        merged_graph_data = await self.dao.get_merged_graph_data_by_id(id)
    
        return merged_graph_data.__dict__