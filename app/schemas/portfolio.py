from pydantic import BaseModel
from app.schemas.stock import Stock # 연관된 스키마를 가져옵니다.

# 포트폴리오 항목 스키마
class Portfolio(BaseModel):
    id: int
    stock_id: int
    quantity: float
    average_buy_price: float
    stock: Stock # 보유 주식의 상세 정보 포함

    class Config:
        from_attributes = True