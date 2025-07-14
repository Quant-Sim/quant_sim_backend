from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import crud_order
from app.schemas.order import Order, OrderCreate
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=Order)
async def place_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud_order.create_order(db=db, order=order)

@router.get("/{symbol}", response_model=List[Order])
async def read_orders(db: AsyncSession = Depends(get_db), symbol: str = Path(...)):
    return await crud_order.get_orders(db=db, symbol=symbol)

@router.get("/{symbol}/user/{user_id}", response_model=List[Order])
async def read_user_orders(db: AsyncSession = Depends(get_db), symbol: str = Path(...), user_id: int = Path(...)):
    return await crud_order.get_user_orders(db=db, symbol=symbol, user_id=user_id)