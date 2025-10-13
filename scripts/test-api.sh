#!/bin/bash

# API 테스트 스크립트

set -e

echo "🧪 API 테스트 시작..."

# API 서버 상태 확인
echo "1. 서비스 상태 확인..."
curl -s http://localhost:8000/recycling/health | jq '.' || echo "❌ API 서버에 연결할 수 없습니다."

echo ""
echo "2. 클래스 정보 조회..."
curl -s http://localhost:8000/recycling/classes | jq '.' || echo "❌ 클래스 정보를 가져올 수 없습니다."

echo ""
echo "3. 쓰레기 종류 정보 조회..."
curl -s http://localhost:8000/location/waste-types/info | jq '.' || echo "❌ 쓰레기 종류 정보를 가져올 수 없습니다."

echo ""
echo "4. 주변 배출 장소 조회 (서울 강남구)..."
curl -s "http://localhost:8000/location/nearby?latitude=37.5665&longitude=127.0780&waste_type=plastic" | jq '.' || echo "❌ 주변 배출 장소를 조회할 수 없습니다."

echo ""
echo "5. 스마트 추천..."
curl -s "http://localhost:8000/integrated/smart-recommendation?latitude=37.5665&longitude=127.0780" | jq '.' || echo "❌ 스마트 추천을 조회할 수 없습니다."

echo ""
echo "✅ API 테스트 완료!"
echo "🌐 API 문서: http://localhost:8000/docs"
