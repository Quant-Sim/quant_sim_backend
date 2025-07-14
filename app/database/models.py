from sqlalchemy import Column, Integer, String, Float, BigInteger, Boolean, JSON
from .base import Base

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(BigInteger, unique=True, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    color = Column(String, nullable=False)

class OrderHistory(Base):
    __tablename__ = "order_history"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, nullable=False)
    time = Column(BigInteger, nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # 요청하신 추가 필드들
    balance = Column(Float, nullable=False, default=100000000.0)
    invested_money = Column(Float, nullable=False, default=0.0)

    # JSON 타입을 사용하여 List[Stock]과 같은 복잡한 구조를 저장합니다.
    # 기본값으로 빈 리스트와 빈 딕셔너리를 설정합니다.
    stocks = Column(JSON, nullable=False, default=[])
    portfolio = Column(JSON, nullable=False, default={})