# Docker 기반 분리수거 품목 분류 시스템

Docker를 사용한 분리수거 품목 분류 시스템의 배포 및 실행 가이드입니다.

## 🐳 Docker 설정

### 1. Docker 이미지 빌드

```bash
# Docker 이미지 빌드
make build

# 또는 직접 빌드
docker build -t recycling-classifier:latest .
```

### 2. 컨테이너 실행

```bash
# 프로덕션 모드 실행
make run

# 개발 모드 실행 (코드 변경 시 자동 재시작)
make dev

# 또는 docker-compose 사용
docker-compose up -d
```

### 3. 데이터베이스 초기화

```bash
# 샘플 데이터 추가
make init-db

# 또는 직접 실행
docker exec recycling-app python add_sample_data.py
```

### 4. 모델 훈련

```bash
# 훈련 데이터 준비 (data/train/ 디렉토리에 클래스별 폴더 구성)
make train

# 또는 직접 실행
docker exec recycling-app python train_model.py \
    --data_dir /app/data/train \
    --epochs 20 \
    --model_path /app/models/recycling_classifier.h5
```

## 🚀 빠른 시작

### 1. 전체 설정 (한 번에 실행)

```bash
# 1. 이미지 빌드 + 컨테이너 실행 + 데이터베이스 초기화
make setup

# 2. API 테스트
make test
```

### 2. 단계별 설정

```bash
# 1. 이미지 빌드
make build

# 2. 컨테이너 실행
make run

# 3. 데이터베이스 초기화
make init-db

# 4. API 테스트
make test
```

## 📋 사용 가능한 명령어

| 명령어 | 설명 |
|--------|------|
| `make help` | 도움말 표시 |
| `make build` | Docker 이미지 빌드 |
| `make run` | 컨테이너 실행 |
| `make dev` | 개발 모드 실행 |
| `make stop` | 컨테이너 중지 |
| `make clean` | 컨테이너 및 이미지 정리 |
| `make init-db` | 데이터베이스 초기화 |
| `make train` | 모델 훈련 |
| `make test` | API 테스트 |
| `make logs` | 컨테이너 로그 확인 |
| `make shell` | 컨테이너 내부 접속 |

## 🔧 개발 환경

### 개발 모드 실행

```bash
# 코드 변경 시 자동 재시작
make dev
```

### 컨테이너 내부 접속

```bash
# 컨테이너 내부 접속
make shell

# 또는 직접 실행
docker exec -it recycling-app /bin/bash
```

### 로그 확인

```bash
# 실시간 로그 확인
make logs

# 또는 직접 실행
docker-compose logs -f
```

## 📊 모니터링

### 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker ps

# 컨테이너 리소스 사용량 확인
docker stats recycling-app
```

### 헬스체크

```bash
# API 서버 상태 확인
curl http://localhost:8000/recycling/health

# 또는 브라우저에서 확인
open http://localhost:8000/docs
```

## 🗂️ 볼륨 마운트

다음 디렉토리들이 호스트와 마운트됩니다:

- `./models` → `/app/models` (훈련된 모델)
- `./data` → `/app/data` (훈련 데이터)
- `./recycling_app.db` → `/app/recycling_app.db` (데이터베이스)

## 🔄 업데이트

### 코드 변경 시

```bash
# 개발 모드에서는 자동 재시작
make dev

# 프로덕션 모드에서는 재빌드 필요
make stop
make build
make run
```

### 모델 업데이트 시

```bash
# 새 모델 훈련
make train

# 컨테이너 재시작
make stop
make run
```

## 🧹 정리

### 컨테이너 정리

```bash
# 컨테이너 중지 및 정리
make clean
```

### 완전 정리

```bash
# 모든 Docker 리소스 정리
docker system prune -a
```

## 🚨 문제 해결

### 컨테이너가 시작되지 않는 경우

```bash
# 로그 확인
make logs

# 컨테이너 내부 접속하여 디버깅
make shell
```

### 포트 충돌

```bash
# 다른 포트 사용
docker-compose up -d --scale recycling-app=0
docker run -p 8001:8000 recycling-classifier:latest
```

### 메모리 부족

```bash
# Docker 메모리 제한 설정
docker run -m 2g -p 8000:8000 recycling-classifier:latest
```

## 📚 추가 정보

- **API 문서**: http://localhost:8000/docs
- **헬스체크**: http://localhost:8000/recycling/health
- **Docker Compose**: `docker-compose.yml` 참조
- **개발 모드**: `docker-compose.dev.yml` 참조
- **프로덕션 모드**: `docker-compose.prod.yml` 참조
