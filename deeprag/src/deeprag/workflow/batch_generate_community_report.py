from deeprag.agent.index.generate_community_report import (
    generate_community_report_agent,
)
import asyncio
from deeprag.workflow.data_model import (
    BatchGenerateCommunityReportResponse,
)
from tqdm.asyncio import tqdm_asyncio
from deeprag.rag_core_utils.utils.context_holder import (
    llm_token_usage_var,
)
from loguru import logger


async def batch_generate_community_report_func(
    graph_description_list_with_community_id: dict[str, str],
) -> BatchGenerateCommunityReportResponse:
    """这个函数是用来批量生成社区检测报告的

    Args:
        graph_description_list_with_community_id (dict): _description_

    Returns:
        dict[str, list]: _description_
    """
    tasks = []
    for (
        community_id,
        graph_description_list,
    ) in graph_description_list_with_community_id.items():
        task = asyncio.create_task(
            generate_community_report_agent(graph_description_list)
        )
        tasks.append((community_id, task))
    # result = await asyncio.gather(*(task for _, task in tasks))
    results = []
    total_llm_tokens_usage = 0
    for future in tqdm_asyncio(
        asyncio.as_completed([task for _, task in tasks]),
        total=len(tasks),
        desc="批量生成划分好的社区的社区报告",
    ):
        result = await future
        results.append(result)
        total_llm_tokens_usage += result.cost_tokens
        logger.info(f"当前社区报告消耗的token: {result.cost_tokens}")
    logger.info(f"总的LLM tokens使用量: {total_llm_tokens_usage}")

    llm_token_usage_var.set(total_llm_tokens_usage)

    community_reports_with_community_id = {
        community_id: report.community_report
        for (community_id, _), report in zip(tasks, results)
    }
    community_reports_structed_data_with_community_id = {
        community_id: report.community_report_structed_data
        for (community_id, _), report in zip(tasks, results)
    }

    return BatchGenerateCommunityReportResponse(
        community_reports_with_community_id=community_reports_with_community_id,
        community_reports_structed_data_with_community_id=community_reports_structed_data_with_community_id,
    )


# # 编写测试代码 测试通过

# test_data = {
#     "610e61ad-5ed5-4514-8a8b-6158d8356cbf": [
#         "深度求索（DeepSeek）和全球 AI 领域的关系是深度求索（DeepSeek）在领域中崭露头角全球 AI 领域,深度求索（DeepSeek）在全球 AI 领域成为众人瞩目的焦点。",
#         "深度求索（DeepSeek）和2023 年的关系是深度求索（DeepSeek）成立于2023 年,深度求索（DeepSeek）成立于2023年。",
#         "深度求索（DeepSeek）和美股市场的关系是深度求索（DeepSeek）影响力体现在美股市场,深度求索（DeepSeek）的影响力在美股市场有明显体现。",
#         "深度求索（DeepSeek）和美股 AI、芯片股的关系是深度求索（DeepSeek）被认为是重要因素美股 AI、芯片股,深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
#     ],
#     "23bd6c9d-b01e-4822-9d51-74733e60d6b1": [
#         "1 月 27 日和美股 AI、芯片股的关系是1 月 27 日导致重挫美股 AI、芯片股,1月27日，美股AI、芯片股重挫。",
#         "美股 AI、芯片股和英伟达的关系是美股 AI、芯片股影响公司股价英伟达,英伟达收盘大跌超过17%，单日市值蒸发5890亿美元。",
#         "英伟达和美国股市的关系是英伟达创历史纪录美国股市,创下美国股市历史上最高纪录。",
#         "深度求索（DeepSeek）和美股 AI、芯片股的关系是深度求索（DeepSeek）被认为是重要因素美股 AI、芯片股,深度求索（DeepSeek）被认为是美股AI、芯片股波动的重要因素之一。",
#     ],
# }


# async def main():
#     await batch_generate_community_report_func(test_data)
#     print(llm_token_usage_var.get())


# asyncio.run(main())
