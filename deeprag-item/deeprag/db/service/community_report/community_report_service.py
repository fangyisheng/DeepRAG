from deeprag.db.dao.community_report.community_report_dao import CommunityReportDAO


class CommunityReportService:
    def __init__(self):
        self.dao = CommunityReportDAO()

    async def get_community_report(self, id):
        community_report = await self.dao.get_community_report_by_id(id)
        return community_report.__dict__
