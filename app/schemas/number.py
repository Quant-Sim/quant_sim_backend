from pydantic import BaseModel
from datetime import datetime

# API 응답으로 클라이언트에게 보낼 데이터의 구조
class RandomNumber(BaseModel):
    id: int
    value: float
    created_at: datetime

    # SQLAlchemy 모델 객체를 Pydantic 모델로 변환할 수 있도록 설정
    class Config:
        from_attributes = True