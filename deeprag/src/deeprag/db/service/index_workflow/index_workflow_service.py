from deeprag.db.dao.index_workflow.index_workflow_dao import IndexWorkFlowDAO
from prisma.models import index_workflow
import uuid


class IndexWorkFlowService:
    def __init__(self):
        self.dao = IndexWorkFlowDAO()

    async def create_workflow(
        self,
        status: str,
        action: str,
        workflow_start_time: str | None = None,
        workflow_end_time: str | None = None,
        workflow_duration_time: str | None = None,
        llm_cost_tokens: int | None = None,
        embedding_cost_tokens: int | None = None,
    ) -> index_workflow:
        id = str(uuid.uuid4())
        created_workflow = await self.dao.create_workflow(
            id,
            status,
            action,
            workflow_start_time,
            workflow_end_time,
            workflow_duration_time,
            llm_cost_tokens,
            embedding_cost_tokens,
        )
        return created_workflow

    async def get_workflow_by_id(self, id: str) -> index_workflow:
        found_workflow = await self.dao.get_workflow_by_id(id)
        return found_workflow  # 这边的返回需要定制一下 毕竟是Service层

    async def get_workflow_by_message_id(self, message_id: str) -> index_workflow:
        found_workflow = await self.dao.get_workflow_by_message_id(message_id)
        return found_workflow  # 这边的返回需要定制一下 毕竟是Service层

    async def update_workflow(
        self,
        id: str,
        status: str | None = None,
        action: str | None = None,
        workflow_start_time: str | None = None,
        workflow_end_time: str | None = None,
        workflow_duration_time: str | None = None,
        llm_cost_tokens: int | None = None,
        embedding_cost_tokens: int | None = None,
    ) -> index_workflow:
        updated_workflow = await self.dao.update_workflow(
            id,
            status,
            action,
            workflow_start_time,
            workflow_end_time,
            workflow_duration_time,
            llm_cost_tokens,
            embedding_cost_tokens,
        )
        return updated_workflow
