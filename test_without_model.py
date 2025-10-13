#!/usr/bin/env python3
"""
모델 없이 API 테스트 스크립트
실제 모델이 없어도 API 구조와 응답 형식을 테스트할 수 있습니다.
"""

import requests
import json
import os
import sys
from typing import Dict, Any

def test_api_without_model():
    """모델 없이 API 테스트"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("모델 없이 API 테스트")
    print("=" * 60)
    
    # 1. 서비스 상태 확인
    print("\n1. 서비스 상태 확인...")
    try:
        response = requests.get(f"{base_url}/recycling/health")
        if response.status_code == 200:
            print("✅ 서비스가 정상적으로 실행 중입니다.")
            print(f"응답: {response.json()}")
        else:
            print(f"❌ 서비스 상태 확인 실패: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        print("서버 실행 명령: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False
    
    # 2. 클래스 정보 확인
    print("\n2. 클래스 정보 확인...")
    try:
        response = requests.get(f"{base_url}/recycling/classes")
        if response.status_code == 200:
            print("✅ 클래스 정보를 성공적으로 가져왔습니다.")
            print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 클래스 정보 가져오기 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 클래스 정보 확인 중 오류: {e}")
    
    # 3. 더미 이미지로 분류 테스트 (실패 예상)
    print("\n3. 더미 이미지로 분류 테스트...")
    
    # 간단한 더미 이미지 생성 (1x1 픽셀)
    dummy_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    try:
        files = {'file': ('dummy.png', dummy_image_data, 'image/png')}
        response = requests.post(f"{base_url}/recycling/classify", files=files)
        
        print(f"응답 상태 코드: {response.status_code}")
        print(f"응답 내용: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print("✅ 예상대로 모델이 없어서 오류가 발생했습니다.")
                print(f"오류 메시지: {result['error']}")
            else:
                print("⚠️  예상과 다르게 분류가 성공했습니다.")
        else:
            print(f"❌ 요청 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 분류 테스트 중 오류: {e}")
    
    # 4. 위치 기반 API 테스트
    print("\n4. 위치 기반 API 테스트...")
    try:
        response = requests.get(
            f"{base_url}/location/nearby",
            params={
                'latitude': 37.5665,
                'longitude': 127.0780,
                'waste_type': 'plastic'
            }
        )
        
        if response.status_code == 200:
            print("✅ 위치 기반 API가 정상적으로 작동합니다.")
            print(f"응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 위치 기반 API 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 위치 기반 API 테스트 중 오류: {e}")
    
    # 5. 통합 API 테스트
    print("\n5. 통합 API 테스트...")
    try:
        files = {'file': ('dummy.png', dummy_image_data, 'image/png')}
        data = {
            'latitude': 37.5665,
            'longitude': 127.0780
        }
        
        response = requests.post(
            f"{base_url}/integrated/classify-and-locate",
            files=files,
            data=data
        )
        
        print(f"응답 상태 코드: {response.status_code}")
        print(f"응답 내용: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and 'error' in result.get('result', {}).get('classification', {}):
                print("✅ 통합 API에서 모델 없음을 올바르게 처리했습니다.")
            else:
                print("⚠️  통합 API 응답이 예상과 다릅니다.")
        else:
            print(f"❌ 통합 API 요청 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 통합 API 테스트 중 오류: {e}")
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)
    print("모델을 생성하려면 다음 명령을 실행하세요:")
    print("python create_pretrained_model.py")
    print("\n그 후 다시 테스트하면 실제 분류 결과를 볼 수 있습니다.")
    
    return True

def main():
    """메인 함수"""
    return test_api_without_model()

if __name__ == "__main__":
    exit(0 if main() else 1)
