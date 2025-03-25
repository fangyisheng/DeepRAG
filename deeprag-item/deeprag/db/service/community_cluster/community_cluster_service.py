from deeprag.db.dao.community_cluster.community_cluster_dao import CommunityClusterDAO


class CommunityClusterService:
    def __init__(self):
        self.dao = CommunityClusterDAO()

    async def get_community_cluster(self, id) -> dict[str, str]:
        community_cluster = await self.dao.get_community_cluster_by_id(id)
        return community_cluster
