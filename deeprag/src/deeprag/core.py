from deeprag.workflow.upload_file_to_minio import upload_file_to_minio_func
from deeprag.workflow.text_extract_and_clean import process_text
from deeprag.workflow.text_chunk_process import TextSplitter
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
from deeprag.workflow.graph_description_enrichment import GraphDescriptionEnrichment
from deeprag.workflow.vector_with_text_to_vector_db import data_insert_to_vector_db
from deeprag.workflow.vector_query_to_vector_db import query_vector_db_by_vector
from deeprag.workflow.final_rag_answer import (
    final_rag_answer_process_stream,
    final_rag_answer_process_not_stream,
)
from deeprag.workflow.batch_generate_community_report import (
    batch_generate_community_report_func,
)
from deeprag.workflow.graph_storage_to_html_with_leiden import (
    realize_leiden_community_algorithm,
)
from deeprag.workflow.flatten_entity_relation import (
    flatten_entity_relation_func,
)
from deeprag.db.service.knowledge_space.knowledge_space_service import (
    KnowledgeSpaceService,
)
from deeprag.db.service.community_report.community_report_service import (
    CommunityReportService,
)
from deeprag.db.service.community_cluster.community_cluster_service import (
    CommunityClusterService,
)
from deeprag.db.service.file.file_service import FileService
from deeprag.db.service.user.user_service import UserService
from deeprag.db.service.user_knowledge_space_file_service import (
    UserKnowledgeSpaceFileService,
)
from deeprag.db.service.sub_graph_data.sub_graph_data_service import (
    SubGraphDataService,
)
from deeprag.db.service.text_chunk.text_chunk_service import TextChunkService
from deeprag.db.service.llm_chat.llm_chat_service import LLMChatService
from deeprag.db.service.merged_graph_data.merged_graph_data_service import (
    MergedGraphDataService,
)
from deeprag.db.service.flatten_entity_relation.flatten_entity_relation_service import (
    FlattenEntityRelationService,
)
from deeprag.db.service.index_workflow.index_workflow_service import (
    IndexWorkFlowService,
)
from deeprag.db.service.rag_param.rag_param_service import RagParamService
from deeprag.db.data_model import RoleMessage
from deeprag.workflow.data_model import (
    CompleteTextUnit,
    ChunkedTextUnit,
    KnowledgeScopeMinioMapping,
    MinioObjectReference,
    KnowledgeScopeLocator,
    KnowledgeScopeRealName,
    BatchTextChunkGenerateGraphsResponse,
    CompleteGraphData,
    GraphDescriptionResponse,
    BatchTextChunkGenerateEmbeddingsResponse,
    BatchGenerateCommunityReportResponse,
    GraphDescriptionWithCommunityClusterResponse,
    TokenListByTextChunk,
    SearchedTextResponse,
    GraphDataAddCommunityWithVisualization,
    FlattenEntityRelation,
    BatchCreateCommunityReportResponse,
    CostTokens,
)
from prisma.models import file, knowledge_space, user, index_workflow
from pathlib import Path
import uuid
import asyncio
from loguru import logger
from deeprag.rag_core_utils.utils.context_holder import (
    llm_token_usage_var,
    embedding_token_usage_var,
)
import json
from datetime import datetime
import ast


class DeepRAG:
    def __init__(self):
        self.file_service = FileService()
        self.knowledge_space_service = KnowledgeSpaceService()
        self.user_service = UserService()
        self.user_knowledge_space_file_service = UserKnowledgeSpaceFileService()
        self.llm_chat_service = LLMChatService()
        self.text_chunk_service = TextChunkService()
        self.sub_graph_data_service = SubGraphDataService()
        self.merged_graph_data_service = MergedGraphDataService()
        self.community_report_service = CommunityReportService()
        self.flatten_entity_relation_service = FlattenEntityRelationService()
        self.community_cluster_service = CommunityClusterService()
        self.index_workflow_service = IndexWorkFlowService()
        self.rag_param_service = RagParamService()
        # self.cost_index_llm_tokens = 0
        # self.cost_index_embedding_tokens = 0
        # self.cost_chat_llm_tokens = 0

    async def delete_file(self, file_id: str) -> file:
        deleted_file = await self.file_service.delete_file_in_knowledge_space(file_id)

        return deleted_file

    async def delete_knowledge_space(self, knowledge_space_id: str) -> knowledge_space:
        deleted_knowledge_space = (
            await self.knowledge_space_service.delete_knowledge_space(
                knowledge_space_id
            )
        )
        return deleted_knowledge_space

    async def delete_user(self, user_id: str) -> user:
        deleted_user = await self.user_service.delete_user(user_id)
        return deleted_user

    async def create_user(self, user_name: str) -> user:
        stored_user = await self.user_service.create_user(user_name)
        logger.info(f"创建用户空间{stored_user.id}成功")
        return stored_user

    async def create_knowledge_space(
        self, user_id: str, knowledge_space_name: str
    ) -> knowledge_space:
        stored_knowledge_space = (
            await self.knowledge_space_service.create_knowledge_space(
                user_id, knowledge_space_name
            )
        )
        logger.info(f"创建知识空间{stored_knowledge_space.id}成功")
        return stored_knowledge_space

    async def create_file_and_upload_to_minio(
        self,
        file_path: str,
        knowledge_space_id: str,
        bucket_name: str,
        object_name: str,
    ) -> KnowledgeScopeMinioMapping:
        doc_title = Path(file_path).name
        stored_file: file = await self.file_service.upload_new_file_to_knowledge_space(
            knowledge_space_id=knowledge_space_id,
            doc_title=doc_title,
            doc_text=None,
            minio_bucket_name=bucket_name,
            minio_object_name=object_name,
        )
        logger.info(f"创建文件{stored_file.id}成功")
        # 这里就对应着doc_text这个字段在数据库表file中是可选的，因为业务逻辑的需求，所以这里doc_text为空
        await self.file_service.upload_new_file_to_minio(
            bucket_name=bucket_name, file_path=file_path, object_name=object_name
        )
        return KnowledgeScopeMinioMapping(
            knowledge_scope=KnowledgeScopeLocator(
                user_id=stored_file.KnowledgeSpaceFile.user_id,
                knowledge_space_id=knowledge_space_id,
                file_id=stored_file.id,
            ),
            minio_object_reference=MinioObjectReference(
                bucket_name=bucket_name, object_name=object_name
            ),
        )

    # 这个get_all的函数还需要进行优化,暂时先不管了
    async def get_all_knowledge_scope_structure(self):
        complete_knowledge_scope_structure = await self.user_knowledge_space_file_service.get_all_knowledge_scope_structure()
        return complete_knowledge_scope_structure

    async def index(
        self,
        collection_name: str,
        knowledge_scope: KnowledgeScopeLocator,
        meta_data: str | None = None,
        deep_index_pattern: bool = False,
    ):
        """index_pattern是一个很重要的概念，代表你要覆盖还是说要新增，这是一个需要区分的字段???这是存疑的。需要再讨论一下，
        不需要之前说的partition_name了
        knowledge_scope 是一个类对象，其形式为：
        user_id
        knowledge_space_id
        file_id

        meta_data 由用户自己定义啦！~可能是用户或者开发者自己想分类的领域

        """
        if knowledge_scope.file_id is None:
            raise ValueError("knowledge_scope.file_id is Needed")

        index_status = await self.file_service.get_index_status_by_file_id(
            knowledge_scope.file_id
        )
        deep_index_status = await self.file_service.get_deep_index_status_by_file_id(
            knowledge_scope.file_id
        )

        #  判断当前文件是否已经索引过了，是否已经被深度索引过了。
        # 如果你的deep_index_pattern为True，那么就代表你需要深度索引，那么就判断是否已经被深度索引过了，如果已经被深度索引过了，那么就抛出异常
        # 如果deep_index_pattern为False，那么就代表你需要普通索引，那么就判断是否已经被索引过了，如果已经被索引过了，那么就抛出异常

        if deep_index_pattern:
            if deep_index_status:
                raise Exception("当前文件已经被深度索引过了！")
            if index_status:
                logger.info(
                    "当前文件已经被普通索引过了，但是没有被深度索引过，可以复用之前的中间过程开始深度索引"
                )
            else:
                logger.info("当前文件没有深度索引过，也没有普通索引过，开始深度索引")
        else:
            if deep_index_status:
                raise Exception(
                    "当前文件已经被深度索引过了,但是没有被普通索引过，可以复用之前的中间过程开始普通索引"
                )
            if index_status:
                raise Exception("当前文件已经被普通索引过了！")
            else:
                logger.info("当前文件没有深度索引过，也没有普通索引过，开始普通索引")
        llm_total_token_usage = 0
        embedding_total_token_usage = 0
        # 通过file_id定位文件在Minio中的位置

        minio_object_reference: MinioObjectReference = (
            await self.file_service.get_minio_reference_by_id(knowledge_scope.file_id)
        )

        if not index_status and not deep_index_status:
            # 接下来判断需要做index的文件类型，如果是csv或者excel等有结构的数据，那么就要跳过数据清洗

            # 首先提取文本
            complete_text: CompleteTextUnit = await process_text(
                minio_object_reference.bucket_name, minio_object_reference.object_name
            )
            logger.info("数据提取和清洗完成")

            # 此时需要将提取干净的文本放进数据库，考虑到数据库IO的压力，这里最多只存放300个字符作为数据库的预览
            # 涉及file的数据库模型
            await self.file_service.update_existed_file_in_knowledge(
                knowledge_scope.file_id,
                {
                    "doc_text": complete_text.root[:300],
                },
            )
            logger.info("file数据模型落盘成功")
            # 然后创建workflow 落盘数据库
            index_workflow_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            created_workflow: index_workflow = (
                await self.index_workflow_service.create_workflow(
                    status="processing",
                    action="text_extract",
                    workflow_start_time=index_workflow_start_time,
                )
            )
            # 然后进行文本切分
            splitter = TextSplitter()
            if Path(minio_object_reference.object_name).suffix != ".csv":
                chunks: ChunkedTextUnit = await splitter.split_text_by_token(
                    complete_text
                )
            else:
                chunks: ChunkedTextUnit = await splitter.split_text_by_row_in_csv(
                    complete_text
                )
            token_list: TokenListByTextChunk = splitter.tokens_by_chunk
            logger.info("文本切分完成")

            # 涉及text_chunk的数据库模型
            text_chunk_id_list = await self.text_chunk_service.batch_create_text_chunk(
                doc_id=knowledge_scope.file_id,
                text_chunk_list=chunks,
                n_tokens_list=token_list,
            )
            logger.info("text_chunk数据模型落盘成功")
            # 更新workflow
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id, data={"action": "text_chunk"}
            )
            # 开始提取图结构
            graphs: BatchTextChunkGenerateGraphsResponse = (
                await batch_text_chunk_generate_graphs_process(chunks)
            )
            logger.info("子图结构提取完成")
            # 开始计算消耗的llm_tokens 后续用来累加
            llm_total_token_usage += llm_token_usage_var.get()
            logger.info(f"目前消耗的llm的token数量为{llm_total_token_usage}")

            # 更新workflow
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id, data={"action": "sub_graph_generate"}
            )
            # 开始合并每个文本分块得到的子图结构变成一张完整的图谱结构
            merged_graph: CompleteGraphData = await merge_sub_entity_relationship_graph(
                graphs
            )
            logger.info("子图结构合并完成一张完整的图")
            # 更新workflow
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id, data={"action": "merge_sub_graph"}
            )
            # 对完整的图谱结构进行普通的可视化
            graph_data_html = await store_graph_data_to_html_with_no_leiden(
                merged_graph
            )
            logger.info("对完整的图结构可视化完成")

            # 然后将可视化的html文件上传到Minio中方便查看
            await upload_file_to_minio_func(
                bucket_name=minio_object_reference.bucket_name,
                object_name=f"html_content/{str(uuid.uuid4())}_graph_data_with_no_leiden.html",
                string_data=graph_data_html.root,
            )
            logger.info("完整的图结构可视化的HTML文件上传到Minio完成")
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "action": "Generate a visualization of the complete graph structure and store it in MinIO."
                },
            )

            # 涉及merged_graph_data的数据库模型
            stored_merged_graph_data = (
                await self.merged_graph_data_service.create_merged_graph_data(
                    str(merged_graph.model_dump()), graph_data_html.root
                )
            )
            # 这里在函数调用的外面仍然加了一个括号的作用是为了隐式续行，放心，不会变成元组

            logger.info("merged_graph_data数据模型落盘完成")
            # 涉及到sub_graph_data的数据库模型
            await self.sub_graph_data_service.batch_create_sub_graph_data(
                text_chunk_id_list=text_chunk_id_list,
                sub_graph_data_list=graphs,
                merged_graph_data_id=stored_merged_graph_data.id,
            )
            logger.info("sub_graph_data数据模型落盘完成")

            # 将描述好的关系描述,以及关系描述的embedding向量以及附带的metadata嵌入到zilliz向量数据库中，目前我的metadata信息只有原文件名，考虑以后的可扩展性？现在考虑好了

        if not deep_index_pattern:
            # 如果之前做过深度索引，那么可以在这里进行普通索引的过程中可以复用之前深度索引的中间过程的结果
            if deep_index_status:
                found_file: file = (
                    await self.file_service.get_file_in_knowledge_space_by_doc_id(
                        knowledge_scope.file_id
                    )
                )
                merged_graph: str = found_file.text_chunks[
                    0
                ].sub_graph_datas.SubGraphDataMergedGraphData.graph_data
                merged_graph: CompleteGraphData = CompleteGraphData(
                    **(ast.literal_eval(merged_graph))
                )
                index_workflow_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                created_workflow = await self.index_workflow_service.create_workflow(
                    status="processing",
                    action="Retrieve the full knowledge graph structure created in the previous indexing phase.",
                    workflow_start_time=index_workflow_start_time,
                )

            # 得到完整的图谱结构以后，要对其中的关系描述进行加强
            graph_description = GraphDescriptionEnrichment()
            graph_data_with_description_enrichment: GraphDescriptionResponse = (
                await graph_description.describe_graph(merged_graph)
            )
            logger.info("对完整的图谱结构的关系描述加强完成")
            # 更新workflow
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id, data={"action": "graph_description_enrichment"}
            )
            # 先将完整的图谱结构进行平铺展开变成一个列表
            flattened_entity_relation: list[
                FlattenEntityRelation
            ] = await flatten_entity_relation_func(
                graph_data_with_description_enrichment.graph_data_with_enriched_description,
                stored_merged_graph_data.id,
            )
            logger.info("完整的图谱结构平铺展开完成，得到head_entity和tail_entity")

            # 涉及到flattend_entity_relation的数据库模型的IO
            await self.flatten_entity_relation_service.batch_create_flatten_entity_relation(
                flattened_entity_relation
            )
            logger.info("flattened_entity_relation数据模型落盘完成")

            # 利用embedding模型生成embedding向量
            embedding_vector: BatchTextChunkGenerateEmbeddingsResponse = (
                await batch_text_chunk_generate_embeddings_process(
                    graph_data_with_description_enrichment.graph_description_list
                )
            )

            logger.info("对完整的图谱结构增强过的关系描述的embedding向量生成完成")
            # 因为embedding_token_usage_var是全局变量，在上面的函数中已经运行过
            embedding_total_token_usage = embedding_token_usage_var.get()
            logger.info(
                f"目前消耗的embedding的token数量为{embedding_total_token_usage}"
            )
            # 更新workflow
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "action": "generate_embedding_vector",
                    "embedding_cost_tokens": embedding_total_token_usage,
                    "llm_cost_tokens": llm_total_token_usage,
                },
            )
            if isinstance(meta_data, str):
                meta_data_list = [
                    meta_data
                    for _ in range(
                        len(
                            graph_data_with_description_enrichment.graph_description_list
                        )
                    )
                ]
            if meta_data is None:
                meta_data_list = None
            if isinstance(knowledge_scope, KnowledgeScopeLocator):
                knowledge_scope_list = [
                    knowledge_scope
                    for _ in range(
                        len(
                            graph_data_with_description_enrichment.graph_description_list
                        )
                    )
                ]
            await data_insert_to_vector_db(
                text_list=graph_data_with_description_enrichment.graph_description_list,
                vector=embedding_vector.root,
                collection_name=collection_name,
                knowledge_scope_list=knowledge_scope_list,
                meta_data_list=meta_data_list,
            )
            logger.info("向量数据库插入完成")
            index_workflow_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            index_workflow_duration_time = str(
                datetime.strptime(index_workflow_end_time, "%Y-%m-%d %H:%M:%S")
                - datetime.strptime(index_workflow_start_time, "%Y-%m-%d %H:%M:%S")
            )
            # 文件索引完毕，也确定好了文件的索引要放在zilliz某个集群下哪个collection_name了,所以要
            await self.file_service.update_existed_file_in_knowledge(
                id=knowledge_scope.file_id,
                data={
                    "indexed": True,
                    "file_embedding_zilliz_collection_name": collection_name,
                },
            )
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "status": "success",
                    "action": "insert_to_vector_db",
                    "workflow_end_time": index_workflow_end_time,
                    "workflow_duration_time": index_workflow_duration_time,
                },
            )
        else:
            # 如果之前已经index好了，那么可以借用之前index过程中生成好的文件的merged_graph, 这块是需要被攻克的一个地方
            if index_status:
                found_file: file = (
                    await self.file_service.get_file_in_knowledge_space_by_doc_id(
                        knowledge_scope.file_id
                    )
                )
                merged_graph: str = found_file.text_chunks[
                    0
                ].sub_graph_datas.SubGraphDataMergedGraphData.graph_data
                merged_graph: CompleteGraphData = CompleteGraphData(
                    **(ast.literal_eval(merged_graph))
                )
                logger.info("从数据库中获取到之前的index过程中产生的完整的图谱结构")
                # 这里需要再重新建立一个workflow，因为之前的workflow已经结束了
                index_workflow_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                created_workflow = await self.index_workflow_service.create_workflow(
                    status="processing",
                    action="Retrieve the full knowledge graph structure created in the previous indexing phase.",
                    workflow_start_time=index_workflow_start_time,
                )

            # 如果是deep_index_pattern 那么要生成社区报告。首先做好社区划分。
            graph_data_with_community_id: GraphDataAddCommunityWithVisualization = (
                await realize_leiden_community_algorithm(merged_graph)
            )
            logger.info("对完整的图谱结构进行leiden算法community划分完成")
            # 更新workflow的状态
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "status": "Perform community detection on the complete graph structure using the Leiden algorithm"
                },
            )

            # 将带有社区标签的可视化html保存到Minio中，方便后续查看
            await upload_file_to_minio_func(
                bucket_name=minio_object_reference.bucket_name,
                object_name=f"html_content/{str(uuid.uuid4())}_graph_data_with_leiden.html",
                string_data=graph_data_with_community_id.html_content,
            )
            logger.info("整的图结构可视化的HTML文件上传到Minio完成")
            # 更新workflow状态
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "action": "Generate a visualization of the complete graph structure with community label and store it in MinIO."
                },
            )

            # 生成带有社区id的graph_data, 并对其中的关系描述进行增强
            graph_description = GraphDescriptionEnrichment()
            graph_data_with_community_id_and_description_enrichment: GraphDescriptionWithCommunityClusterResponse = await graph_description.describe_graph_with_community_cluster(
                graph_data_with_community_id.graph_data
            )
            logger.info("对带有社区划分的完整的图谱结构的关系描述加强完成")
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "action": "graph_description_enrichment_with_community_detection"
                },
            )

            # 生成带有社区id的社区报告
            community_report_with_community_id: BatchGenerateCommunityReportResponse = await batch_generate_community_report_func(
                graph_data_with_community_id_and_description_enrichment.graph_description_dict_by_community_id
            )
            logger.info(
                "对带有社区划分的完整的图谱结构增强过的关系描述的community报告生成完成"
            )
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "action": "graph_description_enrichment_with_community_detection"
                },
            )
            # 这里产生了llm_token的消耗
            llm_total_token_usage += llm_token_usage_var.get()
            logger.info(f"目前消耗的llm的token数量为{llm_total_token_usage}")
            # 这里涉及community_cluster的数据库模型
            batch_create_community_cluster_response = (
                await self.community_cluster_service.batch_create_community_cluster(
                    community_report_with_community_id
                )
            )
            logger.info("community_cluster数据模型落盘完成")

            # 这里涉及community_report的数据库模型
            batch_create_community_report_response: BatchCreateCommunityReportResponse = await self.community_report_service.batch_create_community_report(
                community_report_with_community_id
            )
            logger.info("community_report数据模型落盘完成")

            if isinstance(meta_data, str):
                meta_data = [
                    meta_data
                    for _ in range(
                        len(
                            community_report_with_community_id.community_reports_structed_data_with_community_id
                        )
                    )
                ]
            if meta_data is None:
                meta_data_list = None
            if isinstance(knowledge_scope, KnowledgeScopeLocator):
                knowledge_scope_list = [
                    knowledge_scope
                    for _ in range(
                        len(
                            community_report_with_community_id.community_reports_structed_data_with_community_id
                        )
                    )
                ]
            # 利用embedding模型生成embedding向量
            embedding_vector: BatchTextChunkGenerateEmbeddingsResponse = (
                await batch_text_chunk_generate_embeddings_process(
                    batch_create_community_report_response.community_report_list
                )
            )

            await data_insert_to_vector_db(
                text_list=batch_create_community_report_response.community_report_list,
                vector=embedding_vector.root,
                collection_name=collection_name,
                knowledge_scope_list=knowledge_scope_list,
                community_cluster_list=batch_create_community_report_response.community_id_list,
                meta_data=meta_data,
            )
            logger.info("向量数据库插入完成")
            index_workflow_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            index_workflow_duration_time = str(
                index_workflow_end_time - index_workflow_start_time
            )
            await self.file_service.update_existed_file_in_knowledge(
                id=knowledge_scope.file_id,
                data={
                    "deep_indexed": True,
                    "file_embedding_zilliz_collection_name": collection_name,
                },
            )
            await self.index_workflow_service.update_workflow(
                id=created_workflow.id,
                data={
                    "status": "success",
                    "action": "insert_to_vector_db",
                    "workflow_end_time": index_workflow_end_time,
                    "workflow_duration_time": index_workflow_duration_time,
                },
            )
        return CostTokens(
            llm_token_usage=llm_total_token_usage,
            embedding_token_usage=embedding_total_token_usage,
        )

    async def batch_index(
        self,
        collection_name: str,
        knowledge_scope: list[KnowledgeScopeLocator] | KnowledgeScopeLocator,
        meta_data: str | None = None,
        deep_index_pattern: bool = False,
    ) -> CostTokens:
        # 这个batch index的行为有三种情况，一个是对不同的file_id进行batch index,另外一个是对相同的知识库id下面的文件做batch index，第三个行为是对用户空间下不同知识库id下面的所有的file id进行index/.
        # 这个函数后期还需要改进一下，集中返回所有文件消耗的llm_token_usage和embedding_token_usage
        results = []
        if isinstance(knowledge_scope, list[KnowledgeScopeLocator]):
            if all(knowledge_scope.file_id for knowledge_scope in knowledge_scope):
                tasks = [
                    self.index(
                        collection_name=collection_name,
                        knowledge_scope=knowledge_scope,
                        meta_data=meta_data,
                        deep_index_pattern=deep_index_pattern,
                    )
                    for knowledge_scope in knowledge_scope
                ]
                results = await asyncio.gather(*tasks)
        if isinstance(knowledge_scope, KnowledgeScopeLocator):
            if knowledge_scope.knowledge_space_id and not knowledge_scope.file_id:
                found_file_list = await self.file_service.get_file_in_knowledge_space_by_knowledge_space_id(
                    knowledge_scope.knowledge_space_id
                )
                tasks = [
                    self.index(
                        collection_name=collection_name,
                        knowledge_scope=knowledge_scope.__setattr__("file_id", file.id),
                        meta_data=meta_data,
                        deep_index_pattern=deep_index_pattern,
                    )
                    for file in found_file_list
                ]
                results = await asyncio.gather(**tasks)
        llm_total_token_usage = sum([result.llm_token_usage for result in results])
        embedding_total_token_usage = sum(
            [result.embedding_token_usage for result in results]
        )
        return CostTokens(
            llm_token_usage=llm_total_token_usage,
            embedding_token_usage=embedding_total_token_usage,
        )

    async def query(
        self,
        user_prompt: str,
        knowledge_scope: KnowledgeScopeLocator,
        deep_query_pattern: bool = False,
        session_id: str | None = None,
        context: list[RoleMessage] | None = None,
        recalled_text_fragments_top_k: int = 5,
    ):
        """感觉这里的context参数是可以保留那种原始的历史记录，也可以让用户手动增加的，保留更多灵活性,
        可以用实际已经存在的session_id去调取context上下文，也可以开发者或者用户根据给定的数据结构手动构造上下文添加进来
        session_id如果是空白的，那就是新开一个会话，这个逻辑是可通的, 感觉这个collection_name 是不是也可以去除了，只要针对知识空间提问就行了，不需要再引入别的复杂度了？？"""
        """
        好像这里的deep_query_pattern好像还没开始写这部分的功能
        """

        # 首先利用输入的query对向量数据库进行有筛选的检索
        knowledge_scope_real_name: KnowledgeScopeRealName = await self.user_knowledge_space_file_service.get_knowledge_scope_real_name_by_id(
            knowledge_scope
        )
        logger.info(f"本次查询的知识范围的真实范围是{knowledge_scope_real_name}")
        # 根据知识范围knowledge_scope找到文件产生的embedding向量存放在哪个zilliz_collection中了
        collection_name = await self.file_service.get_zilliz_collection_name_by_file_id(
            knowledge_scope.file_id
        )
        index_status = await self.file_service.get_index_status_by_file_id(
            knowledge_scope.file_id
        )
        deep_index_status = await self.file_service.get_deep_index_status_by_file_id(
            knowledge_scope.file_id
        )
        if deep_query_pattern:
            if not deep_index_status:
                raise Exception(
                    message="当前文件的索引状态为False，请先对知识库进行深度索引后再进行查询",
                    code=400,
                )
        else:
            if not index_status:
                raise Exception(
                    message="当前文件的索引状态为False，请先对知识库进行索引后再进行查询",
                    code=400,
                )

        searched_text: SearchedTextResponse = await query_vector_db_by_vector(
            user_prompt,
            collection_name,
            knowledge_scope,
            recalled_text_fragments_top_k,
            deep_query_pattern,
        )
        embedding_total_token_usage = embedding_token_usage_var.get()
        logger.info(f"本次检索到的文本是{searched_text}")
        if not session_id:
            context = None
        else:
            context = await self.llm_chat_service.construct_context(session_id)
        complete_response = None
        message_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async for response in final_rag_answer_process_stream(
            user_prompt=user_prompt,
            knowledge_scope_real_name=knowledge_scope_real_name,
            recalled_text_fragments=searched_text,
            session_id=session_id,
            embedding_token_usage=embedding_total_token_usage,
            rag_pattern=deep_query_pattern,
            context=context,
        ):
            yield response
            real_response_dict = json.loads(response.split(":", 1)[1].strip())
            complete_response += real_response_dict["answer"]
        message_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_duration_time = str(
            datetime.strptime(message_end_time, "%Y-%m-%d %H:%M:%S")
            - datetime.strptime(message_start_time, "%Y-%m-%d %H:%M:%S")
        )
        llm_total_token_usage = llm_token_usage_var.get()

        await self.llm_chat_service.create_message(
            id=real_response_dict["message_id"],
            user_id=knowledge_scope.user_id,
            user_prompt=user_prompt,
            user_context=context,
            llm_answer=complete_response,
            message_start_time=message_start_time,
            message_end_time=message_end_time,
            message_duration_time=message_duration_time,
            session_id=real_response_dict["session_id"],
            llm_token_usage=llm_total_token_usage,
            embedding_token_usage=embedding_total_token_usage,
        )
        await self.rag_param_service.create_rag_param(
            grounds_for_response=real_response_dict["rag_groundings"],
            message_id=real_response_dict["message_id"],
        )

    async def query_answer_non_stream(
        self,
        user_prompt: str,
        knowledge_scope: KnowledgeScopeLocator,
        deep_query_pattern: bool = False,
        session_id: str | None = None,
        context: list[RoleMessage] | None = None,
        recalled_text_fragments_top_k: int = 5,
    ):
        """
        好像这里的deep_query_pattern好像还没开始写这部分的功能
        """
        knowledge_scope_real_name: KnowledgeScopeRealName = await self.user_knowledge_space_file_service.get_knowledge_scope_real_name_by_id(
            knowledge_scope
        )
        logger.info(f"本次查询的知识范围的真实范围是{knowledge_scope_real_name}")
        # 根据知识范围knowledge_scope找到文件产生的embedding向量存放在哪个zilliz_collection中了
        collection_name = await self.file_service.get_zilliz_collection_name_by_file_id(
            knowledge_scope.file_id
        )
        searched_text: SearchedTextResponse = await query_vector_db_by_vector(
            user_prompt,
            collection_name,
            knowledge_scope,
            recalled_text_fragments_top_k,
            deep_query_pattern,
        )

        embedding_total_token_usage = embedding_token_usage_var.get()
        logger.info(f"本次检索到的文本是{searched_text}")
        if not session_id:
            context = None
        else:
            context = await self.llm_chat_service.construct_context(session_id)

        message_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        answer = await final_rag_answer_process_not_stream(
            user_prompt=user_prompt,
            knowledge_scope_real_name=knowledge_scope_real_name,
            recalled_text_fragments_list=searched_text.root,
            session_id=session_id,
            embedding_token_usage=embedding_total_token_usage,
            deep_query_pattern=deep_query_pattern,
            context=context,
        )
        message_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_duration_time = str(
            datetime.strptime(message_end_time, "%Y-%m-%d %H:%M:%S")
            - datetime.strptime(message_start_time, "%Y-%m-%d %H:%M:%S")
        )
        llm_total_token_usage = llm_token_usage_var.get()
        await self.llm_chat_service.create_message(
            id=answer["message_id"],
            user_id=knowledge_scope.user_id,
            user_prompt=user_prompt,
            user_context=context,
            llm_answer=answer["answer"],
            message_start_time=message_start_time,
            message_end_time=message_end_time,
            message_duration_time=message_duration_time,
            session_id=answer["session_id"],
            llm_token_usage=llm_total_token_usage,
            embedding_token_usage=embedding_total_token_usage,
        )
        await self.rag_param_service.create_rag_param(
            grounds_for_response=answer["rag_groundings"],
            message_id=answer["message_id"],
        )

        return answer
