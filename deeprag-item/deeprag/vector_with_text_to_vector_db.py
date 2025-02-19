# Connect using a MilvusClient object
from pymilvus import MilvusClient
from dotenv import load_dotenv
load_dotenv()
import os
CLUSTER_ENDPOINT =  os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN=os.getenv("MILVUS_CLUSTER_TOKEN") # Set your token
# Initialize a MilvusClient instance
# Replace uri and token with your own
client = MilvusClient(
    uri=CLUSTER_ENDPOINT, # Cluster endpoint obtained from the console
    token=TOKEN # API key or a colon-separated cluster username and password
)
client.create_collection(
    collection_name = "test",
    dimension = int(os.getenv("EMBEDDING_DIMENSION"))
)

async def data_insert_to_vector_db(text_chunk,vector,meta_data):
    data = [{"id":i,"vector":vector[i],"meta_data": meta_data[i]} for i in range(text_chunk)]
    res = client.insert(
    collection_name="test",
    data=data
)
    return res
