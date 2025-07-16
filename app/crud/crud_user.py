from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import models
from app.schemas.user import UserCreate, PortfolioDataPoint
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
        full_name=user.full_name,
        portfolio= {
            {
                '1D': [
                    PortfolioDataPoint(name='10 am', value=0),
                    PortfolioDataPoint(name='11 am', value=0),
                    PortfolioDataPoint(name='12 pm', value=0),
                    PortfolioDataPoint(name='01 pm', value=0),
                    PortfolioDataPoint(name='02 pm', value=0),
                    PortfolioDataPoint(name='03 pm', value=0),
                    PortfolioDataPoint(name='04 pm', value=0),
                ],
                '5D': [
                    PortfolioDataPoint(name='Mon', value=0),
                    PortfolioDataPoint(name='Tue', value=0),
                    PortfolioDataPoint(name='Wed', value=0),
                    PortfolioDataPoint(name='Thu', value=0),
                    PortfolioDataPoint(name='Fri', value=0),
                ],
                '1M': [
                    PortfolioDataPoint(name='Week 1', value=0),
                    PortfolioDataPoint(name='Week 2', value=0),
                    PortfolioDataPoint(name='Week 3', value=0),
                    PortfolioDataPoint(name='Week 4', value=0),
                ],
                '6M': [
                    PortfolioDataPoint(name='Jan', value=0),
                    PortfolioDataPoint(name='Feb', value=0),
                    PortfolioDataPoint(name='Mar', value=0),
                    PortfolioDataPoint(name='Apr', value=0),
                    PortfolioDataPoint(name='May', value=0),
                    PortfolioDataPoint(name='Jun', value=0),
                ],
                '1Y': [
                    PortfolioDataPoint(name='2024 Q1', value=0),
                    PortfolioDataPoint(name='2024 Q2', value=0),
                    PortfolioDataPoint(name='2024 Q3', value=0),
                    PortfolioDataPoint(name='2024 Q4', value=0),
                ],
                'Max': [
                    PortfolioDataPoint(name='2022', value=0),
                    PortfolioDataPoint(name='2023', value=0),
                    PortfolioDataPoint(name='2024', value=0),
                    PortfolioDataPoint(name='2025', value=0),
                ],
            }

        }
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