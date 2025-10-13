"""
위치 기반 쓰레기 배출 정보 모델
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Dict, Optional

Base = declarative_base()


class RecyclingLocation(Base):
    """분리수거 배출 장소 모델"""
    __tablename__ = "recycling_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="배출 장소명")
    address = Column(String(500), nullable=False, comment="주소")
    latitude = Column(Float, nullable=False, comment="위도")
    longitude = Column(Float, nullable=False, comment="경도")
    waste_types = Column(String(200), nullable=False, comment="수거 가능한 쓰레기 종류 (comma separated)")
    operating_hours = Column(String(100), nullable=True, comment="운영 시간")
    contact_info = Column(String(100), nullable=True, comment="연락처")
    description = Column(Text, nullable=True, comment="설명")
    is_active = Column(Boolean, default=True, comment="활성 상태")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'waste_types': self.waste_types.split(',') if self.waste_types else [],
            'operating_hours': self.operating_hours,
            'contact_info': self.contact_info,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserLocation(Base):
    """사용자 위치 기록 모델"""
    __tablename__ = "user_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=True, comment="사용자 ID (선택사항)")
    latitude = Column(Float, nullable=False, comment="위도")
    longitude = Column(Float, nullable=False, comment="경도")
    address = Column(String(500), nullable=True, comment="주소")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
