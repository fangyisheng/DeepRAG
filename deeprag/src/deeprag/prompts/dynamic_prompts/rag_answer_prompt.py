"""这里在构建RAG回答的上下文，需要考虑的因素有很多。
需要做好RAG的强溯源工作，比如被搜索的文件，被搜索的知识空间，或者说是全局知识空间，还有被搜到的文本片段等。
一般来说被搜索到的都是稠密的文本片段，请问怎么还原到稀疏的原始文本位置呢？"""

from deeprag.workflow.data_model import KnowledgeScopeRealName, SystemPrompt


def rag_answer_prompt_content(
    knowledge_scope_real_name: KnowledgeScopeRealName, recalled_text_fragments: str
) -> SystemPrompt:
    """
    这是RAG回答的系统提示词
    """
    user_name = knowledge_scope_real_name.user_name
    knowledge_space_name = knowledge_scope_real_name.knowledge_space_name
    file_name = knowledge_scope_real_name.file_name
    if user_name and knowledge_space_name and file_name:
        return f"""角色 ：你是一个强大的人工智能助手，能够基于给定的知识库片段回答用户问题。
    知识范围：
    用户空间：{user_name}
    知识库空间：{knowledge_space_name}
    检索的文件名：{file_name}
    检索到的文本片段：{recalled_text_fragments}

    任务：仔细分析检索到的内容，并根据知识库信息准确回答用户问题。"""
    if user_name and knowledge_space_name and not file_name:
        return f"""角色 ：你是一个强大的人工智能助手，能够基于给定的知识库片段回答用户问题。
    知识范围：
    用户空间：{user_name}
    知识库空间：{knowledge_space_name}
    检索到的文本片段：{recalled_text_fragments}

    任务：仔细分析检索到的内容，并根据知识库信息准确回答用户问题。"""

    if user_name and not knowledge_space_name and not file_name:
        return f"""角色 ：你是一个强大的人工智能助手，能够基于给定的知识库片段回答用户问题。
    知识范围：
    用户空间：{user_name}
    检索到的文本片段：{recalled_text_fragments}
    任务：仔细分析检索到的内容，并根据知识库信息准确回答用户问题。"""
