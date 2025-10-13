#!/bin/bash

# Docker 이미지 빌드 스크립트

set -e

echo "🐳 Docker 이미지 빌드 시작..."

# 이미지 이름과 태그 설정
IMAGE_NAME="recycling-classifier"
TAG="latest"

# Docker 이미지 빌드
echo "📦 Docker 이미지 빌드 중..."
docker build -t ${IMAGE_NAME}:${TAG} .

echo "✅ Docker 이미지 빌드 완료!"
echo "이미지 이름: ${IMAGE_NAME}:${TAG}"

# 이미지 크기 확인
echo "📊 이미지 정보:"
docker images ${IMAGE_NAME}:${TAG}

echo ""
echo "🚀 실행 방법:"
echo "docker run -p 8000:8000 -v \$(pwd)/models:/app/models ${IMAGE_NAME}:${TAG}"
echo ""
echo "또는 docker-compose 사용:"
echo "docker-compose up -d"
