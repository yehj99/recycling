"""
API 기본 클래스 및 공통 기능
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.factories import service_container


class BaseAPI(ABC):
    """API 기본 클래스"""
    
    def __init__(self):
        self.service_container = service_container
    
    def get_service(self, service_name: str):
        """서비스 인스턴스 가져오기"""
        return self.service_container.get(service_name)
    
    def handle_error(self, error: Exception, message: str = None) -> HTTPException:
        """에러 처리"""
        error_message = message or f"처리 중 오류가 발생했습니다: {str(error)}"
        return HTTPException(status_code=500, detail=error_message)
    
    def create_response(self, data: Any, message: str = "성공", success: bool = True) -> Dict[str, Any]:
        """표준 응답 생성"""
        return {
            "success": success,
            "message": message,
            "data": data
        }


class BaseController(ABC):
    """컨트롤러 기본 클래스"""
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.service_container = service_container
    
    @abstractmethod
    def validate_request(self, request_data: Dict[str, Any]) -> bool:
        """요청 데이터 검증"""
        pass
    
    def get_service(self, service_name: str):
        """서비스 인스턴스 가져오기"""
        return self.service_container.get(service_name)


class APIResponse:
    """API 응답 래퍼"""
    
    def __init__(self, success: bool = True, message: str = "성공", data: Any = None):
        self.success = success
        self.message = message
        self.data = data
    
    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }
    
    @classmethod
    def success(cls, data: Any = None, message: str = "성공"):
        """성공 응답 생성"""
        return cls(success=True, message=message, data=data)
    
    @classmethod
    def error(cls, message: str = "오류가 발생했습니다", data: Any = None):
        """에러 응답 생성"""
        return cls(success=False, message=message, data=data)


class RequestValidator:
    """요청 검증기"""
    
    @staticmethod
    def validate_image_file(file_content_type: str) -> bool:
        """이미지 파일 검증"""
        return file_content_type.startswith('image/')
    
    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> bool:
        """좌표 검증"""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
    
    @staticmethod
    def validate_radius(radius: float) -> bool:
        """반경 검증"""
        return 0 < radius <= 100  # 최대 100km
    
    @staticmethod
    def validate_limit(limit: int) -> bool:
        """제한 수 검증"""
        return 0 < limit <= 100  # 최대 100개


class ErrorHandler:
    """에러 핸들러"""
    
    @staticmethod
    def handle_validation_error(error: Exception) -> HTTPException:
        """검증 에러 처리"""
        return HTTPException(status_code=400, detail=f"입력 데이터가 올바르지 않습니다: {str(error)}")
    
    @staticmethod
    def handle_not_found_error(resource: str) -> HTTPException:
        """리소스 없음 에러 처리"""
        return HTTPException(status_code=404, detail=f"{resource}을(를) 찾을 수 없습니다.")
    
    @staticmethod
    def handle_internal_error(error: Exception) -> HTTPException:
        """내부 서버 에러 처리"""
        return HTTPException(status_code=500, detail=f"서버 내부 오류가 발생했습니다: {str(error)}")
    
    @staticmethod
    def handle_service_error(error: Exception) -> HTTPException:
        """서비스 에러 처리"""
        return HTTPException(status_code=503, detail=f"서비스를 사용할 수 없습니다: {str(error)}")
