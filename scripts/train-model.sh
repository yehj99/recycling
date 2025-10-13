#!/bin/bash

# Docker 컨테이너에서 모델 훈련 스크립트

set -e

echo "🤖 모델 훈련 시작..."

# 컨테이너가 실행 중인지 확인
if ! docker ps | grep -q recycling-app; then
    echo "❌ recycling-app 컨테이너가 실행 중이 아닙니다."
    echo "먼저 docker-compose up -d 또는 scripts/docker-run.sh를 실행하세요."
    exit 1
fi

# 데이터 디렉토리 확인
if [ ! -d "data/train" ]; then
    echo "❌ 훈련 데이터 디렉토리가 없습니다: data/train"
    echo "다음 구조로 데이터를 준비하세요:"
    echo "data/train/"
    echo "├── glass/"
    echo "├── paper/"
    echo "├── plastic/"
    echo "├── metal/"
    echo "└── trash/"
    exit 1
fi

# 모델 훈련 실행
echo "🏋️ 모델 훈련 중..."
docker exec recycling-app python train_model.py \
    --data_dir /app/data/train \
    --epochs 20 \
    --model_path /app/models/recycling_classifier.h5

echo "✅ 모델 훈련 완료!"
echo "📁 모델 저장 위치: models/recycling_classifier.h5"
