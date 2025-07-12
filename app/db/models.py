from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.db.database import Base  # .database에서 Base를 가져오는 것으로 가정합니다.


# --- 1. 사용자 (User) ---
# 기존 User 모델에 '현금 잔고'와 '포트폴리오', '주문 내역' 관계를 추가합니다.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    # 추가된 필드: 사용자의 현금 보유액 (초기값 1억)
    cash_balance = Column(Float, nullable=False, default=100000000)

    # 관계 설정
    portfolios = relationship("Portfolio", back_populates="owner")
    orders = relationship("Order", back_populates="owner")


# --- 2. 주식 (Stock) ---
# 거래 가능한 모든 주식의 목록과 정보를 저장합니다.
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    # Ticker, 예: "AAPL", "TSLA", "BTC-KRW"
    symbol = Column(String, unique=True, index=True, nullable=False)
    # 이름, 예: "Apple Inc.", "Tesla, Inc.", "비트코인"
    name = Column(String, nullable=False)

    # 관계 설정
    ohlcv_data = relationship("OHLCV", back_populates="stock")
    portfolios = relationship("Portfolio", back_populates="stock")
    orders = relationship("Order", back_populates="stock")


# --- 3. 시가/고가/저가/종가/거래량 (OHLCV) ---
# 차트에 표시될 모든 주식의 과거 데이터입니다.
class OHLCV(Base):
    __tablename__ = "ohlcv"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)

    time = Column(Integer, nullable=False, index=True)  # Unix 타임스탬프
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    # 관계 설정
    stock = relationship("Stock", back_populates="ohlcv_data")


# --- 4. 포트폴리오 (Portfolio) ---
# 사용자가 어떤 주식을 얼마나 보유하고 있는지 나타냅니다.
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)

    # 보유 수량
    quantity = Column(Float, nullable=False, default=0)
    # 평균 매수 단가
    average_buy_price = Column(Float, nullable=False, default=0)

    # 관계 설정
    owner = relationship("User", back_populates="portfolios")
    stock = relationship("Stock", back_populates="portfolios")


# --- 5. 주문 (Order) ---
# 사용자의 모든 매수/매도 기록을 저장합니다.
class OrderType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)

    order_type = Column(Enum(OrderType), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)  # 체결 가격
    timestamp = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    owner = relationship("User", back_populates="orders")
    stock = relationship("Stock", back_populates="orders")


class RandomNumber(Base):
    __tablename__ = "random_numbers"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
