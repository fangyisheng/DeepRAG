from deeprag.rag_core_utils.llm_api.llm_api_client import llm_service
from importlib import resources
import asyncio
from loguru import logger

with resources.files("deeprag.prompts.fixed_prompts").joinpath("semantic_enrichment_prompt.txt").open("r") as file:
    system_prompt = file.read()

async def semantic_enrichment_agent(user_prompt):
    response = await llm_service(system_prompt = system_prompt,user_prompt = user_prompt)
    logger.info(f"这是语义丰富后提取的关系:{response}")
    logger.info(f"这是语义丰富后提取的关系结合关系描述的语句：{response}\n{user_prompt}")
    return response + user_prompt

# asyncio.run(semantic_enrichment_agent("Satya Nadella和Microsoft的关系是Satya NadellaCEO ofMicrosoft"))

