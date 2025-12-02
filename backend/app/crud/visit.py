"""
访问记录 CRUD 操作
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.visit import Visit
from app.schemas.visit import VisitCreate, BehaviorUpdate
from app.utils.hash import generate_fingerprint_hash, calculate_fingerprint_quality
from app.utils.ua import parse_user_agent
from typing import Optional, List
import uuid
import json


async def create_visit(
    db: AsyncSession,
    visit_data: VisitCreate,
    ip_address: str
) -> Visit:
    """
    创建访问记录

    Args:
        db: 数据库会话
        visit_data: 访问数据
        ip_address: 客户端 IP 地址

    Returns:
        Visit: 创建的访问记录
    """
    # 解析 User-Agent
    ua_info = parse_user_agent(visit_data.user_agent)

    # 生成指纹哈希
    fingerprint_hash = generate_fingerprint_hash(
        visit_data.canvas_fingerprint,
        visit_data.webgl_fingerprint,
        visit_data.fonts_hash,
        visit_data.screen_resolution,
        visit_data.timezone,
        ip_address
    )

    # 计算指纹质量
    fingerprint_quality = calculate_fingerprint_quality(
        canvas=visit_data.canvas_fingerprint,
        webgl=visit_data.webgl_fingerprint,
        fonts=visit_data.fonts_hash,
        screen=visit_data.screen_resolution,
        timezone=visit_data.timezone,
        language=visit_data.language
    )

    # 简单的真实性评分（基于指纹质量）
    authenticity_score = float(fingerprint_quality)

    # 创建访问记录
    visit = Visit(
        visit_id=str(uuid.uuid4()),
        ip_address=ip_address,
        user_agent=visit_data.user_agent,
        referrer=visit_data.referrer,
        page_url=visit_data.page_url,
        # 设备信息（从 UA 解析）
        device_type=ua_info["device_type"],
        browser=ua_info["browser"],
        browser_version=ua_info["browser_version"],
        os=ua_info["os"],
        os_version=ua_info["os_version"],
        is_bot=ua_info["is_bot"],
        # 浏览器指纹
        screen_resolution=visit_data.screen_resolution,
        timezone=visit_data.timezone,
        language=visit_data.language,
        platform=visit_data.platform,
        canvas_fingerprint=visit_data.canvas_fingerprint,
        webgl_fingerprint=visit_data.webgl_fingerprint,
        fonts_hash=visit_data.fonts_hash,
        # 分析字段
        fingerprint_hash=fingerprint_hash,
        authenticity_score=authenticity_score,
        # 元数据
        raw_data=json.dumps(visit_data.extra_data) if visit_data.extra_data else None
    )

    db.add(visit)
    await db.commit()
    await db.refresh(visit)

    return visit


async def update_behavior(
    db: AsyncSession,
    behavior_data: BehaviorUpdate
) -> Optional[Visit]:
    """
    更新访问记录的行为数据

    Args:
        db: 数据库会话
        behavior_data: 行为数据

    Returns:
        Optional[Visit]: 更新后的访问记录，如果未找到则返回 None
    """
    # 查询访问记录
    stmt = select(Visit).where(Visit.visit_id == behavior_data.visit_id)
    result = await db.execute(stmt)
    visit = result.scalar_one_or_none()

    if not visit:
        return None

    # 更新行为数据
    if behavior_data.stay_duration is not None:
        visit.stay_duration = behavior_data.stay_duration

    if behavior_data.scroll_depth is not None:
        visit.scroll_depth = behavior_data.scroll_depth

    if behavior_data.mouse_movements is not None:
        visit.mouse_movements = behavior_data.mouse_movements

    # 根据行为数据更新真实性评分
    # 基础评分（指纹质量）+ 行为评分
    behavior_score = 0
    if visit.stay_duration > 3:  # 停留超过 3 秒
        behavior_score += 10
    if visit.scroll_depth > 10:  # 滚动超过 10%
        behavior_score += 10

    visit.authenticity_score = min(100.0, visit.authenticity_score + behavior_score)

    await db.commit()
    await db.refresh(visit)

    return visit


async def get_visit_by_id(db: AsyncSession, visit_id: str) -> Optional[Visit]:
    """
    根据 visit_id 获取访问记录

    Args:
        db: 数据库会话
        visit_id: 访问记录 ID

    Returns:
        Optional[Visit]: 访问记录，如果未找到则返回 None
    """
    stmt = select(Visit).where(Visit.visit_id == visit_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_recent_visits(
    db: AsyncSession,
    limit: int = 100,
    offset: int = 0
) -> List[Visit]:
    """
    获取最近的访问记录

    Args:
        db: 数据库会话
        limit: 返回数量限制
        offset: 偏移量

    Returns:
        List[Visit]: 访问记录列表
    """
    stmt = select(Visit).order_by(Visit.timestamp.desc()).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_total_visits(db: AsyncSession) -> int:
    """
    获取总访问量

    Args:
        db: 数据库会话

    Returns:
        int: 总访问量
    """
    stmt = select(func.count(Visit.id))
    result = await db.execute(stmt)
    return result.scalar_one()
