from fastapi import APIRouter

from app.api.v1.endpoints import stocks, orders
from endpoints import auth, numbers # 1. numbers를 임포트합니다.

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(numbers.router, prefix="/numbers", tags=["numbers"]) # 2. numbers 라우터를 추가합니다.
api_router.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])