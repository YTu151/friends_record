import numpy as np
from typing import List, Dict, Optional
import json
import hashlib
from datetime import datetime

from app.models.qwen_client import QwenClient
from app.utils.redis_client import RedisClient
from app.config import VECTOR_DIMENSION, TOP_K_RESULTS, SIMILARITY_THRESHOLD


class VectorService:
    """向量服务 - 管理文本嵌入和相似度检索"""

    def __init__(self):
        self.qwen_client = QwenClient()
        self.redis = RedisClient()

    def _get_vector_key(self, original_id: str, data_type: str) -> str:
        """获取向量存储键"""
        return f"vector:{data_type}:{original_id}"

    def _get_content_key(self, original_id: str, data_type: str) -> str:
        """获取内容存储键"""
        return f"content:{data_type}:{original_id}"

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """计算余弦相似度"""
        a = np.array(v1)
        b = np.array(v2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    async def embed_and_store(self, original_id: str, data_type: str, content: str):
        """生成向量并存储"""
        try:
            # 获取向量嵌入
            embedding = await self.qwen_client.get_embedding(content)

            # 存储向量和内容
            vector_key = self._get_vector_key(original_id, data_type)
            content_key = self._get_content_key(original_id, data_type)

            # 序列化向量
            vector_json = json.dumps(embedding)

            # 存储到Redis
            self.redis.set(vector_key, vector_json, expire=365 * 24 * 3600)  # 1年过期
            self.redis.set(content_key, content, expire=365 * 24 * 3600)

            # 同时存储到有序集合用于检索
            index_key = f"vector_index:{data_type}"
            self.redis.hset(index_key, original_id, json.dumps({
                "original_id": original_id,
                "data_type": data_type,
                "content": content,
                "updated_at": datetime.now().isoformat()
            }))

            print(f"Vector stored: {data_type}/{original_id}")

        except Exception as e:
            print(f"Embed and store error: {e}")
            raise

    def delete_vector(self, original_id: str, data_type: str):
        """删除向量"""
        try:
            vector_key = self._get_vector_key(original_id, data_type)
            content_key = self._get_content_key(original_id, data_type)
            index_key = f"vector_index:{data_type}"

            self.redis.delete(vector_key)
            self.redis.delete(content_key)
            self.redis.hdel(index_key, original_id)

            print(f"Vector deleted: {data_type}/{original_id}")

        except Exception as e:
            print(f"Delete vector error: {e}")
            raise

    async def search(self, query: str, top_k: int = TOP_K_RESULTS) -> List[Dict]:
        """向量相似度搜索"""
        try:
            # 获取查询向量
            query_embedding = await self.qwen_client.get_embedding(query)

            # 搜索所有类型的向量
            all_results = []

            for data_type in ["friend", "preference", "note"]:
                index_key = f"vector_index:{data_type}"
                items = self.redis.hgetall(index_key)

                for original_id, item_json in items.items():
                    try:
                        # 获取该记录的向量
                        vector_key = self._get_vector_key(original_id, data_type)
                        vector_json = self.redis.get(vector_key)

                        if vector_json:
                            vector = json.loads(vector_json)
                            similarity = self._cosine_similarity(query_embedding, vector)

                            if similarity >= SIMILARITY_THRESHOLD:
                                item = json.loads(item_json)
                                all_results.append({
                                    "original_id": original_id,
                                    "data_type": data_type,
                                    "content": item.get("content", ""),
                                    "similarity": round(similarity, 4)
                                })
                    except Exception as e:
                        print(f"Search item error: {e}")
                        continue

            # 按相似度排序并返回前K个
            all_results.sort(key=lambda x: x["similarity"], reverse=True)
            return all_results[:top_k]

        except Exception as e:
            print(f"Vector search error: {e}")
            return []

    async def search_by_type(self, query: str, data_type: str, top_k: int = TOP_K_RESULTS) -> List[Dict]:
        """按类型搜索向量"""
        try:
            query_embedding = await self.qwen_client.get_embedding(query)

            index_key = f"vector_index:{data_type}"
            items = self.redis.hgetall(index_key)

            results = []
            for original_id, item_json in items.items():
                try:
                    vector_key = self._get_vector_key(original_id, data_type)
                    vector_json = self.redis.get(vector_key)

                    if vector_json:
                        vector = json.loads(vector_json)
                        similarity = self._cosine_similarity(query_embedding, vector)

                        if similarity >= SIMILARITY_THRESHOLD:
                            item = json.loads(item_json)
                            results.append({
                                "original_id": original_id,
                                "data_type": data_type,
                                "content": item.get("content", ""),
                                "similarity": round(similarity, 4)
                            })
                except Exception as e:
                    print(f"Search by type error: {e}")
                    continue

            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:top_k]

        except Exception as e:
            print(f"Search by type error: {e}")
            return []
