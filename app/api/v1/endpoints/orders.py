from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# --- 1. 필요한 모듈만 명확하게 가져옵니다. ---

# 데이터베이스 세션을 가져오기 위한 함수
from app.db.database import get_db

# 인증된 사용자 정보를 가져오기 위한 함수
# 이 함수 내부에 토큰 검증 로직이 모두 포함되어 있습니다.
from app.core.security import get_current_active_user

# 데이터베이스 CRUD(생성, 읽기, 업데이트, 삭제) 로직을 담고 있는 함수
from app.crud import crud_order

# API 요청/응답 데이터 형식을 정의하는 스키마
from app.schemas import order as order_schema
from app.schemas import user as user_schema
from app.db import models # current_user의 타입을 명시하기 위해 추가

# --- 2. API 라우터를 생성합니다. ---
router = APIRouter()


# --- 3. 주문 생성 엔드포인트를 정의합니다. ---
@router.post("/", response_model=order_schema.Order)
def create_new_order(
        # 클라이언트가 요청 본문에 보낸 주문 정보 (JSON)
        # FastAPI가 자동으로 JSON을 order_schema.OrderCreate 객체로 변환해줍니다.
        order: order_schema.OrderCreate,

        # 데이터베이스 세션을 주입받는 부분입니다.
        # get_db 함수가 실행되고, 그 결과(db 세션)가 db 변수에 담깁니다.
        db: Session = Depends(get_db),

        # 현재 로그인한 사용자 정보를 주입받는 부분입니다.
        # get_current_active_user 함수가 실행되어 토큰을 검증하고,
        # 그 결과(user 모델 객체)가 current_user 변수에 담깁니다.
        # 토큰이 없거나 유효하지 않으면, 이 함수가 알아서 401 오류를 발생시킵니다.
        current_user: models.User = Depends(get_current_active_user)
):
    """
    새로운 매수 또는 매도 주문을 생성합니다.

    - **인증**: 요청 헤더에 유효한 JWT 토큰이 반드시 포함되어야 합니다.
    - **요청**: 매수/매도할 주식의 ID, 종류, 수량, 가격을 JSON으로 전달해야 합니다.
    - **응답**: 성공적으로 생성된 주문의 상세 정보를 반환합니다.
    """
    # 실제 비즈니스 로직은 crud_order.py의 함수에 위임합니다.
    # 이렇게 하면 API 엔드포인트 코드가 깔끔하게 유지됩니다.
    return crud_order.create_order(db=db, order=order, user_id=current_user.id)
