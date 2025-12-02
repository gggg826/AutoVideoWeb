"""
哈希计算工具
用于生成指纹哈希和唯一标识
"""
import hashlib
from typing import List, Optional


def generate_fingerprint_hash(*components: Optional[str]) -> str:
    """
    生成指纹哈希
    将多个指纹组件合并并生成唯一哈希

    Args:
        *components: 指纹组件（如 canvas、webgl、fonts 等）

    Returns:
        str: SHA-256 哈希值（64位十六进制字符串）
    """
    # 过滤掉 None 值，并转换为字符串
    valid_components = [str(c) for c in components if c is not None]

    # 如果没有有效组件，返回默认值
    if not valid_components:
        return "none"

    # 合并所有组件
    combined = "|".join(valid_components)

    # 生成 SHA-256 哈希
    return hashlib.sha256(combined.encode()).hexdigest()


def generate_visit_id(ip: str, timestamp: str, ua: str) -> str:
    """
    生成访问记录的唯一ID

    Args:
        ip: IP 地址
        timestamp: 时间戳
        ua: User-Agent

    Returns:
        str: 唯一访问 ID
    """
    combined = f"{ip}|{timestamp}|{ua}"
    return hashlib.sha256(combined.encode()).hexdigest()[:32]


def calculate_fingerprint_quality(
    canvas: Optional[str],
    webgl: Optional[str],
    fonts: Optional[str],
    screen: Optional[str],
    timezone: Optional[str],
    language: Optional[str]
) -> int:
    """
    计算指纹完整度评分（0-100）

    Args:
        canvas: Canvas 指纹
        webgl: WebGL 指纹
        fonts: 字体哈希
        screen: 屏幕分辨率
        timezone: 时区
        language: 语言

    Returns:
        int: 指纹质量分数（0-100）
    """
    score = 0

    # Canvas 指纹 (25分)
    if canvas:
        score += 25

    # WebGL 指纹 (25分)
    if webgl:
        score += 25

    # 字体哈希 (20分)
    if fonts:
        score += 20

    # 屏幕分辨率 (10分)
    if screen:
        score += 10

    # 时区 (10分)
    if timezone:
        score += 10

    # 语言 (10分)
    if language:
        score += 10

    return score
