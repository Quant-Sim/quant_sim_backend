from sqlalchemy.orm import Session
from app.db import models

def get_stocks(db: Session, skip: int = 0, limit: int = 100):
    """모든 주식 목록을 조회합니다."""
    return db.query(models.Stock).offset(skip).limit(limit).all()

def get_stock_by_symbol(db: Session, symbol: str):
    """심볼로 특정 주식의 상세 정보(OHLCV 데이터 포함)를 조회합니다."""
    return db.query(models.Stock).filter(models.Stock.symbol == symbol).first()