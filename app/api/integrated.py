"""
개선된 통합 API v2
"""
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.base import ErrorHandler
from app.api.controllers.integrated_controller import IntegratedController
from app.core.database import get_db

router = APIRouter(prefix="/integrated", tags=["integrated"])


@router.post("/classify-and-locate")
async def classify_and_find_locations(
    file: UploadFile = File(...),
    latitude: float = Query(..., description="사용자 위도"),
    longitude: float = Query(..., description="사용자 경도"),
    radius_km: float = Query(5.0, description="검색 반경 (km)"),
    limit: int = Query(10, description="최대 결과 수"),
    db: Session = Depends(get_db)
):
    """이미지 분류 + 주변 배출 장소 조회 통합 API"""
    try:
        controller = IntegratedController(db)
        response = controller.classify_and_find_locations(
            file=file,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            limit=limit
        )
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.post("/batch-classify-and-locate")
async def batch_classify_and_find_locations(
    files: List[UploadFile] = File(...),
    latitude: float = Query(..., description="사용자 위도"),
    longitude: float = Query(..., description="사용자 경도"),
    radius_km: float = Query(5.0, description="검색 반경 (km)"),
    limit: int = Query(10, description="최대 결과 수"),
    db: Session = Depends(get_db)
):
    """여러 이미지 일괄 분류 + 주변 배출 장소 조회"""
    try:
        controller = IntegratedController(db)
        response = controller.batch_classify_and_find_locations(
            files=files,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            limit=limit
        )
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.get("/smart-recommendation")
async def get_smart_recommendation(
    latitude: float = Query(..., description="사용자 위도"),
    longitude: float = Query(..., description="사용자 경도"),
    radius_km: float = Query(5.0, description="검색 반경 (km)"),
    db: Session = Depends(get_db)
):
    """스마트 추천 - 사용자 위치 기반 최적 배출 장소 추천"""
    try:
        controller = IntegratedController(db)
        response = controller.get_smart_recommendation(
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km
        )
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)
