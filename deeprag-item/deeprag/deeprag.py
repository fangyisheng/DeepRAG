from deeprag.workflow.upload_file_to_minio import upload_file_to_minio_func
from deeprag.workflow.text_extract_and_clean import process_text
from deeprag.workflow.text_chunk_based_by_token import TextSplitter
from deeprag.workflow.batch_text_chunk_generate_graphs import (
    batch_text_chunk_generate_graphs_process,
)
from deeprag.workflow.batch_text_chunk_generate_embeddings import batch_text_chunk_generate_embeddings_process
from deeprag.workflow.graph_storage_to_html_with_no_leiden import (
    store_graph_data_to_html_with_no_leiden,
)
from deeprag.workflow.merge_sub_graph import merge_sub_entity_relationship_graph
from deeprag.workflow.graph_description import describe_graph
from deeprag.workflow.vector_with_text_to_vector_db import data_insert_to_vector_db
from deeprag.workflow.vector_query_to_vector_db import query_vector_db_by_vector
from deeprag.workflow.final_rag_answer import final_rag_answer_process_stream,final_rag_answer_process_not_stream
from deeprag.db.service.knowledge_space.knowledge_space_service import KnowledgeSpaceService
from deeprag.db.service.file.file_service import FileService



class DeepRAG:
    def __init__(self):
        pass
        
    async def index(self,file_path:str,collection_name:str,partition_name:str,meta_data:str |list |None = None, knowledge_space_name: str  = "temporary",deep_knowledge_graph_pattern: bool = False):
        #首先提取干净的文本
        cleaned_text = await process_text(file_path)
        # 然后进行文本切分
        splitter = TextSplitter()
        chunks = await splitter.split_text_by_token(cleaned_text)
        # 开始提取图结构
        graphs = await batch_text_chunk_generate_graphs_process(chunks)
        # 开始合并每个文本分块得到的子图结构变成一张完整的图谱结构
        merged_graph = await merge_sub_entity_relationship_graph(graphs)
        # 得到完整的图谱结构以后，要对其中的关系加以描述
        relation_description = await describe_graph(merged_graph)
        # 利用embedding模型生成embedding向量
        embedding_vector = await batch_text_chunk_generate_embeddings_process(relation_description)
        # 将描述好的关系描述,以及关系描述的embedding向量以及附带的metadata嵌入到zilliz向量数据库中，目前我的metadata信息只有原文件名，考虑以后的可扩展性？现在考虑好了
        if not deep_knowledge_graph_pattern:
            partition_name = 

            

            if isinstance(meta_data,str):
                meta_data = [meta_data for _ in range(len(embedding_vector))]
                await data_insert_to_vector_db(relation_description,embedding_vector,collection_name,partition_name,meta_data)
            if isinstance(meta_data,list):
                await data_insert_to_vector_db(relation_description,embedding_vector,collection_name,partition_name,meta_data)
    
    async def query(self,user_prompt:str,stream:bool,context:list |None = None,knowledge_space_id:str | None =None,file_id:str | None =  None):
        if knowledge_space_id is None and file_id is None:
            raise ValueError("Either knowledge_space_id or file_id must be provided.") 
        if knowledge_space_id is None and file_id is not None:


        
    







    


    async def index_and_query(self,file_path,user_prompt,context):


