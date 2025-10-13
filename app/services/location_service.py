"""
위치 기반 쓰레기 배출 정보 서비스
"""
import math
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.interfaces import ILocationService
from app.models.location import RecyclingLocation, UserLocation
from app.repositories.location_repository import LocationRepository, UserLocationRepository, LocationQueryBuilder


class LocationService(ILocationService):
    """위치 기반 서비스"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.location_repo = LocationRepository(db_session)
        self.user_location_repo = UserLocationRepository(db_session)
        self.query_builder = LocationQueryBuilder(db_session)
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """두 지점 간의 거리 계산 (km)"""
        R = 6371  # 지구 반지름 (km)
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def find_nearby_locations(self, 
                            latitude: float, 
                            longitude: float, 
                            waste_type: str = None,
                            radius_km: float = 5.0,
                            limit: int = 10) -> List[Dict]:
        """
        주변 분리수거 배출 장소 찾기
        
        Args:
            latitude: 사용자 위도
            longitude: 사용자 경도
            waste_type: 찾고자 하는 쓰레기 종류
            radius_km: 검색 반경 (km)
            limit: 최대 결과 수
            
        Returns:
            주변 배출 장소 목록
        """
        # 쿼리 빌더를 사용한 조회
        query = (self.query_builder
                .active_only()
                .within_radius(latitude, longitude, radius_km)
                .order_by_distance(latitude, longitude)
                .limit(limit))
        
        if waste_type:
            query = query.by_waste_type(waste_type)
        
        locations = query.build()
        
        # 거리 계산 및 결과 변환
        nearby_locations = []
        for location in locations:
            distance = self.calculate_distance(
                latitude, longitude, 
                location.latitude, location.longitude
            )
            
            if distance <= radius_km:
                location_dict = location.to_dict()
                location_dict['distance_km'] = round(distance, 2)
                nearby_locations.append(location_dict)
        
        return nearby_locations
    
    def get_location_by_id(self, location_id: int) -> Optional[Dict]:
        """ID로 배출 장소 조회"""
        location = self.location_repo.get_by_id(location_id)
        
        if location and location.is_active:
            return location.to_dict()
        return None
    
    def add_recycling_location(self, 
                             name: str,
                             address: str,
                             latitude: float,
                             longitude: float,
                             waste_types: List[str],
                             operating_hours: str = None,
                             contact_info: str = None,
                             description: str = None) -> Dict:
        """새로운 분리수거 배출 장소 추가"""
        location = RecyclingLocation(
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude,
            waste_types=','.join(waste_types),
            operating_hours=operating_hours,
            contact_info=contact_info,
            description=description
        )
        
        created_location = self.location_repo.create(location)
        return created_location.to_dict()
    
    def update_recycling_location(self, 
                                location_id: int,
                                **kwargs) -> Optional[Dict]:
        """분리수거 배출 장소 정보 수정"""
        # 업데이트할 필드들
        updatable_fields = [
            'name', 'address', 'latitude', 'longitude', 
            'waste_types', 'operating_hours', 'contact_info', 'description'
        ]
        
        # 업데이트 데이터 준비
        update_data = {}
        for field, value in kwargs.items():
            if field in updatable_fields:
                if field == 'waste_types' and isinstance(value, list):
                    update_data[field] = ','.join(value)
                else:
                    update_data[field] = value
        
        update_data['updated_at'] = datetime.utcnow()
        
        updated_location = self.location_repo.update(location_id, update_data)
        return updated_location.to_dict() if updated_location else None
    
    def delete_recycling_location(self, location_id: int) -> bool:
        """분리수거 배출 장소 삭제 (비활성화)"""
        return self.location_repo.delete(location_id)
    
    def save_user_location(self, 
                          latitude: float, 
                          longitude: float,
                          user_id: str = None,
                          address: str = None) -> Dict:
        """사용자 위치 저장"""
        user_location = UserLocation(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            address=address
        )
        
        created_location = self.user_location_repo.create(user_location)
        return created_location.to_dict()
    
    def get_waste_type_info(self) -> Dict:
        """쓰레기 종류별 정보 반환"""
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
