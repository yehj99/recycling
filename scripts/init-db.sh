#!/bin/bash

# 데이터베이스 초기화 스크립트

set -e

echo "🗄️ 데이터베이스 초기화 시작..."

# 컨테이너가 실행 중인지 확인
if ! docker ps | grep -q recycling-app; then
    echo "❌ recycling-app 컨테이너가 실행 중이 아닙니다."
    echo "먼저 docker-compose up -d 또는 scripts/docker-run.sh를 실행하세요."
    exit 1
fi

# 샘플 데이터 추가
echo "📊 샘플 데이터 추가 중..."
docker exec recycling-app python add_sample_data.py

echo "✅ 데이터베이스 초기화 완료!"
echo "🌐 API 서버: http://localhost:8000"
echo "📚 API 문서: http://localhost:8000/docs"
