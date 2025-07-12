from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import stock as stock_schema
from app.crud import crud_stock
from app.db.database import get_db # get_db를 직접 가져옵니다.

router = APIRouter()

@router.get("/", response_model=List[stock_schema.Stock])
def read_stocks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    stocks = crud_stock.get_stocks(db, skip=skip, limit=limit)
    return stocks

@router.get("/{symbol}", response_model=stock_schema.StockDetail)
def read_stock_detail(symbol: str, db: Session = Depends(get_db)):
    db_stock = crud_stock.get_stock_by_symbol(db, symbol=symbol)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock