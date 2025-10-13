"""
팩토리 패턴을 사용한 객체 생성
"""
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.core.interfaces import IImageClassifier, ILocationService, IModelTrainer, IDataProcessor, IRepository
from app.models.recycling_classifier import RecyclingClassifier
from app.services.inference_service import InferenceService
from app.services.location_service import LocationService
from app.services.model_trainer import ModelTrainer
from app.core.data_processor import DataProcessor
from app.repositories.location_repository import LocationRepository


class ClassifierFactory:
    """분류기 팩토리"""
    
    @staticmethod
    def create_efficientnet_classifier(model_path: Optional[str] = None) -> IImageClassifier:
        """EfficientNet 기반 분류기 생성"""
        return RecyclingClassifier(model_path)
    
    @staticmethod
    def create_inference_service(model_path: str = "models/recycling_classifier.h5") -> IImageClassifier:
        """추론 서비스 생성"""
        return InferenceService(model_path)


class LocationServiceFactory:
    """위치 서비스 팩토리"""
    
    @staticmethod
    def create_location_service(db_session: Session) -> ILocationService:
        """위치 서비스 생성"""
        return LocationService(db_session)
    
    @staticmethod
    def create_location_repository(db_session: Session) -> IRepository:
        """위치 저장소 생성"""
        return LocationRepository(db_session)


class ModelTrainerFactory:
    """모델 훈련기 팩토리"""
    
    @staticmethod
    def create_model_trainer() -> IModelTrainer:
        """모델 훈련기 생성"""
        return ModelTrainer()


class DataProcessorFactory:
    """데이터 처리기 팩토리"""
    
    @staticmethod
    def create_data_processor() -> IDataProcessor:
        """데이터 처리기 생성"""
        return DataProcessor()


class ServiceContainer:
    """의존성 주입 컨테이너"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register_singleton(self, name: str, factory_func, *args, **kwargs):
        """싱글톤 서비스 등록"""
        self._singletons[name] = (factory_func, args, kwargs)
    
    def register_transient(self, name: str, factory_func, *args, **kwargs):
        """일시적 서비스 등록"""
        self._services[name] = (factory_func, args, kwargs)
    
    def get(self, name: str) -> Any:
        """서비스 인스턴스 가져오기"""
        # 싱글톤 서비스 확인
        if name in self._singletons:
            if name not in self._services:
                factory_func, args, kwargs = self._singletons[name]
                self._services[name] = factory_func(*args, **kwargs)
            return self._services[name]
        
        # 일시적 서비스 확인
        if name in self._services:
            factory_func, args, kwargs = self._services[name]
            return factory_func(*args, **kwargs)
        
        raise ValueError(f"Service '{name}' not registered")
    
    def get_singleton(self, name: str) -> Any:
        """싱글톤 서비스 인스턴스 가져오기"""
        if name not in self._services:
            if name in self._singletons:
                factory_func, args, kwargs = self._singletons[name]
                self._services[name] = factory_func(*args, **kwargs)
            else:
                raise ValueError(f"Singleton service '{name}' not registered")
        return self._services[name]


# 전역 서비스 컨테이너
service_container = ServiceContainer()
