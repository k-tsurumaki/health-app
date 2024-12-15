from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from health_app.backend.app import (
    crud,
    schemas,
)

from health_app.backend.app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse, status_code=201)
async def create_user_endpoint(
    user: schemas.UserCreate, db: Session = Depends(deps.get_db)
) -> schemas.UserResponse:
    """ユーザーを作成するエンドポイント

    Args:
        user (schemas.UserCreate): 作成するユーザーの情報
        db (Session, optional): DBセッション. Defaults to Depends(get_db).

    Raises:
        HTTPException: ユーザーが作成できなかった場合に発生

    Returns:
        UserResponse: 作成されたユーザーの情報
    """
    created_user = crud.create_user(db, user)
    if created_user:
        return created_user
    else:
        raise HTTPException(status_code=400, detail="User could not be created")
    

@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(db: Session = Depends(deps.get_db)) -> List[schemas.UserResponse]:
    """ユーザー一覧を取得するエンドポイント

    Args:
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        List[schemas.UserResponse]: 取得されたユーザーの一覧
    """
    users = crud.get_users(db)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: Session = Depends(deps.get_db)) -> schemas.UserResponse:
    """指定したユーザーを取得するエンドポイント

    Args:
        user_id (int): 取得したいユーザーのユーザーID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        schemas.UserResponse: 取得されたユーザー
    """
    user = crud.get_user_by_uid(db, user_id)
    return user