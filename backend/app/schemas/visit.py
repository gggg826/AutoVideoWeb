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

    # 浏览器指纹
    screen_resolution: Optional[str] = Field(None, description="屏幕分辨率 (如 1920x1080)")
    timezone: Optional[str] = Field(None, description="时区 (如 Asia/Shanghai)")
    language: Optional[str] = Field(None, description="语言 (如 zh-CN)")
    platform: Optional[str] = Field(None, description="平台 (如 Win32)")
    canvas_fingerprint: Optional[str] = Field(None, description="Canvas 指纹哈希")
    webgl_fingerprint: Optional[str] = Field(None, description="WebGL 指纹哈希")
    fonts_hash: Optional[str] = Field(None, description="字体列表哈希")

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
                "timezone": "Asia/Shanghai",
                "language": "zh-CN",
                "platform": "Win32",
                "canvas_fingerprint": "a1b2c3d4",
                "webgl_fingerprint": "e5f6g7h8",
                "fonts_hash": "i9j0k1l2"
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
