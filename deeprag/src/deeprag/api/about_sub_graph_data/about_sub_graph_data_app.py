from fastapi import APIRouter, HTTPException
from deeprag.db.service.sub_graph_data.sub_graph_data_service import SubGraphDataService
from fastapi.responses import JSONResponse

sub_graph_data_service = SubGraphDataService()

sub_graph_data_router = APIRouter(tags=["sub_graph_data"])


@sub_graph_data_router.get("/{id}")
async def get_sub_graph_data(id: str):
    found_sub_graph_data = await sub_graph_data_service.get_sub_graph_data_by_id(id)
    if not found_sub_graph_data:
        raise HTTPException(status_code=404, detail="sub_graph_data not found")
    result = {
        "msg": "get sub_graph_data successful",
        "data": found_sub_graph_data.model_dump(),
        "code": 200,
    }
    return JSONResponse(content=result)
