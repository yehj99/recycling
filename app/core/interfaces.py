"""
애플리케이션의 핵심 인터페이스 정의
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import numpy as np


class IImageClassifier(ABC):
    """이미지 분류기 인터페이스"""
    
    @abstractmethod
    def predict(self, image_path: str) -> Dict[str, Any]:
        """이미지 분류 예측"""
        pass
    
    @abstractmethod
    def predict_from_array(self, image_array: np.ndarray) -> Dict[str, Any]:
        """numpy 배열로부터 이미지 분류 예측"""
        pass
    
    @abstractmethod
    def get_class_info(self) -> Dict[str, Any]:
        """클래스 정보 반환"""
        pass


class ILocationService(ABC):
    """위치 서비스 인터페이스"""
    
    @abstractmethod
    def find_nearby_locations(self, 
                            latitude: float, 
                            longitude: float, 
                            waste_type: Optional[str] = None,
                            radius_km: float = 5.0,
                            limit: int = 10) -> List[Dict[str, Any]]:
        """주변 분리수거 배출 장소 찾기"""
        pass
    
    @abstractmethod
    def get_location_by_id(self, location_id: int) -> Optional[Dict[str, Any]]:
        """ID로 배출 장소 조회"""
        pass
    
    @abstractmethod
    def save_user_location(self, 
                          latitude: float, 
                          longitude: float,
                          user_id: Optional[str] = None,
                          address: Optional[str] = None) -> Dict[str, Any]:
        """사용자 위치 저장"""
        pass


class IModelTrainer(ABC):
    """모델 훈련기 인터페이스"""
    
    @abstractmethod
    def train(self, data_dir: str, epochs: int = 10, save_path: str = None) -> Dict[str, Any]:
        """모델 훈련"""
        pass
    
    @abstractmethod
    def validate_model(self, validation_data: Any) -> Dict[str, Any]:
        """모델 검증"""
        pass


class IDataProcessor(ABC):
    """데이터 처리기 인터페이스"""
    
    @abstractmethod
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """이미지 전처리"""
        pass
    
    @abstractmethod
    def augment_data(self, data: Any) -> Any:
        """데이터 증강"""
        pass


class IRepository(ABC):
    """저장소 인터페이스"""
    
    @abstractmethod
    def create(self, entity: Any) -> Any:
        """엔티티 생성"""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Any]:
        """ID로 엔티티 조회"""
        pass
    
    @abstractmethod
    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[Any]:
        """엔티티 업데이트"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """엔티티 삭제"""
        pass
    
    @abstractmethod
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[Any]:
        """조건에 따른 엔티티 조회"""
        pass
