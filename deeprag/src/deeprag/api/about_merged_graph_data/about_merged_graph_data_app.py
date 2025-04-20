from fastapi import APIRouter
from deeprag.db.service.merged_graph_data.merged_graph_data_service import (
    MergedGraphDataService,
)

merged_graph_data_service = MergedGraphDataService()


merged_graph_data_router = APIRouter(tags=["merged_graph"])


@merged_graph_data_router.get("/{id}")
async def get_merged_graph_data(id):
    merged_graph_data = await merged_graph_data_service.get_merged_graph_data_by_id(id)
    return {
        "msg": "get merged_graph_data successfully",
        "data": merged_graph_data,
        "code": 200,
    }
