"""
访问记录相关的 Pydantic Schema
用于请求验证和响应序列化
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class VisitCreate(BaseModel):
    """创建访问记录的请求体"""

    # 请求信息（自动获取）
    user_agent: str = Field(..., description="User-Agent 字符串")
    referrer: Optional[str] = Field(None, description="来源页面 URL")
    page_url: str = Field(..., description="当前页面 URL")

    # 浏览器指纹 - 基础
    screen_resolution: Optional[str] = Field(None, description="屏幕分辨率 (如 1920x1080)")
    viewport_size: Optional[str] = Field(None, description="视口大小 (如 1366x768)")
    timezone: Optional[str] = Field(None, description="时区 (如 Asia/Shanghai)")
    language: Optional[str] = Field(None, description="语言 (如 zh-CN)")
    platform: Optional[str] = Field(None, description="平台 (如 Win32)")
    canvas_fingerprint: Optional[str] = Field(None, description="Canvas 指纹哈希")
    webgl_fingerprint: Optional[str] = Field(None, description="WebGL 指纹哈希")
    fonts_hash: Optional[str] = Field(None, description="字体列表哈希")

    # WebGL 详细信息
    webgl_vendor: Optional[str] = Field(None, description="WebGL 显卡供应商")
    webgl_renderer: Optional[str] = Field(None, description="WebGL 渲染器")

    # 硬件信息
    device_memory: Optional[float] = Field(None, description="设备内存(GB)")
    hardware_concurrency: Optional[int] = Field(None, description="CPU核心数")
    color_depth: Optional[int] = Field(None, description="颜色深度")
    pixel_ratio: Optional[float] = Field(None, description="设备像素比")
    max_touch_points: Optional[int] = Field(None, description="最大触点数")

    # 网络信息
    connection_type: Optional[str] = Field(None, description="网络类型(4g/3g/wifi等)")
    connection_downlink: Optional[float] = Field(None, description="下行速度(Mbps)")
    connection_rtt: Optional[int] = Field(None, description="网络延迟(ms)")
    connection_save_data: Optional[bool] = Field(None, description="是否开启省流量")

    # 浏览器功能
    cookies_enabled: Optional[bool] = Field(None, description="Cookie是否启用")
    do_not_track: Optional[bool] = Field(None, description="是否启用DNT")
    pdf_viewer_enabled: Optional[bool] = Field(None, description="PDF查看器是否启用")
    plugins_hash: Optional[str] = Field(None, description="插件列表哈希")

    # 音频指纹
    audio_fingerprint: Optional[str] = Field(None, description="音频上下文指纹")

    # 媒体设备
    media_devices_hash: Optional[str] = Field(None, description="媒体设备列表哈希")

    # 存储支持
    local_storage_enabled: Optional[bool] = Field(None, description="localStorage是否可用")
    session_storage_enabled: Optional[bool] = Field(None, description="sessionStorage是否可用")
    indexed_db_enabled: Optional[bool] = Field(None, description="IndexedDB是否可用")

    # 广告拦截检测
    ad_blocker_detected: Optional[bool] = Field(None, description="是否检测到广告拦截器")

    # 电池信息
    battery_charging: Optional[bool] = Field(None, description="是否充电")
    battery_level: Optional[int] = Field(None, description="电量百分比")
    battery_charging_time: Optional[float] = Field(None, description="充满所需时间(秒)")
    battery_discharging_time: Optional[float] = Field(None, description="放电剩余时间(秒)")

    # WebRTC 哈希
    webrtc_hash: Optional[str] = Field(None, description="WebRTC候选哈希")

    # 语音列表哈希
    speech_voices_hash: Optional[str] = Field(None, description="语音合成列表哈希")

    # 性能指标
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="性能指标")

    # Headless 检测
    is_headless: Optional[bool] = Field(None, description="是否Headless浏览器")

    # 浏览器地理位置（用户授权后获取）
    geolocation: Optional[Dict[str, Any]] = Field(None, description="浏览器地理位置信息")

    # 额外数据（可选）
    extra_data: Optional[Dict[str, Any]] = Field(None, description="其他元数据")

    class Config:
        json_schema_extra = {
            "example": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "referrer": "https://google.com",
                "page_url": "https://example.com/landing",
                "screen_resolution": "1920x1080",
                "viewport_size": "1366x768",
                "timezone": "Asia/Shanghai",
                "language": "zh-CN",
                "platform": "Win32",
                "canvas_fingerprint": "a1b2c3d4",
                "webgl_fingerprint": "e5f6g7h8",
                "fonts_hash": "i9j0k1l2",
                "webgl_vendor": "Google Inc. (NVIDIA)",
                "webgl_renderer": "ANGLE (NVIDIA GeForce GTX 1080)",
                "device_memory": 8,
                "hardware_concurrency": 8,
                "color_depth": 24,
                "pixel_ratio": 1.5,
                "max_touch_points": 0,
                "connection_type": "4g",
                "connection_downlink": 10.0,
                "connection_rtt": 50,
                "cookies_enabled": True,
                "do_not_track": False,
                "audio_fingerprint": "abc123",
                "local_storage_enabled": True,
                "session_storage_enabled": True,
                "indexed_db_enabled": True,
                "ad_blocker_detected": False,
                "is_headless": False
            }
        }


class BehaviorUpdate(BaseModel):
    """更新行为数据的请求体"""

    visit_id: str = Field(..., description="访问记录的唯一ID")
    stay_duration: Optional[int] = Field(None, ge=0, description="停留时间（秒）")
    scroll_depth: Optional[int] = Field(None, ge=0, le=100, description="滚动深度（%）")
    mouse_movements: Optional[str] = Field(None, description="鼠标轨迹（JSON字符串）")

    class Config:
        json_schema_extra = {
            "example": {
                "visit_id": "550e8400-e29b-41d4-a716-446655440000",
                "stay_duration": 45,
                "scroll_depth": 75,
                "mouse_movements": '[{"x":100,"y":200,"t":1000}]'
            }
        }


class VisitResponse(BaseModel):
    """访问记录响应"""

    visit_id: str
    timestamp: datetime
    ip_address: str
    device_type: Optional[str] = None
    authenticity_score: float

    class Config:
        from_attributes = True


class VisitDetail(BaseModel):
    """访问记录详细信息"""

    id: int
    visit_id: str
    timestamp: datetime

    # IP 信息
    ip_address: str
    ip_country: Optional[str] = None
    ip_city: Optional[str] = None
    is_proxy: bool

    # 设备信息
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None

    # 行为数据
    stay_duration: int
    scroll_depth: int

    # 分析结果
    is_bot: bool
    authenticity_score: float

    class Config:
        from_attributes = True
