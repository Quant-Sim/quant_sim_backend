from pydantic import BaseModel

class StockBase(BaseModel):
    symbol: str
    name: str
    sector: str = None
    industry: str = None
