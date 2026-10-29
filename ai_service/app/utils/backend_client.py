import httpx
from typing import List, Dict, Optional

from app.config import BACKEND_URL


class BackendClient:
    """SpringBoot 后端 API 调用客户端"""

    def __init__(self):
        self.base_url = BACKEND_URL.rstrip("/")
        self.timeout = 10.0

    async def _get(self, path: str) -> Optional[Dict]:
        """发送 GET 请求"""
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Backend GET error [{url}]: {e}")
            return None

    async def get_all_friends(self) -> List[Dict]:
        """获取所有朋友列表"""
        result = await self._get("/friends")
        return result if isinstance(result, list) else []

    async def get_friend_by_id(self, friend_id: str) -> Optional[Dict]:
        """根据 ID 获取朋友详情"""
        return await self._get(f"/friends/{friend_id}")

    async def get_friend_by_name(self, name: str) -> Optional[Dict]:
        """根据姓名查找朋友（本地模糊匹配）"""
        friends = await self.get_all_friends()
        name_lower = name.lower()
        for friend in friends:
            if name_lower in friend.get("name", "").lower():
                return friend
        return None

    async def get_friend_id_by_name(self, name: str) -> Optional[str]:
        """根据姓名获取朋友 ID"""
        friend = await self.get_friend_by_name(name)
        return friend.get("id") if friend else None

    async def get_preferences(self, friend_id: str) -> List[Dict]:
        """获取指定朋友的偏好列表"""
        result = await self._get(f"/friends/{friend_id}/preferences")
        return result if isinstance(result, list) else []

    async def get_preferences_by_friend_name(self, name: str) -> List[Dict]:
        """根据朋友姓名获取偏好列表"""
        friend_id = await self.get_friend_id_by_name(name)
        if not friend_id:
            return []
        return await self.get_preferences(friend_id)

    async def get_notes(self, friend_id: str) -> List[Dict]:
        """获取指定朋友的便签列表"""
        result = await self._get(f"/friends/{friend_id}/notes")
        return result if isinstance(result, list) else []

    async def get_notes_by_friend_name(self, name: str) -> List[Dict]:
        """根据朋友姓名获取便签列表"""
        friend_id = await self.get_friend_id_by_name(name)
        if not friend_id:
            return []
        return await self.get_notes(friend_id)

    async def get_all_notes(self) -> List[Dict]:
        """获取所有便签列表"""
        result = await self._get("/notes")
        return result if isinstance(result, list) else []

    async def get_stats(self) -> Dict:
        """获取统计数据"""
        friends_stats = await self._get("/friends/stats")
        notes_stats = await self._get("/notes/stats")
        return {
            "friends_count": friends_stats.get("count", 0) if isinstance(friends_stats, dict) else 0,
            "notes_count": notes_stats if isinstance(notes_stats, (int, float)) else 0
        }
