# Connect using a MilvusClient object
from pymilvus import MilvusClient, DataType, Function, FunctionType
from dotenv import load_dotenv
load_dotenv()
import os
CLUSTER_ENDPOINT =  os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN=os.getenv("MILVUS_CLUSTER_TOKEN") # Set your token
# Initialize a MilvusClient instance
# Replace uri and token with your own

async def create_hybrid_search_milvus_client_collection(collection_name: str | None = None):

    client = MilvusClient(
        uri=CLUSTER_ENDPOINT, # Cluster endpoint obtained from the console
        token=TOKEN # API key or a colon-separated cluster username and password
    )

    # Create schema
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )
    # Add fields to schema
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=20000)
    schema.add_field(field_name="sparse", datatype=DataType.SPARSE_FLOAT_VECTOR)
    schema.add_field(field_name="dense", datatype=DataType.FLOAT_VECTOR, dim=1024)
    bm25_function = Function(
        name="text_bm25_emb",
        input_field_names="text", # 包含原始文本数据的 VARCHAR 字段名称
        output_field_names="sparse", # 存储生成的向量的 SPARSE_FLOAT_VECTOR 字段名称
        function_type=FunctionType.BM25,
    )

    schema.add_function(bm25_function)

    index_params = MilvusClient.prepare_index_params()

    index_params.add_index(
        field_name="sparse",
        index_type="AUTOINDEX", 
        metric_type="BM25"
    )
    index_params.add_index(
    field_name="dense", #指定需要创建索引的字段名称
    index_name="dense_index", #为该索引创建一个名字
    index_type="IVF_FLAT", #指定索引的类型
    metric_type="IP",
    params={"nlist": 128}, #index索引的超参数配置，表示向量空间中的聚类
)   
    
    if collection_name:
        if not client.has_collection(collection_name = collection_name):
            client.create_collection(
                collection_name="test", 
                schema=schema, 
                index_params=index_params
            )
        return client
    else:
        return client
    