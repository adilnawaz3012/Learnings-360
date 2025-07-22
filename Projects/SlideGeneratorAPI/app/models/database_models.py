from sqlalchemy import Column, String, Integer, JSON, DateTime, Boolean
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class PresentationDB(Base):
    __tablename__ = "presentations"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    owner_id = Column(Integer)
    config = Column(JSON)
    status = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    pptx_path = Column(String, nullable=True)
    generation_time = Column(Integer)