"""
통합 서비스 컨트롤러
"""
from typing import Dict, Any, List, Optional
from fastapi import UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.base import BaseController, APIResponse, RequestValidator, ErrorHandler
from app.core.interfaces import IImageClassifier, ILocationService


class IntegratedController(BaseController):
    """통합 서비스 컨트롤러"""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.classifier = self.get_service('inference_service')
        self.location_service = self.get_service('location_service')
    
    def validate_request(self, request_data: Dict[str, Any]) -> bool:
        """요청 데이터 검증"""
        return True
    
    def classify_and_find_locations(self, 
                                  file: UploadFile,
                                  latitude: float,
                                  longitude: float,
                                  radius_km: float = 5.0,
                                  limit: int = 10) -> APIResponse:
        """이미지 분류 + 주변 배출 장소 조회"""
        try:
            # 파일 검증
            if not RequestValidator.validate_image_file(file.content_type):
                return APIResponse.error("이미지 파일만 업로드 가능합니다.")
            
            # 좌표 검증
            if not RequestValidator.validate_coordinates(latitude, longitude):
                return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 반경 검증
            if not RequestValidator.validate_radius(radius_km):
                return APIResponse.error("반경은 0보다 크고 100km 이하여야 합니다.")
            
            # 제한 수 검증
            if not RequestValidator.validate_limit(limit):
                return APIResponse.error("제한 수는 0보다 크고 100 이하여야 합니다.")
            
            # 1. 이미지 분류
            contents = file.read()
            classification_result = self.classifier.classify_image_from_bytes(contents)
            
            if 'error' in classification_result:
                return APIResponse.error(classification_result['error'])
            
            # 2. 분류된 쓰레기 종류에 따른 주변 배출 장소 조회
            waste_type = classification_result['predicted_class']
            nearby_locations = self.location_service.find_nearby_locations(
                latitude=latitude,
                longitude=longitude,
                waste_type=waste_type,
                radius_km=radius_km,
                limit=limit
            )
            
            # 3. 쓰레기 종류별 정보 조회
            waste_info = self.location_service.get_waste_type_info()
            waste_type_info = waste_info.get(waste_type, {})
            
            # 4. 결과 통합
            result = {
                "classification": {
                    "filename": file.filename,
                    "predicted_class": classification_result['predicted_class'],
                    "confidence": classification_result['confidence'],
                    "is_recyclable": classification_result['is_recyclable'],
                    "class_probabilities": classification_result['class_probabilities']
                },
                "waste_type_info": waste_type_info,
                "nearby_locations": {
                    "count": len(nearby_locations),
                    "locations": nearby_locations
                },
                "user_location": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
            
            return APIResponse.success(result)
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def batch_classify_and_find_locations(self, 
                                         files: List[UploadFile],
                                         latitude: float,
                                         longitude: float,
                                         radius_km: float = 5.0,
                                         limit: int = 10) -> APIResponse:
        """여러 이미지 일괄 분류 + 주변 배출 장소 조회"""
        try:
            if len(files) > 10:
                return APIResponse.error("한 번에 최대 10개 파일까지만 처리 가능합니다.")
            
            # 좌표 검증
            if not RequestValidator.validate_coordinates(latitude, longitude):
                return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 반경 검증
            if not RequestValidator.validate_radius(radius_km):
                return APIResponse.error("반경은 0보다 크고 100km 이하여야 합니다.")
            
            # 제한 수 검증
            if not RequestValidator.validate_limit(limit):
                return APIResponse.error("제한 수는 0보다 크고 100 이하여야 합니다.")
            
            waste_info = self.location_service.get_waste_type_info()
            results = []
            
            for file in files:
                try:
                    # 파일 검증
                    if not RequestValidator.validate_image_file(file.content_type):
                        results.append({
                            "filename": file.filename,
                            "error": "이미지 파일이 아닙니다.",
                            "classification": None,
                            "nearby_locations": None
                        })
                        continue
                    
                    # 파일 읽기
                    contents = file.read()
                    
                    # 이미지 분류
                    classification_result = self.classifier.classify_image_from_bytes(contents)
                    
                    if 'error' in classification_result:
                        results.append({
                            "filename": file.filename,
                            "error": classification_result['error'],
                            "classification": None,
                            "nearby_locations": None
                        })
                        continue
                    
                    # 분류된 쓰레기 종류에 따른 주변 배출 장소 조회
                    waste_type = classification_result['predicted_class']
                    nearby_locations = self.location_service.find_nearby_locations(
                        latitude=latitude,
                        longitude=longitude,
                        waste_type=waste_type,
                        radius_km=radius_km,
                        limit=limit
                    )
                    
                    # 쓰레기 종류별 정보
                    waste_type_info = waste_info.get(waste_type, {})
                    
                    # 결과 추가
                    results.append({
                        "filename": file.filename,
                        "classification": {
                            "predicted_class": classification_result['predicted_class'],
                            "confidence": classification_result['confidence'],
                            "is_recyclable": classification_result['is_recyclable'],
                            "class_probabilities": classification_result['class_probabilities']
                        },
                        "waste_type_info": waste_type_info,
                        "nearby_locations": {
                            "count": len(nearby_locations),
                            "locations": nearby_locations
                        }
                    })
                    
                except Exception as e:
                    results.append({
                        "filename": file.filename,
                        "error": f"처리 중 오류가 발생했습니다: {str(e)}",
                        "classification": None,
                        "nearby_locations": None
                    })
            
            return APIResponse.success({
                "total_files": len(files),
                "user_location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "results": results
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
    
    def get_smart_recommendation(self, 
                               latitude: float,
                               longitude: float,
                               radius_km: float = 5.0) -> APIResponse:
        """스마트 추천 - 사용자 위치 기반 최적 배출 장소 추천"""
        try:
            # 좌표 검증
            if not RequestValidator.validate_coordinates(latitude, longitude):
                return APIResponse.error("올바르지 않은 좌표입니다.")
            
            # 반경 검증
            if not RequestValidator.validate_radius(radius_km):
                return APIResponse.error("반경은 0보다 크고 100km 이하여야 합니다.")
            
            waste_info = self.location_service.get_waste_type_info()
            recommendations = {}
            
            # 각 쓰레기 종류별로 최적 배출 장소 조회
            for waste_type in ['glass', 'paper', 'plastic', 'metal']:
                nearby_locations = self.location_service.find_nearby_locations(
                    latitude=latitude,
                    longitude=longitude,
                    waste_type=waste_type,
                    radius_km=radius_km,
                    limit=3  # 각 종류별로 최대 3개씩
                )
                
                recommendations[waste_type] = {
                    "waste_info": waste_info.get(waste_type, {}),
                    "locations": nearby_locations,
                    "count": len(nearby_locations)
                }
            
            return APIResponse.success({
                "user_location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "recommendations": recommendations
            })
            
        except Exception as e:
            raise ErrorHandler.handle_internal_error(e)
