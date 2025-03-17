import redis.asyncio as redis
import uuid
import asyncio

# 创建 Redis 连接
# 假设 Redis 在本地运行，默认端口是 6379
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def increment_user_counter_lua(
    user_id, llm_cost_tokens, llm_cost_rps, embedding_cost_tokens, embedding_cost_rps
):
    redis_client = await redis.Redis(host="localhost", port=6379, decode_responses=True)
    data = {
        "llm_cost_tokens": llm_cost_tokens,
        "llm_cost_rps": llm_cost_rps,
        "embedding_cost_tokens": embedding_cost_tokens,
        "embedding_cost_rps": embedding_cost_rps,
    }
    # 定义 Lua 脚本
    lua_script = """
-- KEYS[1]: 键名
-- ARGV[1]: 键值
redis.call("SET", KEYS[1], ARGV[1])
"""

    # 使用 eval 方法执行 Lua 脚本
    new_count = await redis_client.eval(lua_script, 1, user_id, str(data))
    return new_count


print(asyncio.run(increment_user_counter_lua(f"{str(uuid.uuid4())}")))
