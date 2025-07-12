from pydantic import BaseModel, EmailStr
from app.schemas.portfolio import Portfolio # 포트폴리오 스키마를 가져옵니다.
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

# 사용자 생성을 위한 스키마 (클라이언트 -> 서버)
class UserCreate(BaseModel):
    email: str
    password: str
    username: str

# DB에서 읽어온 기본 사용자 정보 (다른 모델에서 사용될 수 있음)
class User(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True

# '내 정보' 조회 시 사용할 상세 스키마 (서버 -> 클라이언트)
class UserMe(User):
    cash_balance: float
    portfolios: list[Portfolio] = []

    class Config:
        from_attributes = True