from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
from app.schemas.user import UserCreate
from app.security import get_password_hash

async def create_user(db: AsyncSession, user: UserCreate):
    """
    새로운 사용자를 데이터베이스에 생성합니다.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
        # balance, invested_money, stocks, portfolio는 모델에서 정의한 기본값으로 생성됩니다.
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id(db: AsyncSession, user_id: int):
    """
    ID로 특정 사용자를 조회합니다.
    """
    query = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    """
    이메일 주소로 특정 사용자를 조회합니다.
    """
    query = select(models.User).filter(models.User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    await db.refresh(user)
    return user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    데이터베이스에서 사용자 목록을 조회합니다.
    """
    query = select(models.User).order_by(models.User.id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()