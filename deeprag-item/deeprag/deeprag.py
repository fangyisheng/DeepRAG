from deeprag.workflow.upload_file_to_minio import upload_file_to_minio_func
from deeprag.workflow.text_extract_and_clean import process_text
from deeprag.workflow.text_chunk_based_by_token import TextSplitter
from deeprag.workflow.batch_text_chunk_generate_graphs import (
    batch_text_chunk_generate_graphs_process,
)
from deeprag.workflow.batch_text_chunk_generate_embeddings import (
    batch_text_chunk_generate_embeddings_process,
)
from deeprag.workflow.graph_storage_to_html_with_no_leiden import (
    store_graph_data_to_html_with_no_leiden,
)  # 可视化的函数方法
from deeprag.workflow.merge_sub_graph import merge_sub_entity_relationship_graph
from deeprag.workflow.graph_description import GraphDescription
from deeprag.workflow.vector_with_text_to_vector_db import data_insert_to_vector_db
from deeprag.workflow.vector_query_to_vector_db import query_vector_db_by_vector
from deeprag.workflow.final_rag_answer import (
    final_rag_answer_process_stream,
    final_rag_answer_process_not_stream,
)
from deeprag.workflow.batch_generate_community_report import (
    batch_generate_community_report_func,
)

from deeprag.db.service.knowledge_space.knowledge_space_service import (
    KnowledgeSpaceService,
)

from deeprag.db.service.file.file_service import FileService
from deeprag.db.service.user.user_service import UserService
from deeprag.workflow.data_model import (
    CompleteTextUnit,
    KnowledgeScope,
    ChunkedTextUnit,
    BatchTextChunkGenerateGraphsResponse,
    CompleteGraphData,
    GraphDescriptionResponse,
    BatchTextChunkGenerateEmbeddingsResponse,
    BatchGenerateCommunityReportResponse,
    GraphDescriptionWithCommunityClusterResponse,
    TokenListByTextChunk,
    SearchedTextResponse
)


class DeepRAG:
    def __init__(self):
        self.file_service = FileService()
        self.knowledge_space_service = KnowledgeSpaceService()
        self.user_service = UserService()

    async def delete_file(self, file_id: str):
        await self.file_service.delete_file_in_knowledge_space(file_id)

    async def delete_knowledge_space(self, knowledge_space_id: str):
        await self.knowledge_space_service.delete_knowledge_space(knowledge_space_id)

    async def delete_user(self, user_id: str):
        await self.user_service.delete_user(user_id)

    async def index(
        self,
        file_path: str,
        collection_name: str,
        knowledge_scope: str|list[KnowledgeScope]|None = None,
        meta_data: str | list | None = None,
        deep_index_pattern: bool = False,
    ):
        """index_pattern是一个很重要的概念，代表你要覆盖还是说要新增，这是一个需要区分的字段???这是存疑的。需要再讨论一下，
        不需要之前说的partition_name了
        knowledge_scope 是一个字典的列表，字典需要的形式为：
        {
            "user_id":"",
            "knowledge_space_id":"",
            "file_id":""
        }

        meta_data 由用户自己定义啦！~

        """

        # 首先提取干净的文本
        cleaned_text: CompleteTextUnit = await process_text(file_path)
        # 然后进行文本切分
        splitter = TextSplitter()
        chunks: ChunkedTextUnit = await splitter.split_text_by_token(cleaned_text)
        token_list: TokenListByTextChunk = splitter.tokens_by_chunk
        # 开始提取图结构
        graphs: BatchTextChunkGenerateGraphsResponse = (
            await batch_text_chunk_generate_graphs_process(chunks)
        )
        # 开始合并每个文本分块得到的子图结构变成一张完整的图谱结构
        merged_graph: CompleteGraphData = await merge_sub_entity_relationship_graph(
            graphs
        )
        # 得到完整的图谱结构以后，要对其中的关系加以描述
        graph_description = GraphDescription()
        relation_description: GraphDescriptionResponse = (
            await graph_description.describe_graph(merged_graph)
        )
        # 利用embedding模型生成embedding向量
        embedding_vector: BatchTextChunkGenerateEmbeddingsResponse = (
            await batch_text_chunk_generate_embeddings_process(relation_description)
        )
        # 将描述好的关系描述,以及关系描述的embedding向量以及附带的metadata嵌入到zilliz向量数据库中，目前我的metadata信息只有原文件名，考虑以后的可扩展性？现在考虑好了
        if isinstance(meta_data, str) :
                meta_data = [meta_data for _ in range(len(embedding_vector))]
        if isinstance(knowledge_scope, str):
                knowledge_scope = [knowledge_scope for _ in range(len(embedding_vector))]
        if not deep_index_pattern:
            
            await data_insert_to_vector_db(
                relation_description,
                embedding_vector,
                collection_name,
                knowledge_scope,
                meta_data,
            )
        else:
            # 如果是deep_index_pattern 那么要生成社区报告。首先做好社区划分。
            relation_description_with_community_id: GraphDescriptionWithCommunityClusterResponse = await graph_description.describe_graph_with_community_cluster(
                merged_graph
            )
            community_report_with_community_id: BatchGenerateCommunityReportResponse = (
                await batch_generate_community_report_func(
                    relation_description_with_community_id
                )
            )
            community_report_content = [
                value.community_report
                for value in community_report_with_community_id.values()
            ]
            await data_insert_to_vector_db(
                community_report_content,
                embedding_vector,
                collection_name,
                knowledge_scope,
                meta_data,
            )
        return 

    async def query(self,user_prompt:str,stream:bool,collection_name:str,knowledge_scope:KnowledgeScope,session_id:str,context:list |None = None):
        """感觉这里的context参数是可以保留那种原始的历史记录，也可以让用户手动增加的，保留更多灵活性,
        session_id如果是空白的，那就是新开一个会话，这个逻辑是可通的"""
        

        #首先利用输入的query对向量数据库进行有筛选的检索
        searched_text: SearchedTextResponse = await query_vector_db_by_vector(
            user_prompt,
            collection_name,
            knowledge_scope,
        )
        if stream:
             async for response in final_rag_answer_process_stream(
                user_prompt,
                collection_name,
                searched_text.searched_file_name,
                searched_text,
                context
            ):
                yield response


    async def index_and_query(self,file_path,user_prompt,context):
