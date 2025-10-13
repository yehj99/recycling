"""
데이터베이스 설정
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 데이터베이스 URL 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recycling_app.db")

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스
Base = declarative_base()


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """테이블 생성"""
    # 모든 모델의 Base를 import하여 테이블 생성
    from app.models.location import Base as LocationBase
    from app.models.chat_log import Base as ChatLogBase
    
    # 모든 테이블 생성
    LocationBase.metadata.create_all(bind=engine)
    ChatLogBase.metadata.create_all(bind=engine)
