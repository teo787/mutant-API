from redis.asyncio import Redis, ConnectionPool
from core.settings import settings

_pool: ConnectionPool | None = None
_redis: Redis | None = None


def get_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=20,        
            decode_responses=True,     
            socket_connect_timeout=2,  
            socket_timeout=2,
        )
    return _pool


async def get_redis() -> Redis:
    """
    Dependency inyectable en endpoints:
        redis: Redis = Depends(get_redis)
    """
    global _redis
    if _redis is None:
        _redis = Redis(connection_pool=get_pool())
    return _redis


async def close_redis():
    """Llamar al apagar la app."""
    global _redis, _pool
    if _redis:
        await _redis.aclose()
        _redis = None
    if _pool:
        await _pool.aclose()
        _pool = None