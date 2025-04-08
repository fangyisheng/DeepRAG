from deeprag.db.dao.sub_graph_data.sub_graph_data_dao import SubGraphDataDAO
import uuid


class SubGraphDataService:
    def __init__(self):
        self.dao = SubGraphDataDAO()

    async def create_sub_graph_data(
        self,
        id: str,
        text_chunk_id: str,
        sub_graph_data: str,
        merged_graph_data_id: str,
    ):
        stored_sub_graph_data = await self.dao.create_sub_graph_data(
            id,
            text_chunk_id,
            sub_graph_data,
            merged_graph_data_id,
        )

        return stored_sub_graph_data.model_dump()

    async def batch_create_sub_graph_data(
        self,
        text_chunk_id_list: list[str],
        sub_graph_data_list: list[str],
        merged_graph_data_id: str,
    ) -> int:
        id_list = [str(uuid.uuid4()) for _ in range(len(text_chunk_id_list))]
        stored_sub_graph_data_count = await self.dao.batch_create_sub_graph_data(
            id_list, text_chunk_id_list, sub_graph_data_list, merged_graph_data_id
        )
        return stored_sub_graph_data_count

    async def get_sub_graph_data_by_id(self, id: str):
        sub_graph_data = await self.dao.get_sub_graph_data_by_id(id)

        return sub_graph_data.model_dump()
