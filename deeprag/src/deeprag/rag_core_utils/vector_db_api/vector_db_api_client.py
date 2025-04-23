# Connect using a MilvusClient object
from pymilvus import MilvusClient, DataType, Function, FunctionType
from dotenv import load_dotenv
import os

import os

load_dotenv()


CLUSTER_ENDPOINT = os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN = os.getenv("MILVUS_CLUSTER_TOKEN")  # Set your token
# Initialize a MilvusClient instance
# Replace uri and token with your own


async def create_or_use_hybrid_search_milvus_client_collection(
    collection_name: str | None = None,
) -> "MilvusClient":
    client = MilvusClient(
        uri=CLUSTER_ENDPOINT,  # Cluster endpoint obtained from the console
        token=TOKEN,  # API key or a colon-separated cluster username and password
    )

    # Create schema
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=True)
    # Add fields to schema
    schema.add_field(
        field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True
    )
    schema.add_field(
        field_name="text",
        datatype=DataType.VARCHAR,
        max_length=20000,
        enable_analyzer=True,
    )
    schema.add_field(
        field_name="meta_data", datatype=DataType.JSON
    )  # 这是使用DeepRAG的用户和开发者添加的元数据信息
    schema.add_field(
        field_name="community_id", max_length=1000, datatype=DataType.VARCHAR
    )
    schema.add_field(field_name="knowledge_scope", datatype=DataType.JSON)

    schema.add_field(field_name="sparse", datatype=DataType.SPARSE_FLOAT_VECTOR)
    schema.add_field(field_name="dense", datatype=DataType.FLOAT_VECTOR, dim=1024)
    bm25_function = Function(
        name="text_bm25_emb",
        input_field_names="text",  # 包含原始文本数据的 VARCHAR 字段名称
        output_field_names="sparse",  # 存储生成的向量的 SPARSE_FLOAT_VECTOR 字段名称
        function_type=FunctionType.BM25,
    )

    schema.add_function(bm25_function)

    index_params = MilvusClient.prepare_index_params()

    index_params.add_index(
        field_name="sparse", index_type="SPARSE_INVERTED_INDEX", metric_type="BM25"
    )
    index_params.add_index(
        field_name="dense",  # 指定需要创建索引的字段名称
        index_name="dense_index",  # 为该索引创建一个名字
        index_type="IVF_FLAT",  # 指定索引的类型
        metric_type="IP",
        params={"nlist": 128},  # index索引的超参数配置，表示向量空间中的聚类
    )
    # 首先判断这个输入的参数collection_name存不存在
    # 如果输入的参数存在，那么继续判断这个collection_name在不在zilliz的集群中
    if not client.has_collection(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            schema=schema,
            index_params=index_params,
        )

    # # 检查并创建分区
    # if not client.has_partition(
    #     collection_name=collection_name, partition_name=partition_name
    # ):
    #     client.create_partition(
    #         collection_name=collection_name, partition_name=partition_name
    #     )

    return client
