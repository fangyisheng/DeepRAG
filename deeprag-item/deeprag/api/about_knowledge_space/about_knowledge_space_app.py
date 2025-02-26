from fastapi import APIRouter
import json
from deeprag.db.dao.knowledge_space.knowledge_space_dao import KnowledgeSpaceDAO

app = APIRouter()

class KnowledgeSpace:
    id: str
    human_readable_id: str
    knowledge_space_id: str
    knowledge_space_title: str





knowledge_space_dao = KnowledgeSpaceDAO()

@app.get("/knowledge_space/{knowledge_space_id}")
async def get_knowledge_space(knowledge_space_id: str):
    knowledge_space = await knowledge_space_dao.query_by_knowledge_space_id(knowledge_space_id)
    return {
        "msg":"get knowledge_space successful",
        "data":{
            "id":knowledge_space.id,
            "human_readable_id":knowledge_space.human_readable_id,
            "knowledge_space_id":knowledge_space.knowledge_space_id,
            "knowledge_space_title":knowledge_space.knowledge_space_title
        }
    }

@app.post("/knowledge_space")
async def create_knowledge_space():
    knowledge_space = await knowledge_space_dao.


