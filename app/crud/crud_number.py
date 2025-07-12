from sqlalchemy.orm import Session
from app.db import models

def get_random_numbers(db: Session, skip: int = 0, limit: int = 100):
    """
    데이터베이스에서 난수 목록을 조회합니다.
    최신 데이터가 먼저 오도록 정렬합니다.
    """
    return db.query(models.RandomNumber).order_by(models.RandomNumber.created_at.desc()).offset(skip).limit(limit).all()