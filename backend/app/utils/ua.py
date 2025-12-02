"""
User-Agent 解析工具
"""
from user_agents import parse
from typing import Dict


def parse_user_agent(ua_string: str) -> Dict[str, any]:
    """
    解析 User-Agent 字符串，提取设备和浏览器信息

    Args:
        ua_string: User-Agent 字符串

    Returns:
        dict: 包含设备类型、浏览器、操作系统等信息的字典
    """
    ua = parse(ua_string)

    # 判断设备类型
    if ua.is_mobile:
        device_type = "mobile"
    elif ua.is_tablet:
        device_type = "tablet"
    elif ua.is_bot:
        device_type = "bot"
    else:
        device_type = "pc"

    return {
        "device_type": device_type,
        "browser": ua.browser.family,
        "browser_version": ua.browser.version_string,
        "os": ua.os.family,
        "os_version": ua.os.version_string,
        "is_bot": ua.is_bot,
        "is_mobile": ua.is_mobile,
        "is_tablet": ua.is_tablet,
        "is_pc": ua.is_pc,
    }


def is_bot_ua(ua_string: str) -> bool:
    """
    快速检查 User-Agent 是否为机器人

    Args:
        ua_string: User-Agent 字符串

    Returns:
        bool: 是否为机器人
    """
    if not ua_string:
        return True

    ua = parse(ua_string)
    return ua.is_bot


def get_device_type(ua_string: str) -> str:
    """
    仅获取设备类型

    Args:
        ua_string: User-Agent 字符串

    Returns:
        str: 设备类型 (pc/mobile/tablet/bot)
    """
    ua = parse(ua_string)

    if ua.is_bot:
        return "bot"
    elif ua.is_mobile:
        return "mobile"
    elif ua.is_tablet:
        return "tablet"
    else:
        return "pc"
