from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import crud_order
from app.schemas.order import Order, OrderCreate
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=Order)
async def place_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud_order.create_order(db=db, order=order)

@router.get("/", response_model=List[Order])
async def read_orders(db: AsyncSession = Depends(get_db)):
    return await crud_order.get_orders(db=db)