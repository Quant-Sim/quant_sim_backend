from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(settings.DATABASE_URL)

# 비동기 세션 메이커
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# API 요청마다 DB 세션을 주입해주는 비동기 의존성 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session