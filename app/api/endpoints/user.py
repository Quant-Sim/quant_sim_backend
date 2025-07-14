from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import user as user_schema
from typing import List
from app.crud import crud_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def create_new_user(
        user: user_schema.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    새로운 사용자를 생성합니다.

    - **username**: 사용자 아이디 (필수)
    - **email**: 사용자 이메일 (필수)
    - **password**: 사용자 비밀번호 (필수)
    - **full_name**: 사용자 전체 이름 (선택)
    """
    db_user = await crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    return await crud_user.create_user(db=db, user=user)


@router.get("/", response_model=List[user_schema.User])
async def read_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    등록된 사용자 목록을 조회합니다.
    """
    users = await crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_schema.User)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    특정 ID를 가진 사용자의 정보를 조회합니다.
    """
    db_user = await crud_user.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return db_user