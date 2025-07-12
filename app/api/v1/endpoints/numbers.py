from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import number as number_schema
from app.crud import crud_number

# --- 수정된 부분 ---
# 잘못된 'app.api.deps' 대신, auth.py와 동일한 방식으로 get_db를 가져옵니다.
from app.db.database import get_db
# --------------------

router = APIRouter()

@router.get("/", response_model=List[number_schema.RandomNumber])
def read_random_numbers(
        # --- 수정된 부분 ---
        # Depends(deps.get_db)가 아닌, Depends(get_db)를 사용합니다.
        db: Session = Depends(get_db),
        # --------------------
        skip: int = 0,
        limit: int = 100,
):
    """
    저장된 난수 목록을 조회합니다.
    """
    numbers = crud_number.get_random_numbers(db, skip=skip, limit=limit)
    return numbers