from pydantic import BaseModel
from datetime import datetime
from app.db.models import OrderType

# 주문 생성을 위한 스키마 (클라이언트 -> 서버)
class OrderCreate(BaseModel):
    stock_id: int
    order_type: OrderType
    quantity: float
    price: float # 지정가 주문을 위해 가격 필드 추가

# DB에서 읽어온 주문 내역용 스키마 (서버 -> 클라이언트)
class Order(BaseModel):
    id: int
    stock_id: int
    order_type: OrderType
    quantity: float
    price: float
    timestamp: datetime

    class Config:
        from_attributes = True