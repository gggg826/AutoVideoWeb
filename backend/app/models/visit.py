"""
访问记录数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, Index
from sqlalchemy.sql import func
from app.core.database import Base


class Visit(Base):
    """访问记录表"""

    __tablename__ = "visits"

    # 主键和唯一标识
    id = Column(Integer, primary_key=True, index=True, comment="自增主键")
    visit_id = Column(String(64), unique=True, nullable=False, index=True, comment="访问唯一ID")

    # 时间信息
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
        comment="访问时间戳"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="记录创建时间"
    )

    # IP 信息
    ip_address = Column(String(45), nullable=False, index=True, comment="IP 地址")
    ip_country = Column(String(2), index=True, comment="国家代码")
    ip_city = Column(String(100), index=True, comment="城市")
    is_proxy = Column(Boolean, default=False, comment="是否代理IP")

    # 请求信息
    user_agent = Column(Text, comment="User-Agent")
    referrer = Column(Text, comment="来源页面")
    page_url = Column(String(500), nullable=False, comment="访问页面 URL")

    # 设备信息（从 User-Agent 解析）
    device_type = Column(String(20), index=True, comment="设备类型: pc/mobile/tablet")
    browser = Column(String(50), comment="浏览器名称")
    browser_version = Column(String(20), comment="浏览器版本")
    os = Column(String(50), comment="操作系统")
    os_version = Column(String(20), comment="操作系统版本")

    # 浏览器指纹
    screen_resolution = Column(String(20), comment="屏幕分辨率")
    timezone = Column(String(50), comment="时区")
    language = Column(String(10), comment="语言")
    platform = Column(String(50), comment="平台")
    canvas_fingerprint = Column(String(64), comment="Canvas 指纹")
    webgl_fingerprint = Column(String(64), comment="WebGL 指纹")
    fonts_hash = Column(String(64), comment="字体列表哈希")

    # 浏览器地理位置（用户授权后获取）
    browser_latitude = Column(Float, comment="浏览器纬度")
    browser_longitude = Column(Float, comment="浏览器经度")
    browser_accuracy = Column(Float, comment="浏览器位置精度（米）")
    browser_altitude = Column(Float, comment="浏览器海拔高度")
    browser_altitude_accuracy = Column(Float, comment="浏览器海拔精度")

    # 行为数据
    stay_duration = Column(Integer, default=0, comment="停留时间（秒）")
    scroll_depth = Column(Integer, default=0, comment="滚动深度（%）")
    mouse_movements = Column(Text, comment="鼠标轨迹（JSON）")

    # 分析字段
    is_bot = Column(Boolean, default=False, index=True, comment="是否机器人")
    authenticity_score = Column(Float, default=0.0, index=True, comment="真实性评分 0-100")
    fingerprint_hash = Column(String(64), nullable=False, index=True, comment="综合指纹哈希")

    # 元数据
    raw_data = Column(Text, comment="原始数据备份（JSON）")

    # 复合索引 - 优化常用查询
    __table_args__ = (
        # 用于按时间和设备类型筛选（admin visits list）
        Index('idx_timestamp_device', timestamp, device_type),

        # 用于按时间和评分筛选
        Index('idx_timestamp_score', timestamp, authenticity_score),

        # 用于地理位置统计
        Index('idx_location', ip_country, ip_city),

        # 用于机器人检测和时间筛选
        Index('idx_timestamp_bot', timestamp, is_bot),
    )

    def __repr__(self):
        return f"<Visit {self.visit_id} - {self.ip_address} - {self.device_type}>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "visit_id": self.visit_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "ip_address": self.ip_address,
            "ip_country": self.ip_country,
            "ip_city": self.ip_city,
            "device_type": self.device_type,
            "browser": self.browser,
            "os": self.os,
            "authenticity_score": self.authenticity_score,
            "stay_duration": self.stay_duration,
            "scroll_depth": self.scroll_depth,
        }
