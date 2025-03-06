from fastapi import FastAPI,APIRouter
from fastapi.responses import StreamingResponse

chat_router = APIRouter(tags = ["chat"])

@chat_router.post("/completions")
async def chat():

