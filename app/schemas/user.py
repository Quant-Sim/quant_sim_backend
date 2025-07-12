from pydantic import BaseModel, EmailStr

# --- 기본 User 스키마 ---
class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None

# --- 회원가입 시 받을 데이터 ---
class UserCreate(UserBase):
    password: str

# --- DB에서 읽어온 데이터 (비밀번호 포함) ---
class UserInDB(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True

# --- API 응답으로 클라이언트에게 보낼 데이터 (비밀번호 제외) ---
class User(UserBase):
    id: int

    class Config:
        from_attributes = True