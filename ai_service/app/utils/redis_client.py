import redis
import json
from typing import Optional, Any

from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD


class RedisClient:
    """Redis客户端封装"""

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD or None,
            decode_responses=True
        )
        self.client = redis.Redis(connection_pool=self.pool)

    def get(self, key: str) -> Optional[str]:
        """获取值"""
        try:
            value = self.client.get(key)
            return value.decode('utf-8') if isinstance(value, bytes) else value
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def set(self, key: str, value: str, expire: int = None):
        """设置值"""
        try:
            self.client.set(key, value, ex=expire)
        except Exception as e:
            print(f"Redis set error: {e}")

    def delete(self, key: str):
        """删除键"""
        try:
            self.client.delete(key)
        except Exception as e:
            print(f"Redis delete error: {e}")

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False

    def hget(self, name: str, key: str) -> Optional[str]:
        """获取哈希字段值"""
        try:
            value = self.client.hget(name, key)
            return value.decode('utf-8') if isinstance(value, bytes) else value
        except Exception as e:
            print(f"Redis hget error: {e}")
            return None

    def hset(self, name: str, key: str, value: str):
        """设置哈希字段值"""
        try:
            self.client.hset(name, key, value)
        except Exception as e:
            print(f"Redis hset error: {e}")

    def hdel(self, name: str, key: str):
        """删除哈希字段"""
        try:
            self.client.hdel(name, key)
        except Exception as e:
            print(f"Redis hdel error: {e}")

    def hgetall(self, name: str) -> dict:
        """获取所有哈希字段"""
        try:
            result = self.client.hgetall(name)
            return {k.decode('utf-8') if isinstance(k, bytes) else k:
                    v.decode('utf-8') if isinstance(v, bytes) else v
                    for k, v in result.items()}
        except Exception as e:
            print(f"Redis hgetall error: {e}")
            return {}

    def zadd(self, name: str, mapping: dict):
        """添加有序集合成员"""
        try:
            self.client.zadd(name, mapping)
        except Exception as e:
            print(f"Redis zadd error: {e}")

    def zrangebyscore(self, name: str, min_score: float, max_score: float, withscores: bool = False):
        """按分数范围获取有序集合成员"""
        try:
            return self.client.zrangebyscore(name, min_score, max_score, withscores=withscores)
        except Exception as e:
            print(f"Redis zrangebyscore error: {e}")
            return []

    def zrem(self, name: str, *values):
        """删除有序集合成员"""
        try:
            self.client.zrem(name, *values)
        except Exception as e:
            print(f"Redis zrem error: {e}")

    def keys(self, pattern: str) -> list:
        """获取匹配的键"""
        try:
            return [k.decode('utf-8') if isinstance(k, bytes) else k
                    for k in self.client.keys(pattern)]
        except Exception as e:
            print(f"Redis keys error: {e}")
            return []
