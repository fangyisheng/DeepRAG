from prisma import Prisma
from deeprag.db.dao.sub_graph_data.sub_graph_data_dao import SubGraphDataDAO



class SubGraphDataService:
    def __init__(self):
        self.dao = SubGraphDataDAO()

    async def create_sub_graph_data(self, id: str , text_chunk_id: str, sub_graph_data: str, merged_graph_data_id: str):
      
        sub_graph_data = await self.dao.create_sub_graph_data(
            data = {
                "id": id,
                "text_chunk_id": text_chunk_id,
                "sub_graph_data": sub_graph_data,
                "merged_graph_data_id": merged_graph_data_id
            }
        )
       
        return sub_graph_data.__dict__
    
    async def get_sub_graph_data_by_id(self, id: str):
       
        sub_graph_data = await self.dao.get_sub_graph_data_by_id(where={"id":id})
        
        return sub_graph_data.__dict__