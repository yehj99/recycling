"""
서비스 레지스트리 - 의존성 주입 설정
"""
from sqlalchemy.orm import Session

from app.core.factories import service_container, ClassifierFactory, LocationServiceFactory, ModelTrainerFactory, DataProcessorFactory
from app.core.database import get_db


def register_services():
    """서비스 등록"""
    # 싱글톤 서비스 등록
    service_container.register_singleton(
        'inference_service',
        ClassifierFactory.create_inference_service,
        "models/recycling_classifier.h5"
    )
    
    service_container.register_singleton(
        'data_processor',
        DataProcessorFactory.create_data_processor
    )
    
    service_container.register_singleton(
        'model_trainer',
        ModelTrainerFactory.create_model_trainer
    )
    
    # 일시적 서비스 등록 (DB 세션 필요)
    service_container.register_transient(
        'location_service',
        LocationServiceFactory.create_location_service
    )
    
    service_container.register_transient(
        'location_repository',
        LocationServiceFactory.create_location_repository
    )


def get_service_with_db(service_name: str, db: Session):
    """DB 세션이 필요한 서비스 가져오기"""
    if service_name in ['location_service', 'location_repository']:
        # DB 세션이 필요한 서비스는 매번 새로 생성
        if service_name == 'location_service':
            from app.core.factories import LocationServiceFactory
            return LocationServiceFactory.create_location_service(db)
        elif service_name == 'location_repository':
            from app.core.factories import LocationServiceFactory
            return LocationServiceFactory.create_location_repository(db)
    else:
        return service_container.get(service_name)


# 서비스 등록 실행
register_services()
