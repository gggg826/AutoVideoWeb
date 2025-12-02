"""
IP 地址处理工具
"""
from fastapi import Request


def get_client_ip(request: Request) -> str:
    """
    获取客户端真实 IP 地址
    优先检查代理头部，然后使用直接连接 IP

    Args:
        request: FastAPI Request 对象

    Returns:
        str: 客户端 IP 地址
    """
    # 检查 X-Forwarded-For 头（代理/负载均衡器）
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # 取第一个 IP（原始客户端 IP）
        return forwarded_for.split(",")[0].strip()

    # 检查 X-Real-IP 头（Nginx 代理）
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    # 使用直接连接的 IP
    if request.client:
        return request.client.host

    return "unknown"


def is_private_ip(ip: str) -> bool:
    """
    检查是否为私有 IP 地址

    Args:
        ip: IP 地址字符串

    Returns:
        bool: 是否为私有 IP
    """
    if ip == "unknown":
        return False

    # 简单的私有 IP 检测
    private_ranges = [
        "10.",
        "172.16.", "172.17.", "172.18.", "172.19.",
        "172.20.", "172.21.", "172.22.", "172.23.",
        "172.24.", "172.25.", "172.26.", "172.27.",
        "172.28.", "172.29.", "172.30.", "172.31.",
        "192.168.",
        "127.",
        "localhost"
    ]

    for private_range in private_ranges:
        if ip.startswith(private_range):
            return True

    return False
