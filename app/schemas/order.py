from pydantic import BaseModel

class OrderBase(BaseModel):
    type: str
    price: float
    quantity: float

class OrderCreate(OrderBase):
    user_id: int
    symbol: str
    pass

class Order(OrderBase):
    id: int
    user_id: int
    symbol: str
    timestamp: str
    time: int
    total: float

    class Config:
        from_attributes = True