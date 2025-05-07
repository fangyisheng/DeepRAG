"""这里是DeepRAG的sdk对应的api集成，方便集成到生产环境。实现的功能有问答查询的流式输出，查找已经存在的知识空间，根据text_chunk的id去定位text_chunk的原文等操作，等我慢慢补充这部分内容"""

from fastapi import FastAPI
from deeprag.api.about_answer.about_answer_app import chat_router
from deeprag.api.about_file.about_file_app import file_router
from deeprag.api.about_knowledge_space.about_knowledge_space_app import (
    knowledge_space_router,
)
from deeprag.api.about_merged_graph_data.about_merged_graph_data_app import (
    merged_graph_data_router,
)
from deeprag.api.about_sub_graph_data.about_sub_graph_data_app import (
    sub_graph_data_router,
)
from deeprag.api.about_text_chunk.about_text_chunk_app import text_chunk_router
from deeprag.api.about_user.about_user_app import user_router
from deeprag.api.about_workflow.about_workflow_app import workflow_router
from deeprag.api.about_index.about_index_app import index_router
from deeprag.api.about_batch_index.about_batch_index_app import (
    batch_index_router,
)

app = FastAPI()


app.include_router(chat_router, prefix="/chat")
app.include_router(file_router, prefix="/file")
app.include_router(knowledge_space_router, prefix="/knowledge_space")
app.include_router(merged_graph_data_router, prefix="/merged_graph_data")
app.include_router(sub_graph_data_router, prefix="/sub_graph_data")
app.include_router(text_chunk_router, prefix="/text_chunk")
app.include_router(user_router, prefix="/user")
app.include_router(workflow_router, prefix="/workflow")
app.include_router(batch_index_router, prefix="/batch_index")
app.include_router(index_router, prefix="/index")
