"""
공공 API 서비스 - 분리수거 배출장소 정보 조회
"""
import httpx
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PublicAPIService:
    """공공 API 서비스"""
    
    def __init__(self):
        self.base_url = "http://apis.data.go.kr"
        self.timeout = 30.0
        
    async def get_waste_facilities(self, 
                                 latitude: float, 
                                 longitude: float, 
                                 radius_km: float = 5.0,
                                 waste_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        공공 API에서 분리수거 배출장소 정보 조회
        
        Args:
            latitude: 위도
            longitude: 경도
            radius_km: 검색 반경 (km)
            waste_type: 쓰레기 종류
            
        Returns:
            배출장소 목록
        """
        try:
            # 실제 공공 API 연동 (예시)
            # 실제로는 공공데이터포털에서 발급받은 API 키 사용
            facilities = await self._fetch_from_public_api(latitude, longitude, radius_km, waste_type)
            
            # 거리 계산 및 정렬
            nearby_facilities = []
            for facility in facilities:
                distance = self._calculate_distance(
                    latitude, longitude,
                    facility.get('latitude', 0),
                    facility.get('longitude', 0)
                )
                
                if distance <= radius_km:
                    facility['distance_km'] = round(distance, 2)
                    nearby_facilities.append(facility)
            
            # 거리순 정렬
            nearby_facilities.sort(key=lambda x: x['distance_km'])
            
            return nearby_facilities
            
        except Exception as e:
            logger.error(f"공공 API 조회 중 오류 발생: {e}")
            return []
    
    async def _fetch_from_public_api(self, 
                                   latitude: float, 
                                   longitude: float, 
                                   radius_km: float,
                                   waste_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """공공 API에서 데이터 조회"""
        
        # 실제 공공 API 연동 예시
        # 환경부 폐기물처리시설 정보 API 사용 예시
        api_url = f"{self.base_url}/B552584/RecycleInfoService/getRecycleInfo"
        
        params = {
            'serviceKey': 'YOUR_API_KEY',  # 실제 API 키로 교체 필요
            'type': 'json',
            'numOfRows': 100,
            'pageNo': 1
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(api_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_api_response(data)
                else:
                    logger.warning(f"공공 API 응답 오류: {response.status_code}")
                    return self._get_sample_data(latitude, longitude, radius_km)
                    
        except Exception as e:
            logger.warning(f"공공 API 호출 실패, 샘플 데이터 사용: {e}")
            return self._get_sample_data(latitude, longitude, radius_km)
    
    def _parse_api_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """API 응답 파싱"""
        try:
            items = data.get('response', {}).get('body', {}).get('items', [])
            facilities = []
            
            for item in items:
                facility = {
                    'id': item.get('id', ''),
                    'name': item.get('name', ''),
                    'address': item.get('address', ''),
                    'latitude': float(item.get('latitude', 0)),
                    'longitude': float(item.get('longitude', 0)),
                    'waste_types': item.get('wasteTypes', '').split(','),
                    'operating_hours': item.get('operatingHours', ''),
                    'contact_info': item.get('contactInfo', ''),
                    'description': item.get('description', ''),
                    'is_active': True,
                    'source': 'public_api'
                }
                facilities.append(facility)
            
            return facilities
            
        except Exception as e:
            logger.error(f"API 응답 파싱 오류: {e}")
            return []
    
    def _get_sample_data(self, latitude: float, longitude: float, radius_km: float) -> List[Dict[str, Any]]:
        """샘플 데이터 반환 (API 연동 실패 시)"""
        # 서울시 주요 분리수거 배출장소 샘플 데이터
        sample_facilities = [
            {
                'id': 'sample_1',
                'name': '강남구 분리수거장',
                'address': '서울특별시 강남구 테헤란로 123',
                'latitude': 37.5665,
                'longitude': 126.9780,
                'waste_types': ['plastic', 'glass', 'paper', 'metal'],
                'operating_hours': '09:00-18:00',
                'contact_info': '02-1234-5678',
                'description': '강남구 대표 분리수거 배출장소',
                'is_active': True,
                'source': 'sample_data'
            },
            {
                'id': 'sample_2',
                'name': '서초구 재활용센터',
                'address': '서울특별시 서초구 서초대로 456',
                'latitude': 37.4947,
                'longitude': 127.0276,
                'waste_types': ['plastic', 'glass', 'paper'],
                'operating_hours': '08:00-20:00',
                'contact_info': '02-2345-6789',
                'description': '서초구 재활용센터',
                'is_active': True,
                'source': 'sample_data'
            },
            {
                'id': 'sample_3',
                'name': '송파구 분리수거장',
                'address': '서울특별시 송파구 올림픽로 789',
                'latitude': 37.5145,
                'longitude': 127.1059,
                'waste_types': ['plastic', 'glass', 'metal'],
                'operating_hours': '10:00-17:00',
                'contact_info': '02-3456-7890',
                'description': '송파구 분리수거 배출장소',
                'is_active': True,
                'source': 'sample_data'
            }
        ]
        
        # 사용자 위치 기준으로 거리 계산하여 반환
        nearby_facilities = []
        for facility in sample_facilities:
            distance = self._calculate_distance(
                latitude, longitude,
                facility['latitude'], facility['longitude']
            )
            
            if distance <= radius_km:
                facility['distance_km'] = round(distance, 2)
                nearby_facilities.append(facility)
        
        return nearby_facilities
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """두 지점 간의 거리 계산 (km)"""
        import math
        
        R = 6371  # 지구 반지름 (km)
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    async def get_waste_type_info(self) -> Dict[str, Any]:
        """쓰레기 종류별 정보 조회"""
        return {
            'glass': {
                'name': '유리',
                'description': '유리병, 유리컵 등',
                'recycling_method': '깨끗이 씻어서 배출',
                'color': '#4A90E2'
            },
            'paper': {
                'name': '종이',
                'description': '신문지, 종이, 골판지 등',
                'recycling_method': '비닐, 테이프 제거 후 배출',
                'color': '#F5A623'
            },
            'plastic': {
                'name': '플라스틱',
                'description': '플라스틱 병, 용기 등',
                'recycling_method': '라벨 제거 후 깨끗이 씻어서 배출',
                'color': '#7ED321'
            },
            'metal': {
                'name': '금속',
                'description': '캔, 철재 등',
                'recycling_method': '내용물 비우고 깨끗이 씻어서 배출',
                'color': '#BD10E0'
            },
            'trash': {
                'name': '일반 쓰레기',
                'description': '재활용 불가능한 쓰레기',
                'recycling_method': '일반 쓰레기로 배출',
                'color': '#B8B8B8'
            }
        }
