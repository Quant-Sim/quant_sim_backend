from pydantic import BaseModel

class PriceBase(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float

class VolumeBase(BaseModel):
    time: int
    value: int
    color: str

class PriceUpdate(BaseModel):
    candle: PriceBase
    volume: VolumeBase
    initial: bool = False