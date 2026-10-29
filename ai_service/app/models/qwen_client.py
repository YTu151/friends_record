import os
from typing import List, Dict
import json

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.config import QWEN_API_KEY, CHAT_MODEL, EMBEDDING_MODEL
from app.utils.redis_client import RedisClient

# 设置DashScope API密钥（ChatTongyi/DashScopeEmbeddings通过此环境变量读取）
os.environ["DASHSCOPE_API_KEY"] = QWEN_API_KEY


class QwenClient:
    """通义千问API客户端 - 使用LangChain社区包（ChatTongyi + DashScopeEmbeddings）"""

    def __init__(self):
        self.redis_client = RedisClient()

        # 初始化聊天模型
        self.llm = ChatTongyi(
            model=CHAT_MODEL,
            temperature=0.7,
            max_tokens=2000,
        )

        # 初始化嵌入模型
        self.embeddings_model = DashScopeEmbeddings(model=EMBEDDING_MODEL)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """调用聊天模型"""
        try:
            langchain_messages = []
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))

            self.llm.temperature = temperature
            self.llm.max_tokens = max_tokens

            response = await self.llm.ainvoke(langchain_messages)
            return response.content

        except Exception as e:
            print(f"Chat completion error: {e}")
            return "AI服务暂时不可用，请稍后重试。"

    async def get_embedding(self, text: str) -> List[float]:
        """获取文本向量嵌入"""
        try:
            cache_key = f"embedding:{hash(text)}"
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            embedding = await self.embeddings_model.aembed_query(text)

            self.redis_client.set(cache_key, json.dumps(embedding), expire=86400)
            return embedding

        except Exception as e:
            print(f"Embedding error: {e}")
            return [0.0] * 1536
