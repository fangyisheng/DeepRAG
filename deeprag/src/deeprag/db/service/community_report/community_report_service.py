from deeprag.db.dao.community_report.community_report_dao import CommunityReportDAO
from deeprag.workflow.data_model import (
    BatchGenerateCommunityReportResponse,
    BatchCreateCommunityReportResponse,
)
from prisma.models import community_report
import uuid


class CommunityReportService:
    def __init__(self):
        self.dao = CommunityReportDAO()

    async def get_community_report_by_id(self, id: str) -> community_report:
        community_report = await self.dao.get_community_report_by_id(id)
        return community_report.model_dump()

    async def batch_create_community_report(
        self,
        community_report_with_id_dict: BatchGenerateCommunityReportResponse,
    ) -> BatchCreateCommunityReportResponse:
        community_id_list = [key for key in community_report_with_id_dict.keys()]
        community_report_list = [
            report for report in community_report_with_id_dict.values()
        ]
        id_list = [str(uuid.uuid4()) for _ in community_report_with_id_dict.keys()]
        await self.dao.batch_create_community_report(
            community_id_list=community_id_list, id_list=id_list
        )
        return BatchCreateCommunityReportResponse(
            community_id_list=community_id_list,
            community_report_list=community_report_list,
        )
