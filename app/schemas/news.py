from pydantic import BaseModel

class News(BaseModel):
    id: str
    headline: str
    sentiment: float
    impact: int
    timestamp: int