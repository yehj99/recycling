# 객체지향 설계 문서

## 🏗️ 아키텍처 개요

이 프로젝트는 SOLID 원칙을 적용한 객체지향 설계로 리팩토링되었습니다.

## 📁 프로젝트 구조

```
app/
├── core/
│   ├── interfaces.py          # 핵심 인터페이스 정의
│   ├── factories.py           # 팩토리 패턴 구현
│   ├── service_registry.py    # 의존성 주입 컨테이너
│   ├── data_processor.py     # 데이터 처리기
│   └── database.py           # 데이터베이스 설정
├── models/
│   ├── recycling_classifier.py  # EfficientNetV2 모델
│   └── location.py           # 위치 모델
├── repositories/
│   └── location_repository.py    # 저장소 패턴 구현
├── services/
│   ├── inference_service.py      # 추론 서비스
│   ├── location_service.py       # 위치 서비스
│   └── model_trainer.py          # 모델 훈련 서비스
├── api/
│   ├── base.py               # API 기본 클래스
│   ├── controllers/          # 컨트롤러 패턴
│   │   ├── recycling_controller.py
│   │   ├── location_controller.py
│   │   └── integrated_controller.py
│   └── v2/                   # 개선된 API v2
│       ├── recycling.py
│       ├── location.py
│       └── integrated.py
└── main.py                   # FastAPI 애플리케이션
```

## 🎯 SOLID 원칙 적용

### 1. Single Responsibility Principle (SRP)
- **IImageClassifier**: 이미지 분류만 담당
- **ILocationService**: 위치 관련 서비스만 담당
- **IModelTrainer**: 모델 훈련만 담당
- **IDataProcessor**: 데이터 처리만 담당

### 2. Open/Closed Principle (OCP)
- 인터페이스를 통한 확장 가능한 설계
- 새로운 분류기나 서비스를 추가할 때 기존 코드 수정 없이 확장 가능

### 3. Liskov Substitution Principle (LSP)
- 모든 구현체는 인터페이스를 완전히 구현
- 구현체 간 교체 가능

### 4. Interface Segregation Principle (ISP)
- 클라이언트가 사용하지 않는 메서드에 의존하지 않음
- 작고 집중된 인터페이스들로 분리

### 5. Dependency Inversion Principle (DIP)
- 고수준 모듈이 저수준 모듈에 의존하지 않음
- 의존성 주입 컨테이너를 통한 의존성 관리

## 🏭 디자인 패턴

### 1. Factory Pattern
```python
class ClassifierFactory:
    @staticmethod
    def create_efficientnet_classifier(model_path: Optional[str] = None) -> IImageClassifier:
        return RecyclingClassifier(model_path)
```

### 2. Repository Pattern
```python
class LocationRepository(IRepository):
    def create(self, entity: Any) -> Any:
        # 엔티티 생성 로직
        pass
```

### 3. Service Container Pattern
```python
class ServiceContainer:
    def register_singleton(self, name: str, factory_func, *args, **kwargs):
        # 싱글톤 서비스 등록
        pass
```

### 4. Controller Pattern
```python
class RecyclingController(BaseController):
    def classify_image(self, file: UploadFile) -> APIResponse:
        # 이미지 분류 로직
        pass
```

## 🔧 핵심 컴포넌트

### 1. 인터페이스 (Interfaces)
- **IImageClassifier**: 이미지 분류 인터페이스
- **ILocationService**: 위치 서비스 인터페이스
- **IModelTrainer**: 모델 훈련 인터페이스
- **IDataProcessor**: 데이터 처리 인터페이스
- **IRepository**: 저장소 인터페이스

### 2. 팩토리 (Factories)
- **ClassifierFactory**: 분류기 생성
- **LocationServiceFactory**: 위치 서비스 생성
- **ModelTrainerFactory**: 모델 훈련기 생성
- **DataProcessorFactory**: 데이터 처리기 생성

### 3. 서비스 컨테이너 (Service Container)
- 의존성 주입 관리
- 싱글톤 및 일시적 서비스 등록
- 서비스 인스턴스 생성 및 관리

### 4. 컨트롤러 (Controllers)
- **RecyclingController**: 분리수거 품목 분류 컨트롤러
- **LocationController**: 위치 서비스 컨트롤러
- **IntegratedController**: 통합 서비스 컨트롤러

## 🚀 사용 예시

### 1. 서비스 사용
```python
# 서비스 컨테이너에서 서비스 가져오기
classifier = service_container.get('inference_service')
location_service = service_container.get('location_service', db_session)

# 서비스 사용
result = classifier.predict(image_path)
locations = location_service.find_nearby_locations(lat, lon)
```

### 2. 컨트롤러 사용
```python
# 컨트롤러 인스턴스 생성
controller = RecyclingController(db_session)

# API 요청 처리
response = controller.classify_image(uploaded_file)
return response.to_dict()
```

### 3. 저장소 사용
```python
# 저장소 인스턴스 생성
repository = LocationRepository(db_session)

# CRUD 작업
location = repository.create(new_location)
location = repository.get_by_id(location_id)
locations = repository.find_by_criteria(criteria)
```

## 📊 장점

### 1. 유지보수성
- 각 클래스가 단일 책임을 가짐
- 코드 변경 시 영향 범위 최소화

### 2. 확장성
- 새로운 기능 추가 시 기존 코드 수정 없이 확장 가능
- 인터페이스 기반 설계로 구현체 교체 용이

### 3. 테스트 용이성
- 의존성 주입을 통한 Mock 객체 사용 가능
- 각 컴포넌트별 단위 테스트 작성 용이

### 4. 재사용성
- 공통 기능을 인터페이스로 추상화
- 다양한 구현체에서 재사용 가능

## 🔄 API 버전 관리

### v1 API (기존)
- `/recycling/*` - 기존 분류 API
- `/location/*` - 기존 위치 API
- `/integrated/*` - 기존 통합 API

### v2 API (개선된 객체지향 버전)
- `/v2/recycling/*` - 개선된 분류 API
- `/v2/location/*` - 개선된 위치 API
- `/v2/integrated/*` - 개선된 통합 API

## 🧪 테스트 전략

### 1. 단위 테스트
- 각 클래스별 단위 테스트
- Mock 객체를 사용한 의존성 격리

### 2. 통합 테스트
- API 엔드포인트별 통합 테스트
- 실제 데이터베이스 사용

### 3. 성능 테스트
- 대용량 데이터 처리 성능 테스트
- 동시 요청 처리 성능 테스트

## 📈 향후 개선 방향

### 1. 캐싱 전략
- Redis를 활용한 결과 캐싱
- 메모리 캐싱 구현

### 2. 비동기 처리
- Celery를 활용한 비동기 작업 처리
- 큐 기반 작업 스케줄링

### 3. 모니터링
- 로깅 시스템 개선
- 메트릭 수집 및 모니터링

### 4. 보안
- 인증 및 권한 관리
- API 보안 강화
