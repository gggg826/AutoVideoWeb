"""
追踪 API 路由
处理访问记录和行为数据的追踪
"""
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.visit import VisitCreate, BehaviorUpdate, VisitResponse
from app.crud import visit as visit_crud
from app.utils.ip import get_client_ip

router = APIRouter(prefix="/track", tags=["tracker"])


@router.post("/", response_model=VisitResponse, summary="记录访问")
async def track_visit(
    visit_data: VisitCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    记录访问信息

    接收前端发送的访问数据，包括：
    - User-Agent（自动获取）
    - 页面 URL 和 Referrer
    - 浏览器指纹（Canvas、WebGL、字体等）

    返回：
    - visit_id: 访问记录的唯一ID（用于后续更新行为数据）
    - timestamp: 访问时间戳
    - ip_address: 客户端 IP 地址
    - device_type: 设备类型
    - authenticity_score: 初始真实性评分
    """
    # 获取客户端真实 IP
    ip_address = get_client_ip(request)

    # 创建访问记录
    visit = await visit_crud.create_visit(db, visit_data, ip_address)

    return VisitResponse(
        visit_id=visit.visit_id,
        timestamp=visit.timestamp,
        ip_address=visit.ip_address,
        device_type=visit.device_type,
        authenticity_score=visit.authenticity_score
    )


@router.post("/behavior", summary="更新行为数据")
async def update_behavior(
    behavior_data: BehaviorUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新访问记录的行为数据

    前端在页面卸载前发送行为数据，包括：
    - 停留时间（秒）
    - 滚动深度（%）
    - 鼠标移动轨迹（采样）

    这些数据用于评估访问的真实性
    """
    visit = await visit_crud.update_behavior(db, behavior_data)

    if not visit:
        raise HTTPException(status_code=404, detail="访问记录不存在")

    return {
        "success": True,
        "message": "行为数据已更新",
        "visit_id": visit.visit_id,
        "authenticity_score": visit.authenticity_score
    }


@router.get("/ping", summary="健康检查")
async def ping():
    """
    追踪服务健康检查
    """
    return {"status": "ok", "service": "tracker"}
