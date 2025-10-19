# 분리수거 품목 분류 시스템

EfficientNetV2를 사용한 분리수거 품목 자동 분류 시스템입니다.

## 기능

- **이미지 분류**: 업로드된 이미지를 5개 클래스로 분류
- **분리수거 가능 여부 판단**: 분리수거 가능한 품목인지 자동 판단
- **위치 기반 배출 정보**: 사용자 위치 기반 주변 분리수거 배출 장소 조회
- **통합 API**: 이미지 분류 + 위치 기반 배출 정보 통합 제공
- **REST API**: FastAPI를 통한 웹 API 제공
- **배치 처리**: 여러 이미지 동시 처리

## 분류 클래스

1. **glass** - 유리 (분리수거 가능)
2. **paper** - 종이 (분리수거 가능)
3. **plastic** - 플라스틱 (분리수거 가능)
4. **metal** - 금속 (분리수거 가능)
5. **trash** - 일반 쓰레기

## 설치 및 실행

### Docker Compose 사용 (권장)

#### 1. 개발 환경 실행

```bash
# 개발 환경으로 실행
docker-compose -f docker-compose.dev.yml up --build

# 백그라운드 실행
docker-compose -f docker-compose.dev.yml up -d --build
```

#### 2. 프로덕션 환경 실행

```bash
# 프로덕션 환경으로 실행
docker-compose -f docker-compose.prod.yml up --build

# 백그라운드 실행
docker-compose -f docker-compose.prod.yml up -d --build
```

#### 3. 기본 Docker Compose 실행

```bash
# 기본 설정으로 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build
```

#### 4. 서비스 중지

```bash
# 실행 중인 서비스 중지
docker-compose down

# 볼륨까지 삭제하며 중지
docker-compose down -v
```

#### 5. 데이터베이스 초기화

```bash
# 데이터베이스 초기화 (샘플 데이터 포함)
docker-compose exec recycling-app python init_database.py
```

#### 6. 서비스 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 로그 확인
docker-compose logs -f recycling-app

# 특정 서비스 로그만 확인
docker-compose logs recycling-app
```

#### 7. Docker Compose 설정 설명

- **기본 설정** (`docker-compose.yml`): SQLite + PostgreSQL 옵션 포함
- **개발 환경** (`docker-compose.dev.yml`): 코드 변경 시 자동 재시작 (--reload)
- **프로덕션 환경** (`docker-compose.prod.yml`): 최적화된 설정, 리소스 제한

#### 8. 포트 및 접속 정보

- **API 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **PostgreSQL 버전**: http://localhost:8001 (선택사항)

### 로컬 설치 (Docker 없이)

#### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

#### 2. 데이터 준비

훈련 데이터를 다음과 같은 구조로 준비하세요:

```
data/
├── train/
│   ├── glass/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── paper/
│   ├── plastic/
│   ├── metal/
│   └── trash/
```

#### 3. 모델 훈련

```bash
python train_model.py --data_dir ./data/train --epochs 20 --model_path ./models/recycling_classifier.h5
```

#### 4. 추론 테스트

```bash
python test_inference.py --image_path ./test_image.jpg --model_path ./models/recycling_classifier.h5
```

#### 5. 샘플 데이터 추가

```bash
python add_sample_data.py
```

#### 6. API 서버 실행

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API 사용법

### 1. 서비스 상태 확인

```bash
curl http://localhost:8000/recycling/health
```

### 2. 이미지 분류

```bash
curl -X POST "http://localhost:8000/recycling/classify" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg"
```

### 3. 로컬 이미지 분류

```bash
curl -X POST "http://localhost:8000/recycling/classify/local?image_path=./test_image.jpg"
```

### 4. 배치 분류

```bash
curl -X POST "http://localhost:8000/recycling/batch-classify" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@image1.jpg" \
     -F "files=@image2.jpg"
```

### 5. 주변 배출 장소 조회

```bash
curl "http://localhost:8000/location/nearby?latitude=37.5665&longitude=127.0780&waste_type=plastic"
```

### 6. 통합 API (분류 + 위치)

```bash
curl -X POST "http://localhost:8000/integrated/classify-and-locate" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg" \
     -F "latitude=37.5665" \
     -F "longitude=127.0780"
```

### 7. 스마트 추천

```bash
curl "http://localhost:8000/integrated/smart-recommendation?latitude=37.5665&longitude=127.0780"
```

## API 응답 예시

### 이미지 분류 결과
```json
{
  "filename": "test_image.jpg",
  "predicted_class": "plastic",
  "confidence": 0.9234,
  "is_recyclable": true,
  "class_probabilities": {
    "glass": 0.0234,
    "paper": 0.0123,
    "plastic": 0.9234,
    "metal": 0.0089,
    "trash": 0.0320
  }
}
```

### 통합 API 응답 (분류 + 위치)
```json
{
  "success": true,
  "result": {
    "classification": {
      "filename": "test_image.jpg",
      "predicted_class": "plastic",
      "confidence": 0.9234,
      "is_recyclable": true
    },
    "waste_type_info": {
      "name": "플라스틱",
      "description": "플라스틱 병, 용기 등",
      "recycling_method": "라벨 제거 후 깨끗이 씻어서 배출"
    },
    "nearby_locations": {
      "count": 3,
      "locations": [
        {
          "id": 1,
          "name": "서울시 강남구 분리수거장",
          "address": "서울특별시 강남구 테헤란로 123",
          "distance_km": 0.5,
          "operating_hours": "24시간"
        }
      ]
    }
  }
}
```

## 프로젝트 구조

```
├── app/
│   ├── api/
│   │   ├── base.py             # API 기본 클래스
│   │   ├── controllers/        # 컨트롤러 패턴
│   │   │   ├── recycling_controller.py
│   │   │   ├── location_controller.py
│   │   │   └── integrated_controller.py
│   │   ├── recycling.py        # 분류 API
│   │   ├── location.py         # 위치 기반 API
│   │   ├── integrated.py       # 통합 API
│   │   └── threads.py          # 기존 API
│   ├── core/
│   │   ├── interfaces.py       # 핵심 인터페이스
│   │   ├── factories.py        # 팩토리 패턴
│   │   ├── service_registry.py # 의존성 주입
│   │   ├── data_processor.py   # 데이터 처리기
│   │   └── database.py         # 데이터베이스 설정
│   ├── models/
│   │   ├── recycling_classifier.py  # EfficientNetV2 모델
│   │   ├── location.py          # 위치 모델
│   │   └── chat_log.py         # 기존 모델
│   ├── repositories/
│   │   └── location_repository.py  # 저장소 패턴
│   ├── services/
│   │   ├── inference_service.py     # 추론 서비스
│   │   ├── location_service.py     # 위치 서비스
│   │   └── model_trainer.py         # 모델 훈련
│   └── main.py                 # FastAPI 앱
├── models/                     # 훈련된 모델 저장
├── train_model.py             # 모델 훈련 스크립트
├── test_inference.py          # 추론 테스트 스크립트
├── add_sample_data.py         # 샘플 데이터 추가
└── requirements.txt           # 의존성
```

## 모델 성능 최적화

- **전이학습**: ImageNet 사전 훈련된 EfficientNetV2-S 사용
- **데이터 증강**: 회전, 이동, 확대/축소 등으로 데이터 다양성 증가
- **조기 종료**: 검증 정확도가 개선되지 않으면 훈련 중단
- **학습률 스케줄링**: 검증 손실이 개선되지 않으면 학습률 감소

## 주의사항

1. **GPU 사용**: 훈련 시 GPU 사용을 권장합니다 (CUDA 설치 필요)
2. **메모리**: 대용량 이미지 처리 시 메모리 사용량에 주의하세요
3. **데이터 품질**: 훈련 데이터의 품질이 모델 성능에 직접적인 영향을 미칩니다
4. **모델 크기**: EfficientNetV2-S는 약 22MB의 모델 크기를 가집니다

## 문제 해결

### 모델 로드 실패
- 모델 파일 경로 확인
- TensorFlow 버전 호환성 확인
- 의존성 재설치

### 메모리 부족
- 배치 크기 감소
- 이미지 크기 조정
- GPU 메모리 설정

### 낮은 정확도
- 더 많은 훈련 데이터 수집
- 데이터 전처리 개선
- 하이퍼파라미터 조정
