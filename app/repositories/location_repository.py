"""
위치 관련 저장소 패턴 구현
"""
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.core.interfaces import IRepository
from app.models.location import RecyclingLocation, UserLocation


class LocationRepository(IRepository):
    """위치 저장소 구현"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create(self, entity: Any) -> Any:
        """엔티티 생성"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[Any]:
        """ID로 엔티티 조회"""
        return self.db.query(RecyclingLocation).filter(
            RecyclingLocation.id == entity_id
        ).first()
    
    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[Any]:
        """엔티티 업데이트"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """엔티티 삭제 (소프트 삭제)"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        
        entity.is_active = False
        self.db.commit()
        return True
    
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[Any]:
        """조건에 따른 엔티티 조회"""
        query = self.db.query(RecyclingLocation)
        
        if 'is_active' in criteria:
            query = query.filter(RecyclingLocation.is_active == criteria['is_active'])
        
        if 'waste_type' in criteria:
            query = query.filter(RecyclingLocation.waste_types.contains(criteria['waste_type']))
        
        if 'name' in criteria:
            query = query.filter(RecyclingLocation.name.contains(criteria['name']))
        
        return query.all()


class UserLocationRepository(IRepository):
    """사용자 위치 저장소 구현"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create(self, entity: Any) -> Any:
        """엔티티 생성"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[Any]:
        """ID로 엔티티 조회"""
        return self.db.query(UserLocation).filter(
            UserLocation.id == entity_id
        ).first()
    
    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[Any]:
        """엔티티 업데이트"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """엔티티 삭제"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        
        self.db.delete(entity)
        self.db.commit()
        return True
    
    def find_by_criteria(self, criteria: Dict[str, Any]) -> List[Any]:
        """조건에 따른 엔티티 조회"""
        query = self.db.query(UserLocation)
        
        if 'user_id' in criteria:
            query = query.filter(UserLocation.user_id == criteria['user_id'])
        
        if 'latitude' in criteria and 'longitude' in criteria:
            # 위치 기반 조회 (반경 내)
            lat = criteria['latitude']
            lon = criteria['longitude']
            radius = criteria.get('radius', 1.0)  # 기본 1km
            
            # 간단한 반경 계산 (실제로는 더 정확한 계산 필요)
            query = query.filter(
                and_(
                    UserLocation.latitude.between(lat - radius, lat + radius),
                    UserLocation.longitude.between(lon - radius, lon + radius)
                )
            )
        
        return query.all()


class LocationQueryBuilder:
    """위치 쿼리 빌더"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.query = db_session.query(RecyclingLocation)
    
    def active_only(self):
        """활성 상태만 조회"""
        self.query = self.query.filter(RecyclingLocation.is_active == True)
        return self
    
    def by_waste_type(self, waste_type: str):
        """쓰레기 종류별 조회"""
        self.query = self.query.filter(RecyclingLocation.waste_types.contains(waste_type))
        return self
    
    def by_name(self, name: str):
        """이름으로 조회"""
        self.query = self.query.filter(RecyclingLocation.name.contains(name))
        return self
    
    def within_radius(self, latitude: float, longitude: float, radius_km: float):
        """반경 내 조회"""
        # 실제 구현에서는 더 정확한 거리 계산 필요
        lat_range = radius_km / 111.0  # 대략적인 위도 1도 = 111km
        lon_range = radius_km / (111.0 * abs(latitude) / 90.0)  # 경도는 위도에 따라 다름
        
        self.query = self.query.filter(
            and_(
                RecyclingLocation.latitude.between(latitude - lat_range, latitude + lat_range),
                RecyclingLocation.longitude.between(longitude - lon_range, longitude + lon_range)
            )
        )
        return self
    
    def order_by_distance(self, latitude: float, longitude: float):
        """거리순 정렬"""
        # 실제 구현에서는 더 정확한 거리 계산 필요
        self.query = self.query.order_by(
            (RecyclingLocation.latitude - latitude).label('lat_diff'),
            (RecyclingLocation.longitude - longitude).label('lon_diff')
        )
        return self
    
    def limit(self, count: int):
        """결과 수 제한"""
        self.query = self.query.limit(count)
        return self
    
    def build(self) -> List[RecyclingLocation]:
        """쿼리 실행"""
        return self.query.all()
