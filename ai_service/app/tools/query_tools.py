from langchain_core.tools import tool
from typing import Dict, List, Optional
from app.utils.backend_client import BackendClient
from lunardate import LunarDate
import json

_backend = BackendClient()


# ========== 内部辅助方法（返回结构化数据，供编排代码使用） ==========

async def _get_friend_detail(name: str) -> Optional[Dict]:
    """查询朋友的详细信息，返回dict"""
    return await _backend.get_friend_by_name(name)


async def _get_friend_preferences(name: str, pref_type: Optional[str] = None) -> List[Dict]:
    """获取指定朋友的偏好记录"""
    prefs = await _backend.get_preferences_by_friend_name(name)
    if pref_type:
        prefs = [p for p in prefs if p.get("type") == pref_type]
    return prefs


async def _get_friend_notes(name: str) -> List[Dict]:
    """获取指定朋友的便签记录"""
    return await _backend.get_notes_by_friend_name(name)


async def _get_all_friends_brief() -> List[Dict]:
    """获取所有朋友的简要信息"""
    friends = await _backend.get_all_friends()
    return [
        {
            "id": f.get("id"),
            "name": f.get("name"),
            "gender": f.get("gender"),
            "birthday": f.get("birthday"),
            "birthdayType": f.get("birthdayType"),
            "occupation": f.get("occupation"),
            "hometown": f.get("hometown"),
            "remark": f.get("remark"),
        }
        for f in friends
    ]


def _add_lunar_birthday_note(friend: Dict) -> None:
    """为农历生日的朋友补充农历日期说明，防止AI误解"""
    bday = friend.get("birthday")
    btype = friend.get("birthdayType", "solar")
    if bday and btype == "lunar":
        try:
            y, m, d = map(int, bday.split("-"))
            lunar = LunarDate.fromSolarDate(y, m, d)
            lunar_month_names = ["", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
            lunar_day_names = ["", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                               "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                               "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
            friend["_birthday_note"] = (
                f"【重要】该朋友过农历生日。birthday字段({bday})是公历日期，对应的农历是"
                f"{lunar_month_names[lunar.month]}月{lunar_day_names[lunar.day]}。"
                f"计算生日时请基于农历{lunar.month}月{lunar.day}日来计算，不要直接使用birthday字段。"
            )
        except Exception:
            pass


async def _get_friend_summary_data(name: str) -> Optional[Dict]:
    """聚合查询某个朋友的全部信息"""
    friend = await _get_friend_detail(name)
    if not friend:
        return None
    _add_lunar_birthday_note(friend)
    preferences = await _get_friend_preferences(name)
    notes = await _get_friend_notes(name)
    return {"basic_info": friend, "preferences": preferences, "notes": notes}


# ========== @tool 装饰的工具函数（返回字符串，供Agent/LLM使用） ==========

@tool(description="根据姓名获取朋友的详细信息，包括生日、职业、家乡、备注等")
async def get_friend_detail(name: str) -> str:
    """查询朋友的详细信息"""
    friend = await _get_friend_detail(name)
    if not friend:
        return f"未找到名为【{name}】的朋友。"
    _add_lunar_birthday_note(friend)
    return json.dumps(friend, ensure_ascii=False, indent=2, default=str)


@tool(description="获取指定朋友的喜好记录（喜欢什么、爱好什么）")
async def get_friend_likes(name: str) -> str:
    """查询朋友的喜好/爱好"""
    prefs = await _get_friend_preferences(name, pref_type="like")
    if not prefs:
        return f"【{name}】没有喜好记录。"
    return "\n".join(
        f"- [{p.get('tag', '')}] {p.get('content', '')}" for p in prefs
    )


@tool(description="获取指定朋友的厌恶/忌讳记录（讨厌什么、有什么禁忌）")
async def get_friend_dislikes(name: str) -> str:
    """查询朋友的厌恶/忌讳"""
    prefs = await _get_friend_preferences(name, pref_type="dislike")
    if not prefs:
        return f"【{name}】没有厌恶记录。"
    return "\n".join(
        f"- [{p.get('tag', '')}] {p.get('content', '')}" for p in prefs
    )


@tool(description="获取指定朋友的便签/小事记录")
async def get_friend_notes(name: str) -> str:
    """查询朋友的便签记录"""
    notes = await _get_friend_notes(name)
    if not notes:
        return f"【{name}】没有便签记录。"
    return "\n".join(
        f"- [{n.get('noteTime', '')}] {n.get('title', '')}: {n.get('content', '')} (创建时间: {n.get('createdAt', '')})"
        for n in notes
    )


@tool(description="获取所有朋友的简要列表")
async def get_all_friends_brief() -> str:
    """获取所有朋友的简要信息"""
    friends = await _get_all_friends_brief()
    if not friends:
        return "目前没有朋友记录。"
    return "\n".join(
        f"- {f.get('name', '')} ({f.get('gender', '')}, {f.get('occupation', '')})"
        for f in friends
    )


@tool(description="获取指定朋友的完整档案总结（基础信息+喜好+厌恶+便签）")
async def get_friend_summary(name: str) -> str:
    """生成朋友的完整档案总结"""
    data = await _get_friend_summary_data(name)
    if not data:
        return f"未找到【{name}】的信息。"
    return json.dumps(data, ensure_ascii=False, indent=2)
