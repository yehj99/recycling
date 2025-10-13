from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.threads import router as threads_router
from app.api.recycling import router as recycling_router
from app.api.location import router as location_router
from app.api.integrated import router as integrated_router
from app.core.database import create_tables
from app.core.service_registry import register_services

app = FastAPI(
    title="분리수거 품목 분류 API",
    description="EfficientNetV2를 사용한 분리수거 품목 분류 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 테이블 생성
create_tables()

# 서비스 등록
register_services()

# 라우터 등록
app.include_router(threads_router)
app.include_router(recycling_router)
app.include_router(location_router)
app.include_router(integrated_router)