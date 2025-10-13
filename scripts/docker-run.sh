#!/bin/bash

# Docker 컨테이너 실행 스크립트

set -e

echo "🚀 Docker 컨테이너 실행 시작..."

# 이미지 이름
IMAGE_NAME="recycling-classifier:latest"

# 기존 컨테이너 정리
echo "🧹 기존 컨테이너 정리 중..."
docker stop recycling-app 2>/dev/null || true
docker rm recycling-app 2>/dev/null || true

# 모델 디렉토리 생성
mkdir -p models
mkdir -p data

# Docker 컨테이너 실행
echo "🐳 Docker 컨테이너 실행 중..."
docker run -d \
    --name recycling-app \
    -p 8000:8000 \
    -v $(pwd)/models:/app/models \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/recycling_app.db:/app/recycling_app.db \
    -e DATABASE_URL=sqlite:///./recycling_app.db \
    -e PYTHONPATH=/app \
    --restart unless-stopped \
    ${IMAGE_NAME}

echo "✅ Docker 컨테이너 실행 완료!"
echo "🌐 API 서버: http://localhost:8000"
echo "📚 API 문서: http://localhost:8000/docs"

# 컨테이너 상태 확인
echo ""
echo "📊 컨테이너 상태:"
docker ps | grep recycling-app

echo ""
echo "📋 로그 확인:"
echo "docker logs -f recycling-app"
