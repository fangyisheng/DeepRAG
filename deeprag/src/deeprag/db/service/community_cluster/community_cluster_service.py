from deeprag.db.dao.community_cluster.community_cluster_dao import CommunityClusterDAO
from prisma.models import community_cluster
from deeprag.workflow.data_model import BatchGenerateCommunityReportResponse


class CommunityClusterService:
    def __init__(self):
        self.dao = CommunityClusterDAO()

    async def get_community_cluster_by_id(self, id) -> community_cluster:
        community_cluster = await self.dao.get_community_cluster_by_id(id)
        return community_cluster

    async def batch_create_community_cluster(
        self,
        community_reports_structed_and_unstructed_bundle: BatchGenerateCommunityReportResponse,
    ) -> int:
        community_cluster_list = []

        for key in community_reports_structed_and_unstructed_bundle.community_reports_structed_data_with_community_id.keys():
            community_cluster_list.append(
                community_cluster(
                    id=key,
                    community_title=community_reports_structed_and_unstructed_bundle.community_reports_structed_data_with_community_id[
                        key
                    ].title,
                )
            )

        stored_community_cluster_list = await self.dao.batch_create_community_cluster(
            community_cluster_list
        )
        return stored_community_cluster_list
