from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db import models
from app.db.database import engine
from app.api.v1.endpoints import auth
from app.services.scheduler import generate_and_store_random_number

# 데이터베이스 테이블 생성
# (이미 테이블이 존재하면 아무 작업도 하지 않음)
models.Base.metadata.create_all(bind=engine)

# 비동기 스케줄러 생성
scheduler = AsyncIOScheduler()

app = FastAPI(
    title="My Stock Trading App API",
    description="API for user authentication and scheduled tasks.",
    version="0.1.0",
)

@app.on_event("startup")
def startup_event():
    """
    FastAPI 앱이 시작될 때 스케줄러를 시작합니다.
    """
    # 'generate_and_store_random_number' 함수를 1초 간격으로 실행하도록 추가
    scheduler.add_job(generate_and_store_random_number, 'interval', seconds=1, id="random_number_job")
    scheduler.start()
    print("Scheduler started... Will generate a random number every second.")

@app.on_event("shutdown")
def shutdown_event():
    """
    FastAPI 앱이 종료될 때 스케줄러를 종료합니다.
    """
    scheduler.shutdown()
    print("Scheduler shut down.")

app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend!"}