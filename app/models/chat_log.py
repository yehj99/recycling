from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chat_log"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, index=True)
    user = Column(String, index=True)
    message = Column(Text)
    created_at = Column(DateTime)