from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# 수정된 import 구문: 이제 app.database에서 직접 가져올 수 있습니다.
from app.database import Base, engine
from app.api.endpoints import websocket, orders

async def create_db_and_tables():
    """서버 시작 시 데이터베이스에 모든 테이블을 생성합니다."""
    async with engine.begin() as conn:
        # Base.metadata는 models.py에 정의된 모든 테이블 정보를 담고 있습니다.
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 실제 프로덕션에서는 특정 도메인만 허용하세요.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 연결
app.include_router(orders.router, prefix="/api/order")
# websocket.py의 router를 최상위 경로에 연결합니다.
# 이렇게 하면 /ws 로 접속할 수 있습니다.
app.include_router(websocket.router)

@app.on_event("startup")
async def on_startup():
    # 서버 시작 시 DB 테이블 생성
    await create_db_and_tables()
    # 백그라운드에서 가격 생성기 실행
    asyncio.create_task(websocket.price_generator())