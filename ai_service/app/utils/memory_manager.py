import json
from typing import List, Dict
from datetime import datetime

from app.utils.redis_client import RedisClient


class MemoryManager:
    """对话历史记忆管理"""

    def __init__(self):
        self.redis = RedisClient()
        self.max_history = 20  # 最大保留20轮对话

    def get_session_key(self, session_id: str) -> str:
        return f"session:{session_id}:history"

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """获取对话历史"""
        try:
            key = self.get_session_key(session_id)
            data = self.redis.get(key)
            if data:
                return json.loads(data)
            return []
        except Exception as e:
            print(f"Get history error: {e}")
            return []

    def add_to_history(self, session_id: str, role: str, content: str):
        """添加消息到历史"""
        try:
            history = self.get_history(session_id)
            history.append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })

            # 限制历史长度
            if len(history) > self.max_history * 2:
                history = history[-self.max_history * 2:]

            key = self.get_session_key(session_id)
            self.redis.set(key, json.dumps(history), expire=3600 * 24 * 7)  # 保留7天

        except Exception as e:
            print(f"Add history error: {e}")

    def clear_history(self, session_id: str):
        """清除对话历史"""
        try:
            key = self.get_session_key(session_id)
            self.redis.delete(key)
        except Exception as e:
            print(f"Clear history error: {e}")

    def get_formatted_history(self, session_id: str, max_turns: int = 10) -> str:
        """获取格式化的历史对话（用于提示词）"""
        history = self.get_history(session_id)
        if not history:
            return ""

        formatted = []
        recent = history[-max_turns * 2:]  # 只取最近的几轮

        for msg in recent:
            role = "用户" if msg["role"] == "user" else "助手"
            formatted.append(f"{role}: {msg['content']}")

        return "\n".join(formatted)
