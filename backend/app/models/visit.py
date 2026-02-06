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
    ip_address = Column(String(45), nullable=False, index=True, comment="初始IP地址")
    ip_country = Column(String(2), index=True, comment="国家代码")
    ip_city = Column(String(100), index=True, comment="城市")
    is_proxy = Column(Boolean, default=False, comment="是否代理IP")

    # IP 变化检测
    last_ip = Column(String(45), comment="最后一次请求的IP地址")
    ip_changed = Column(Boolean, default=False, index=True, comment="访问期间IP是否变化")
    ip_change_count = Column(Integer, default=0, comment="IP变化次数")

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

    # 浏览器指纹 - 基础
    screen_resolution = Column(String(20), comment="屏幕分辨率")
    viewport_size = Column(String(20), comment="视口大小")
    timezone = Column(String(50), comment="时区")
    language = Column(String(10), comment="语言")
    platform = Column(String(50), comment="平台")
    canvas_fingerprint = Column(String(64), comment="Canvas 指纹")
    webgl_fingerprint = Column(String(64), comment="WebGL 指纹")
    fonts_hash = Column(String(64), comment="字体列表哈希")

    # WebGL 详细信息
    webgl_vendor = Column(String(200), comment="WebGL 显卡供应商")
    webgl_renderer = Column(String(200), comment="WebGL 渲染器")

    # 硬件信息
    device_memory = Column(Float, comment="设备内存(GB)")
    hardware_concurrency = Column(Integer, comment="CPU核心数")
    color_depth = Column(Integer, comment="颜色深度")
    pixel_ratio = Column(Float, comment="设备像素比")
    max_touch_points = Column(Integer, comment="最大触点数")

    # 网络信息
    connection_type = Column(String(20), comment="网络类型(4g/3g/wifi等)")
    connection_downlink = Column(Float, comment="下行速度(Mbps)")
    connection_rtt = Column(Integer, comment="网络延迟(ms)")
    connection_save_data = Column(Boolean, comment="是否开启省流量")

    # 浏览器功能
    cookies_enabled = Column(Boolean, comment="Cookie是否启用")
    do_not_track = Column(Boolean, comment="是否启用DNT")
    pdf_viewer_enabled = Column(Boolean, comment="PDF查看器是否启用")
    plugins_hash = Column(String(64), comment="插件列表哈希")

    # 音频指纹
    audio_fingerprint = Column(String(64), comment="音频上下文指纹")

    # 媒体设备
    media_devices_hash = Column(String(64), comment="媒体设备列表哈希")

    # 存储支持
    local_storage_enabled = Column(Boolean, comment="localStorage是否可用")
    session_storage_enabled = Column(Boolean, comment="sessionStorage是否可用")
    indexed_db_enabled = Column(Boolean, comment="IndexedDB是否可用")

    # 广告拦截检测
    ad_blocker_detected = Column(Boolean, comment="是否检测到广告拦截器")

    # 电池信息
    battery_charging = Column(Boolean, comment="是否充电")
    battery_level = Column(Integer, comment="电量百分比")
    battery_charging_time = Column(Float, comment="充满所需时间(秒)")
    battery_discharging_time = Column(Float, comment="放电剩余时间(秒)")

    # WebRTC 哈希
    webrtc_hash = Column(String(64), comment="WebRTC候选哈希")

    # 语音列表哈希
    speech_voices_hash = Column(String(64), comment="语音合成列表哈希")

    # 性能指标
    page_load_time = Column(Integer, comment="页面加载时间(ms)")
    dom_parse_time = Column(Integer, comment="DOM解析时间(ms)")
    dns_time = Column(Integer, comment="DNS查询时间(ms)")
    tcp_time = Column(Integer, comment="TCP连接时间(ms)")
    ttfb = Column(Integer, comment="首字节时间(ms)")

    # Headless 检测
    is_headless = Column(Boolean, comment="是否Headless浏览器")

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
