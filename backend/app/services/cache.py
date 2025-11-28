"""Сервис кэширования Redis."""
import redis
import json
from typing import Optional, Any
from app.core.config import settings
from functools import wraps


class CacheService:
    """Сервис кэширования."""

    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

    def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша."""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Установка значения в кэш."""
        return self.redis_client.setex(key, ttl, json.dumps(value))

    def delete(self, key: str) -> bool:
        """Удаление ключа из кэша."""
        return bool(self.redis_client.delete(key))

    def delete_pattern(self, pattern: str) -> int:
        """Удаление ключей по паттерну."""
        keys = self.redis_client.keys(pattern)
        if keys:
            return self.redis_client.delete(*keys)
        return 0

    def invalidate_timetable_cache(self):
        """Инвалидация кэша расписания."""
        self.delete_pattern("timetable:*")
        self.delete_pattern("calendar:*")


# Глобальный экземпляр
cache_service = CacheService()


def cache_result(key_prefix: str, ttl: int = 3600):
    """Декоратор для кэширования результатов функции."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ кэша из аргументов
            cache_key = f"{key_prefix}:{hash(str(args) + str(kwargs))}"
            cached = cache_service.get(cache_key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator

