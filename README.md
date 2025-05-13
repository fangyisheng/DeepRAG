# DeepRAG A Fast and Efficient Retrieval-Augmented Generation (RAG) Framework for LLMs

DeepRAG is a lightweight, high-performance RAG framework designed for building advanced LLM-powered applications. It supports integration with large language models such as DeepSeek-v3 , Qwen , Llama 3 , and more — whether from cloud APIs or self-hosted backends like SGLang or vLLM .

With support for powerful vector databases like Zilliz/Milvus , efficient data parsing pipelines, and modular architecture, DeepRAG makes it easy to build, scale, and customize retrieval-augmented generation systems for real-world applications.

![9c0d2b267fb0518c63d1e634b95285c](https://github.com/user-attachments/assets/48739d37-39a9-40c4-b1d6-ad5a6870cba1)
A Fast and Efficient LLM-RAG Python project based DeepSeek-v3 or other LLM models using Poetry

Let me introduce the RAG frame developed by myself to help u process your documents

**Step 1: You should prepare the LLM model and Embedding API KEY and BASE_URL from the cloud provider or your self-hosted SGLang VLLM ....**

For example, u can get the mentioned things from Deepseek official website or  Aliyun website. 
OtherWise, if high-performnce computing device such as Nvidia or Ascend or Google TPU or Intel (these brands mentioned has no sortinhgs ) is around u ,u can self-host the LLM or Embedding Model by SGLang 
or vllm. For the further information about self-hosting , vllm and SGLang docs website is all u need. Trust me, it is easy.


**Step 2: Zilliz/Milvus vector database is required**

u can self-host the milvus vector database by docker to setup the milvus_uri and milvus_token which .env file needs
as the docker shells for standalone and distributed deploying milvus vector database are different, the shells example wont be provided in the readme. For the further information on how to self-host the milvus
vector database, the milvus docs website is your best choice.

As u always concerned,why u dont use the open-source vector database. Cuz I want to build a hight-performance RAG system and self-hosted vector database may bring u some unpredictable problems annoying.
Given the Zilliz vector database, u can go to the Zilliz domain website to register your own account. For the economics consideration, by the way ,if u just dev or learn the RAG system, just subscribe the Free
cluster in Zilliz. Free, and relative high-performance and low failure rate.


**Step 3:PG database and Minio is required**
pg database is everywhere in cloud providers.but it mays costs some money.
if u dont want to purchase cloud database,  just self-host it by docker or podman. let me just show u a case.

```bash
docker run --name my-postgres \
  -e POSTGRES_PASSWORD=mypassword \
  -v pg_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres
```
```bash
docker run -d --name minio --restart always -p 9002:9000 -p 9001:9001 -v minio_data:/data -e "MINIO_ROOT_USER=minioadmin" -e "MINIO_ROOT_PASSWORD=minioadmin" minio/minio server /data --console-address ":9001"
```

**Step4: complete writing the .env file**
``` git clone 





