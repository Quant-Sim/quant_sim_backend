from pydantic import BaseModel

class OrderBase(BaseModel):
    type: str
    price: float
    quantity: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    timestamp: str
    time: int
    total: float

    class Config:
        from_attributes = True