# Docker 기반 분리수거 품목 분류 시스템 Makefile

.PHONY: help build run stop clean dev test init-db train logs

# 기본 타겟
help:
	@echo "🐳 Docker 기반 분리수거 품목 분류 시스템"
	@echo ""
	@echo "사용 가능한 명령어:"
	@echo "  build      - Docker 이미지 빌드"
	@echo "  run        - 컨테이너 실행"
	@echo "  dev        - 개발 모드 실행 (코드 변경 시 자동 재시작)"
	@echo "  stop       - 컨테이너 중지"
	@echo "  clean      - 컨테이너 및 이미지 정리"
	@echo "  init-db    - 데이터베이스 초기화 (샘플 데이터 추가)"
	@echo "  train      - 모델 훈련"
	@echo "  test      - API 테스트"
	@echo "  logs       - 컨테이너 로그 확인"
	@echo "  shell      - 컨테이너 내부 접속"
	@echo ""

# Docker 이미지 빌드
build:
	@echo "🐳 Docker 이미지 빌드 중..."
	docker build -t recycling-classifier:latest .
	@echo "✅ 빌드 완료!"

# 컨테이너 실행
run:
	@echo "🚀 컨테이너 실행 중..."
	docker-compose up -d
	@echo "✅ 컨테이너 실행 완료!"
	@echo "🌐 API 서버: http://localhost:8000"
	@echo "📚 API 문서: http://localhost:8000/docs"

# 개발 모드 실행
dev:
	@echo "🔧 개발 모드 실행 중..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ 개발 모드 실행 완료!"
	@echo "🌐 API 서버: http://localhost:8000"
	@echo "📚 API 문서: http://localhost:8000/docs"

# 컨테이너 중지
stop:
	@echo "🛑 컨테이너 중지 중..."
	docker-compose down
	@echo "✅ 컨테이너 중지 완료!"

# 정리
clean:
	@echo "🧹 정리 중..."
	docker-compose down -v
	docker rmi recycling-classifier:latest 2>/dev/null || true
	docker system prune -f
	@echo "✅ 정리 완료!"

# 데이터베이스 초기화
init-db:
	@echo "🗄️ 데이터베이스 초기화 중..."
	@if ! docker ps | grep -q recycling-app; then \
		echo "❌ 컨테이너가 실행 중이 아닙니다. 먼저 'make run'을 실행하세요."; \
		exit 1; \
	fi
	docker exec recycling-app python add_sample_data.py
	@echo "✅ 데이터베이스 초기화 완료!"

# 모델 훈련
train:
	@echo "🤖 모델 훈련 중..."
	@if ! docker ps | grep -q recycling-app; then \
		echo "❌ 컨테이너가 실행 중이 아닙니다. 먼저 'make run'을 실행하세요."; \
		exit 1; \
	fi
	@if [ ! -d "data/train" ]; then \
		echo "❌ 훈련 데이터가 없습니다. data/train 디렉토리에 데이터를 준비하세요."; \
		exit 1; \
	fi
	docker exec recycling-app python train_model.py \
		--data_dir /app/data/train \
		--epochs 20 \
		--model_path /app/models/recycling_classifier.h5
	@echo "✅ 모델 훈련 완료!"

# API 테스트
test:
	@echo "🧪 API 테스트 중..."
	@if ! docker ps | grep -q recycling-app; then \
		echo "❌ 컨테이너가 실행 중이 아닙니다. 먼저 'make run'을 실행하세요."; \
		exit 1; \
	fi
	@if ! command -v jq >/dev/null 2>&1; then \
		echo "❌ jq가 설치되지 않았습니다. 'brew install jq' 또는 'apt-get install jq'를 실행하세요."; \
		exit 1; \
	fi
	@echo "1. 서비스 상태 확인..."
	@curl -s http://localhost:8000/recycling/health | jq '.' || echo "❌ API 서버에 연결할 수 없습니다."
	@echo ""
	@echo "2. 클래스 정보 조회..."
	@curl -s http://localhost:8000/recycling/classes | jq '.' || echo "❌ 클래스 정보를 가져올 수 없습니다."
	@echo ""
	@echo "3. 주변 배출 장소 조회..."
	@curl -s "http://localhost:8000/location/nearby?latitude=37.5665&longitude=127.0780&waste_type=plastic" | jq '.' || echo "❌ 주변 배출 장소를 조회할 수 없습니다."
	@echo ""
	@echo "✅ API 테스트 완료!"

# 로그 확인
logs:
	@echo "📋 컨테이너 로그 확인 중..."
	docker-compose logs -f

# 컨테이너 내부 접속
shell:
	@echo "🐚 컨테이너 내부 접속 중..."
	docker exec -it recycling-app /bin/bash

# 전체 설정
setup: build run init-db
	@echo "🎉 전체 설정 완료!"
	@echo "🌐 API 서버: http://localhost:8000"
	@echo "📚 API 문서: http://localhost:8000/docs"
