"""
개선된 분리수거 품목 분류 API v2
"""
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.base import ErrorHandler
from app.api.controllers.recycling_controller import RecyclingController
from app.core.database import get_db

router = APIRouter(prefix="/recycling", tags=["recycling"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """서비스 상태 확인"""
    try:
        controller = RecyclingController(db)
        response = controller.health_check()
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.get("/classes")
async def get_classes(db: Session = Depends(get_db)):
    """분류 가능한 클래스 목록 조회"""
    try:
        controller = RecyclingController(db)
        response = controller.get_class_info()
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.post("/classify")
async def classify_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """이미지 업로드 및 분류"""
    try:
        controller = RecyclingController(db)
        response = await controller.classify_image(file)
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.post("/classify/local")
async def classify_local_image(
    image_path: str,
    db: Session = Depends(get_db)
):
    """로컬 이미지 파일 분류"""
    try:
        controller = RecyclingController(db)
        response = controller.classify_local_image(image_path)
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)


@router.post("/batch-classify")
async def batch_classify_images(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """여러 이미지 일괄 분류"""
    try:
        controller = RecyclingController(db)
        response = await controller.batch_classify_images(files)
        return response.to_dict()
    except Exception as e:
        raise ErrorHandler.handle_internal_error(e)
