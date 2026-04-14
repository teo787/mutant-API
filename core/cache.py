import json
import hashlib
import functools
from typing import Any, Callable

from fastapi import Depends
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from core.redis import get_redis


class CacheService:
    """
    Operaciones de cache de bajo nivel.
    Inyectable como dependency o usable directamente en servicios.
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Any | None:
        """Devuelve el valor deserializado o None si no existe."""
        raw = await self.redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Guarda el valor serializado con TTL en segundos."""
        await self.redis.setex(key, ttl, json.dumps(value, default=str))

    async def delete(self, key: str) -> None:
        """Invalida una entrada de cache."""
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str) -> int:
        """
        Borra todas las keys que coincidan con el patrón.
        Ej: delete_pattern("users:*") borra todo el cache de usuarios.

        CUIDADO: SCAN es O(N) sobre todas las keys. En Redis grandes
        usar con moderación o usar namespaces con Redis HASH.
        """
        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0

    async def get_or_set(
        self,
        key: str,
        fetch_fn: Callable,
        ttl: int = 300,
    ) -> Any:
        """
        Patrón cache-aside:
          1. Intenta leer de Redis.
          2. Si no existe, llama a fetch_fn() para obtener el dato.
          3. Guarda el resultado en Redis.
          4. Devuelve el dato.

        Uso:
            data = await cache.get_or_set(
                key="users:list",
                fetch_fn=lambda: db.query(User).all(),
                ttl=60,
            )
        """
        cached = await self.get(key)
        if cached is not None:
            return cached

        fresh = await fetch_fn() if callable(fetch_fn) else fetch_fn
        await self.set(key, fresh, ttl)
        return fresh


async def get_cache(redis: Redis = Depends(get_redis)) -> CacheService:
    """Dependency inyectable para usar CacheService en endpoints."""
    return CacheService(redis)


def cache_response(ttl: int = 300, key_prefix: str = ""):
    """
    Decorador para cachear respuestas completas de endpoints GET.

    Construye la cache key a partir del prefijo + los parámetros
    de la request (path params + query params), de forma que
    /users/1 y /users/2 tienen keys distintas.

    Uso:
        @router.get("/products")
        @cache_response(ttl=120, key_prefix="products")
        async def list_products(category: str = None):
            ...

    NO usar para:
        - Endpoints que devuelven datos personalizados por usuario
        - Endpoints POST/PUT/DELETE
        - Datos sensibles
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extraer redis de los kwargs (inyectado por FastAPI)
            redis_instance: Redis | None = None
            for v in kwargs.values():
                if isinstance(v, Redis):
                    redis_instance = v
                    break

            if redis_instance:
                # Construir key única para esta combinación de parámetros
                param_hash = hashlib.md5(
                    json.dumps(
                        {k: str(v) for k, v in kwargs.items()
                         if not isinstance(v, Redis)},
                        sort_keys=True,
                    ).encode()
                ).hexdigest()[:8]
                cache_key = f"resp:{key_prefix}:{param_hash}"

                raw = await redis_instance.get(cache_key)
                if raw:
                    return JSONResponse(
                        content=json.loads(raw),
                        headers={"X-Cache": "HIT"},
                    )

                result = await func(*args, **kwargs)

                # Guardar solo si el resultado es serializable
                if hasattr(result, "model_dump"):
                    data = result.model_dump()
                elif isinstance(result, (dict, list)):
                    data = result
                else:
                    return result

                await redis_instance.setex(
                    cache_key, ttl, json.dumps(data, default=str)
                )
                return JSONResponse(
                    content=data,
                    headers={"X-Cache": "MISS"},
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator