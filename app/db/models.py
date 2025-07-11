from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class User(Base):
    """사용자 정보 저장을 위한 테이블 모델"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)

class RandomNumber(Base):
    """난수를 저장하기 위한 테이블 모델"""
    __tablename__ = "random_numbers"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())