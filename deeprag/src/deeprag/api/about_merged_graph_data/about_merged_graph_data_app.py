from fastapi import APIRouter, HTTPException
from deeprag.db.service.merged_graph_data.merged_graph_data_service import (
    MergedGraphDataService,
)

merged_graph_data_service = MergedGraphDataService()


merged_graph_data_router = APIRouter(tags=["merged_graph"])


@merged_graph_data_router.get("/{id}")
async def get_merged_graph_data(id):
    found_merged_graph_data = (
        await merged_graph_data_service.get_merged_graph_data_by_id(id)
    )
    if not found_merged_graph_data:
        raise HTTPException(status_code=404, detail="merged_graph_data not found")
    return {
        "msg": "get merged_graph_data successfully",
        "data": found_merged_graph_data.model_,
        "code": 200,
    }
