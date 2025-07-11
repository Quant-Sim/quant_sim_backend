import random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models

def generate_and_store_random_number():
    """
    1. 0과 1000 사이의 난수를 생성합니다.
    2. 새로운 데이터베이스 세션을 열어 난수를 저장합니다.
    3. 세션을 닫습니다.
    """
    db: Session = SessionLocal()
    try:
        random_value = random.randint(0, 1000)
        db_number = models.RandomNumber(value=random_value)
        db.add(db_number)
        db.commit()
        # 터미널에서 실시간으로 확인하기 위한 print문
        print(f"[{db_number.created_at}] Stored new random number: {random_value}")
    finally:
        db.close()