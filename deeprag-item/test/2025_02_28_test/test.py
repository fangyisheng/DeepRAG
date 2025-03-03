from rank_bm25 import BM25Okapi

# 假设我们有以下文档和查询
corpus = [
    "This is the first document.",
    "This document is the fisrt document.",
    "And this is the third one.",
    "Is this the first document?",
]

query = "first document"

# 对文档进行分词
tokenized_corpus = [doc.split(" ") for doc in corpus]

# 创建BM25对象
bm25 = BM25Okapi(tokenized_corpus)

# 对查询进行分词
tokenized_query = query.split(" ")

# 计算BM25分数
doc_scores = bm25.get_scores(tokenized_query)

# 输出结果
for i, score in enumerate(doc_scores):
    print(f"Document {i+1}: {score}")