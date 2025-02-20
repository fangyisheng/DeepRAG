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