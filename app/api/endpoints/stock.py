from fastapi import APIRouter, Depends, Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_stock
from app.database.session import get_db

router = APIRouter()

@router.get("/list", response_model=List[str])
async def stock_list(db: AsyncSession = Depends(get_db)):
    return await crud_stock.get_stock_list(db=db)

@router.post("/init")
async def initialize_stocks(db: AsyncSession = Depends(get_db)):
    await crud_stock.insert_initial_stocks(db)
    return {"message": "Stocks inserted"}
