from fastapi import APIRouter
from deeprag.db.service.sub_graph_data.sub_graph_data_service import SubGraphDataService


sub_graph_data_service = SubGraphDataService()

sub_graph_data_router = APIRouter()

@sub_graph_data_router.get("/{id}")
async def get_sub_graph_data(id):
    sub_graph_data =  await sub_graph_data_service.get_sub_graph_data_by_id(id)
    return {
        "msg":"get sub_graph_data successful",
        "data": sub_graph_data,
        "code": 200
    }
