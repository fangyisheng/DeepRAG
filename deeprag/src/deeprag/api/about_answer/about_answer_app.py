from fastapi import FastAPI,APIRouter
from fastapi.responses import StreamingResponse
from deeprag.core import DeepRAG




chat_router = APIRouter(tags = ["chat"])


deeprag = DeepRAG()
@chat_router.post("/completions")
async def chat():
    

