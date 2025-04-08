from deeprag.db.dao.community_report.community_report_dao import CommunityReportDAO


class CommunityReportService:
    def __init__(self):
        self.dao = CommunityReportDAO()

    async def get_community_report_by_id(self, id: str) -> dict[str, str]:
        community_report = await self.dao.get_community_report_by_id(id)
        return community_report.model_dump()

    async def batch_create_community_report(
        self,
        id_list: list[str],
        community_report_list: list[str],
        community_id: list[str],
    ) -> int:
        stored_community_report = self.dao.batch_create_community_report(
            id_list, community_report_list, community_id
        )
        return stored_community_report
