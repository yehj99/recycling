"""
개선된 위치 기반 서비스 API v2
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.api.base import ErrorHandler
from app.api.controllers.location_controller import LocationController
from app.core.database import get_db

router = APIRouter(prefix="/location", tags=["location"])


class RecyclingLocationRequest(BaseModel):
    """분리수거 배출 장소 추가 요청 모델"""
    name: str
    address: str
    latitude: float
    longitude: float
    waste_types: list[str]
    operating_hours: Optional[str] = None
    contact_info: Optional[str] = None
    description: Optional[str] = None


@router.get("/nearby")
async def get_nearby_locations(
    latitude: float = Query(..., description="위도"),
    longitude: float = Query(..., description="경도"),
    waste_type: Optional[str] = Query(None, description="쓰레기 종류"),
    radius_km: float = Query(5.0, description="검색 반경 (km)"),
    limit: int = Query(10, description="최대 결과 수"),
    db: Session = Depends(get_db)
):
    """주변 분리수거 배출 장소 조회 (공공 API + 로컬 DB)"""
    try:
        controller = LocationController(db)
        response = await controller.get_nearby_locations(
            latitude=latitude,
            longitude=longitude,
            waste_type=waste_type,
            radius_km=radius_km,
            limit=limit
        )
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.get("/{location_id}")
async def get_location_by_id(
    location_id: int,
    db: Session = Depends(get_db)
):
    """ID로 배출 장소 조회"""
    try:
        controller = LocationController(db)
        response = controller.get_location_by_id(location_id)
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.post("/add")
async def add_recycling_location(
    request: RecyclingLocationRequest,
    db: Session = Depends(get_db)
):
    """새로운 분리수거 배출 장소 추가"""
    try:
        controller = LocationController(db)
        response = controller.add_recycling_location(request.dict())
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.put("/{location_id}")
async def update_recycling_location(
    location_id: int,
    request: RecyclingLocationRequest,
    db: Session = Depends(get_db)
):
    """분리수거 배출 장소 정보 수정"""
    try:
        controller = LocationController(db)
        response = controller.update_recycling_location(location_id, request.dict())
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.delete("/{location_id}")
async def delete_recycling_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    """분리수거 배출 장소 삭제"""
    try:
        controller = LocationController(db)
        response = controller.delete_recycling_location(location_id)
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.post("/save-user-location")
async def save_user_location(
    latitude: float = Query(..., description="위도"),
    longitude: float = Query(..., description="경도"),
    user_id: Optional[str] = Query(None, description="사용자 ID"),
    address: Optional[str] = Query(None, description="주소"),
    db: Session = Depends(get_db)
):
    """사용자 위치 저장"""
    try:
        controller = LocationController(db)
        response = controller.save_user_location(
            latitude=latitude,
            longitude=longitude,
            user_id=user_id,
            address=address
        )
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.get("/waste-types/info")
async def get_waste_type_info(db: Session = Depends(get_db)):
    """쓰레기 종류별 정보 조회"""
    try:
        controller = LocationController(db)
        response = controller.get_waste_type_info()
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)
