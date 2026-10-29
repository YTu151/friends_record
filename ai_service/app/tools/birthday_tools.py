from datetime import date, datetime
from typing import Dict, List, Optional
from lunardate import LunarDate
from langchain_core.tools import tool
import json


def _get_zodiac(month: int, day: int) -> str:
    """根据公历月日计算星座"""
    zodiac_dates = [
        ("摩羯座", (1, 1), (1, 19)),
        ("水瓶座", (1, 20), (2, 18)),
        ("双鱼座", (2, 19), (3, 20)),
        ("白羊座", (3, 21), (4, 19)),
        ("金牛座", (4, 20), (5, 20)),
        ("双子座", (5, 21), (6, 21)),
        ("巨蟹座", (6, 22), (7, 22)),
        ("狮子座", (7, 23), (8, 22)),
        ("处女座", (8, 23), (9, 22)),
        ("天秤座", (9, 23), (10, 23)),
        ("天蝎座", (10, 24), (11, 22)),
        ("射手座", (11, 23), (12, 21)),
        ("摩羯座", (12, 22), (12, 31)),
    ]
    for zodiac, start, end in zodiac_dates:
        if start <= (month, day) <= end:
            return zodiac
    return "未知"


def _parse_date(date_str: str) -> date:
    """解析日期字符串"""
    year, month, day = map(int, date_str.split("-"))
    return date(year, month, day)


def get_next_solar_birthday(birth_date: date) -> date:
    """计算阳历下次生日对应的日期"""
    today = date.today()
    next_birthday = birth_date.replace(year=today.year)
    if next_birthday < today:
        next_birthday = birth_date.replace(year=today.year + 1)
    return next_birthday


def get_this_year_lunar_birthday(lunar_month: int, lunar_day: int) -> Optional[date]:
    """计算今年农历生日对应的公历日期"""
    today = date.today()
    today_lunar = LunarDate.fromSolarDate(today.year, today.month, today.day)
    current_lunar_year = today_lunar.year
    try:
        return LunarDate(current_lunar_year, lunar_month, lunar_day).toSolarDate()
    except ValueError:
        return None


def get_next_lunar_birthday(lunar_month: int, lunar_day: int) -> Optional[date]:
    """计算下一个即将到来的农历生日对应的公历日期"""
    today = date.today()
    today_lunar = LunarDate.fromSolarDate(today.year, today.month, today.day)
    current_lunar_year = today_lunar.year

    candidates = []
    for lunar_year in [current_lunar_year, current_lunar_year + 1]:
        try:
            solar = LunarDate(lunar_year, lunar_month, lunar_day).toSolarDate()
            if solar >= today:
                candidates.append(solar)
        except ValueError:
            continue

    return min(candidates) if candidates else None


def calculate_solar_birthday_info(birth_date_str: str) -> Dict:
    """计算阳历生日的相关信息"""
    birth_date = _parse_date(birth_date_str)
    today = date.today()

    zodiac = _get_zodiac(birth_date.month, birth_date.day)

    age = today.year - birth_date.year
    next_birthday = get_next_solar_birthday(birth_date)
    if today < birth_date.replace(year=today.year):
        age -= 1

    days_until = (next_birthday - today).days

    return {
        "zodiac": zodiac,
        "age": age,
        "next_birthday": next_birthday.strftime("%Y-%m-%d"),
        "days_until": days_until,
    }


def calculate_lunar_birthday_info(solar_date_str: str) -> Dict:
    """计算农历生日信息：birth_date_str是存储的公历日期，先转为农历再计算"""
    solar_year, solar_month, solar_day = map(int, solar_date_str.split("-"))

    # 1. 将存储的公历生日转为农历，获取农历月日
    lunar_date = LunarDate.fromSolarDate(solar_year, solar_month, solar_day)
    lunar_month = lunar_date.month
    lunar_day = lunar_date.day

    # 2. 星座从公历计算
    zodiac = _get_zodiac(solar_month, solar_day)

    # 3. 计算农历月日中文字符串
    lunar_month_names = ["", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    lunar_day_names = ["", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                       "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                       "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

    # 4. 计算年龄
    today = date.today()
    this_year_lunar_solar = get_this_year_lunar_birthday(lunar_month, lunar_day)

    age = today.year - solar_year
    if this_year_lunar_solar and today < this_year_lunar_solar:
        age -= 1

    # 5. 计算下次生日
    next_birthday = get_next_lunar_birthday(lunar_month, lunar_day)
    days_until = (next_birthday - today).days if next_birthday else None

    return {
        "solar_birthday": f"{solar_year}-{solar_month:02d}-{solar_day:02d}",
        "lunar_birthday": f"{lunar_month_names[lunar_month]}月{lunar_day_names[lunar_day]}",
        "zodiac": zodiac,
        "age": age,
        "next_birthday": next_birthday.strftime("%Y-%m-%d") if next_birthday else None,
        "days_until": days_until,
    }


def calculate_birthday_info(birth_date_str: str, birthday_type: str = "solar") -> Dict:
    """统一入口：根据生日类型计算相关信息"""
    if birthday_type.lower() == "lunar":
        return calculate_lunar_birthday_info(birth_date_str)
    return calculate_solar_birthday_info(birth_date_str)


def get_upcoming_birthdays(friends_data: List[Dict]) -> List[Dict]:
    """计算所有朋友的近期生日，按距离天数升序排列"""
    today = date.today()
    results = []

    for friend in friends_data:
        name = friend.get("name", "未知")
        birthday_str = friend.get("birthday")
        btype = friend.get("birthdayType", "solar")

        if not birthday_str:
            continue

        try:
            info = calculate_birthday_info(birthday_str, btype)
            days_until = info.get("days_until")
            if days_until is None:
                continue

            results.append({
                "name": name,
                "birthday_type": btype,
                "original_birthday": birthday_str,
                "next_birthday": info.get("next_birthday"),
                "days_until": days_until,
                "age": info.get("age"),
                "zodiac": info.get("zodiac"),
            })
        except Exception as e:
            print(f"Calculate upcoming birthday error for {name}: {e}")
            continue

    results.sort(key=lambda x: x["days_until"])
    return results


@tool(description="计算指定生日的年龄、星座、距离下次生日天数等信息")
def get_birthday_info(birth_date_str: str, birthday_type: str = "solar") -> str:
    """计算生日相关信息：年龄、星座、下次生日等"""
    info = calculate_birthday_info(birth_date_str, birthday_type)
    return json.dumps(info, ensure_ascii=False, indent=2)


@tool(description="获取当前日期和时间，用于计算天数差、判断生日是否已过等时间相关计算")
def get_current_time() -> str:
    """获取当前日期和时间"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
