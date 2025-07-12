from pydantic import BaseModel

# OHLCV 데이터 기본 스키마
class OHLCVBase(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float

# DB에서 읽어온 OHLCV 데이터용 스키마
class OHLCV(OHLCVBase):
    id: int
    stock_id: int

    class Config:
        from_attributes = True

# 주식 기본 정보 스키마
class StockBase(BaseModel):
    symbol: str
    name: str

# DB에서 읽어온 주식 정보 스키마
class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True

# 상세 주식 정보 (차트 데이터 포함)
class StockDetail(Stock):
    ohlcv_data: list[OHLCV] = []