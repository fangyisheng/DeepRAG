import redis.asyncio as redis
import uuid
import asyncio

# 创建 Redis 连接
# 假设 Redis 在本地运行，默认端口是 6379
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def increment_user_counter_lua(
    user_id, llm_cost_tokens, llm_cost_rps, embedding_cost_tokens, embedding_cost_rps
):
    data = {
        "llm_cost_tokens": llm_cost_tokens,
        "llm_cost_rps": llm_cost_rps,
        "embedding_cost_tokens": embedding_cost_tokens,
        "embedding_cost_rps": embedding_cost_rps,
    }
    # 定义 Lua 脚本
    lua_script = """
    local key = KEYS[1]  -- 获取传入的键（用户名）
    local current_count = redis.call('GET', key)  -- 获取当前计数值
    if not current_count then
        current_count = 0  -- 如果键不存在，初始化为 0
    else
        current_count = tonumber(current_count)  -- 将字符串转换为数字
    end
    current_count = current_count + 1  -- 计数加 1
    redis.call('SET', key, current_count)  -- 更新计数值
    return current_count  -- 返回最新的计数值
    """

    # 使用 eval 方法执行 Lua 脚本
    new_count = await redis_client.eval(lua_script, 1, user_id, data)
    return new_count


print(asyncio.run(increment_user_counter_lua(f"{str(uuid.uuid4())}")))
