from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.chat_log import ChatLog

router = APIRouter()

@router.get("/api/threads")
def get_threads(db: Session = Depends(get_db)):
    threads = db.query(ChatLog).all()
    return threads