from pydantic import BaseModel
from typing import List, Dict, Any


# 프론트엔드에서 사용하는 Stock 데이터 구조에 대한 스키마
class Stock(BaseModel):
    name: str
    symbol: str
    price: float
    quantity: float
    total: str
    change: str
    color: str
    chartColor: str
    points: str


# 프론트엔드에서 사용하는 Portfolio의 각 데이터 포인트에 대한 스키마
class PortfolioDataPoint(BaseModel):
    name: str
    value: float


# 기본 사용자 정보 (공통 속성)
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str


# 사용자 생성을 위한 스키마 (비밀번호 포함)
class UserCreate(UserBase):
    password: str


# 데이터베이스에서 읽어올 사용자 정보 스키마 (API 응답 모델)
class User(UserBase):
    id: int
    is_active: bool = True
    balance: float  # 잔액
    invested_money: float  # 투자 원금

    # 프론트엔드 데이터 구조에 맞춘 필드
    stocks: List[Stock] = []
    portfolio: Dict[str, List[PortfolioDataPoint]] = {
        '1D': [],
        '5D': [],
        '1M': [],
        '6M': [],
        '1Y': [],
        'Max': [],
    }

    class Config:
        # Pydantic v2 이상에서는 from_attributes = True 사용
        from_attributes = True
