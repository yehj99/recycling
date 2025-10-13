"""
위치 기반 서비스 컨트롤러
"""
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, Query
from sqlalchemy.orm import Session

from app.api.base import BaseController, APIResponse, RequestValidator, ErrorHandler
from app.core.interfaces import ILocationService


class LocationController(BaseController):
    """위치 기반 서비스 컨트롤러"""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.location_service = self.get_service('location_service')
    
    def validate_request(self, request_data: Dict[str, Any]) -> bool:
        """요청 데이터 검증"""
        # 기본 검증 로직
        return True
    
    def get_nearby_locations(self, 
                           latitude: float, 
                           longitude: float,
                           waste_type: Optional[str] = None,
                           radius_km: float = 5.0,
                           limit: int = 10) -> APIResponse:
        """주변 배출 장소 조회"""
        try:
            # 좌표 검증
            if not RequestValidator.validate_coordinates(latitude, longitude):
                return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 반경 검증
            if not RequestValidator.validate_radius(radius_km):
                return APIResponse.error("반경은 0보다 크고 100km 이하여야 합니다.")
            
            # 제한 수 검증
            if not RequestValidator.validate_limit(limit):
                return APIResponse.error("제한 수는 0보다 크고 100 이하여야 합니다.")
            
            # 주변 배출 장소 조회
            locations = self.location_service.find_nearby_locations(
                latitude=latitude,
                longitude=longitude,
                waste_type=waste_type,
                radius_km=radius_km,
                limit=limit
            )
            
            return APIResponse.success({
                "count": len(locations),
                "locations": locations
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def get_location_by_id(self, location_id: int) -> APIResponse:
        """ID로 배출 장소 조회"""
        try:
            location = self.location_service.get_location_by_id(location_id)
            
            if not location:
                raise ErrorHandler.handle_not_found_error("배출 장소")
            
            return APIResponse.success({"location": location})
            
        except HTTPException:
            raise
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def add_recycling_location(self, location_data: Dict[str, Any]) -> APIResponse:
        """새로운 분리수거 배출 장소 추가"""
        try:
            # 필수 필드 검증
            required_fields = ['name', 'address', 'latitude', 'longitude', 'waste_types']
            for field in required_fields:
                if field not in location_data:
                    return APIResponse.error(f"필수 필드가 누락되었습니다: {field}")
            
            # 좌표 검증
            if not RequestValidator.validate_coordinates(
                location_data['latitude'], 
                location_data['longitude']
            ):
                return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 배출 장소 추가
            location = self.location_service.add_recycling_location(**location_data)
            
            return APIResponse.success({
                "message": "배출 장소가 성공적으로 추가되었습니다.",
                "location": location
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def update_recycling_location(self, location_id: int, location_data: Dict[str, Any]) -> APIResponse:
        """분리수거 배출 장소 정보 수정"""
        try:
            # 좌표 검증 (있는 경우)
            if 'latitude' in location_data and 'longitude' in location_data:
                if not RequestValidator.validate_coordinates(
                    location_data['latitude'], 
                    location_data['longitude']
                ):
                    return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 배출 장소 수정
            location = self.location_service.update_recycling_location(location_id, **location_data)
            
            if not location:
                raise ErrorHandler.handle_not_found_error("배출 장소")
            
            return APIResponse.success({
                "message": "배출 장소 정보가 성공적으로 수정되었습니다.",
                "location": location
            })
            
        except HTTPException:
            raise
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def delete_recycling_location(self, location_id: int) -> APIResponse:
        """분리수거 배출 장소 삭제"""
        try:
            success = self.location_service.delete_recycling_location(location_id)
            
            if not success:
                raise ErrorHandler.handle_not_found_error("배출 장소")
            
            return APIResponse.success({
                "message": "배출 장소가 성공적으로 삭제되었습니다."
            })
            
        except HTTPException:
            raise
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def save_user_location(self, 
                          latitude: float, 
                          longitude: float,
                          user_id: Optional[str] = None,
                          address: Optional[str] = None) -> APIResponse:
        """사용자 위치 저장"""
        try:
            # 좌표 검증
            if not RequestValidator.validate_coordinates(latitude, longitude):
                return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 사용자 위치 저장
            user_location = self.location_service.save_user_location(
                latitude=latitude,
                longitude=longitude,
                user_id=user_id,
                address=address
            )
            
            return APIResponse.success({
                "message": "사용자 위치가 성공적으로 저장되었습니다.",
                "location": user_location
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def get_waste_type_info(self) -> APIResponse:
        """쓰레기 종류별 정보 조회"""
        try:
            waste_info = self.location_service.get_waste_type_info()
            return APIResponse.success({"waste_types": waste_info})
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
