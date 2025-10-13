#!/usr/bin/env python3
"""
샘플 분리수거 배출 장소 데이터 추가 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, create_tables
from app.services.location_service import LocationService


def add_sample_locations():
    """샘플 배출 장소 데이터 추가"""
    # 테이블 생성
    create_tables()
    
    # 데이터베이스 세션 생성
    db = SessionLocal()
    location_service = LocationService(db)
    
    # 샘플 데이터
    sample_locations = [
        {
            "name": "서울시 강남구 분리수거장",
            "address": "서울특별시 강남구 테헤란로 123",
            "latitude": 37.5665,
            "longitude": 127.0780,
            "waste_types": ["glass", "paper", "plastic", "metal"],
            "operating_hours": "24시간",
            "contact_info": "02-1234-5678",
            "description": "강남구 대표 분리수거장"
        },
        {
            "name": "서울시 서초구 재활용센터",
            "address": "서울특별시 서초구 서초대로 456",
            "latitude": 37.4947,
            "longitude": 127.0276,
            "waste_types": ["glass", "paper", "plastic"],
            "operating_hours": "09:00-18:00",
            "contact_info": "02-2345-6789",
            "description": "서초구 재활용센터"
        },
        {
            "name": "서울시 송파구 쓰레기 배출장",
            "address": "서울특별시 송파구 올림픽로 789",
            "latitude": 37.5145,
            "longitude": 127.1058,
            "waste_types": ["metal", "plastic"],
            "operating_hours": "06:00-22:00",
            "contact_info": "02-3456-7890",
            "description": "송파구 쓰레기 배출장"
        },
        {
            "name": "서울시 마포구 분리수거소",
            "address": "서울특별시 마포구 홍대입구역 101",
            "latitude": 37.5563,
            "longitude": 126.9226,
            "waste_types": ["glass", "paper", "plastic", "metal"],
            "operating_hours": "24시간",
            "contact_info": "02-4567-8901",
            "description": "마포구 분리수거소"
        },
        {
            "name": "서울시 영등포구 재활용센터",
            "address": "서울특별시 영등포구 여의도동 202",
            "latitude": 37.5219,
            "longitude": 126.9242,
            "waste_types": ["paper", "plastic"],
            "operating_hours": "08:00-20:00",
            "contact_info": "02-5678-9012",
            "description": "영등포구 재활용센터"
        },
        {
            "name": "서울시 종로구 분리수거장",
            "address": "서울특별시 종로구 청계천로 303",
            "latitude": 37.5735,
            "longitude": 126.9788,
            "waste_types": ["glass", "metal"],
            "operating_hours": "24시간",
            "contact_info": "02-6789-0123",
            "description": "종로구 분리수거장"
        },
        {
            "name": "서울시 중구 쓰레기 배출소",
            "address": "서울특별시 중구 명동길 404",
            "latitude": 37.5636,
            "longitude": 126.9826,
            "waste_types": ["glass", "paper", "plastic", "metal"],
            "operating_hours": "06:00-24:00",
            "contact_info": "02-7890-1234",
            "description": "중구 쓰레기 배출소"
        },
        {
            "name": "서울시 동대문구 재활용센터",
            "address": "서울특별시 동대문구 회기동 505",
            "latitude": 37.5895,
            "longitude": 127.0563,
            "waste_types": ["paper", "plastic", "metal"],
            "operating_hours": "09:00-18:00",
            "contact_info": "02-8901-2345",
            "description": "동대문구 재활용센터"
        }
    ]
    
    print("샘플 분리수거 배출 장소 데이터를 추가합니다...")
    
    try:
        for location_data in sample_locations:
            location = location_service.add_recycling_location(**location_data)
            print(f"✓ 추가됨: {location['name']}")
        
        print(f"\n총 {len(sample_locations)}개의 샘플 데이터가 추가되었습니다.")
        
    except Exception as e:
        print(f"오류: {e}")
        return 1
    
    finally:
        db.close()
    
    return 0


if __name__ == "__main__":
    exit(add_sample_locations())
