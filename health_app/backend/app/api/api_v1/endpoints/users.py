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
    raise HTTPException(status_code=400, detail="User could not be created")
    

@router.get("/", response_model=List[schemas.UserResponse])
async def read_users(db: Session = Depends(deps.get_db)) -> List[schemas.UserResponse]:
    """ユーザー一覧を取得するエンドポイント

    Args:
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).
        
    Raises:
        HTTPException: ユーザーが取得できなかった場合に発生

    Returns:
        List[schemas.UserResponse]: 取得されたユーザーの一覧
    """
    users = crud.get_users(db)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: Session = Depends(deps.get_db)) -> schemas.UserResponse:
    """指定したユーザーを取得するエンドポイント

    Args:
        user_id (int): 取得したいユーザーのユーザーID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: ユーザーが取得できなかった場合に発生

    Returns:
        schemas.UserResponse: 取得されたユーザー
    """
    user = crud.get_user_by_uid(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(deps.get_db)) -> schemas.UserResponse:
    """指定したユーザーを更新するエンドポイント

    Args:
        user_id (int): 更新したいユーザーのユーザーID
        user (schemas.UserUpdate): 更新するユーザーの情報
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: ユーザーが取得できなかった場合に発生

    Returns:
        schemas.UserResponse: 更新されたユーザー
    """
    existing_user = crud.get_user_by_uid(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud.update_user(db, user_id, user)
    return updated_user


@router.delete("/{user_id}", response_model=schemas.UserResponse)
async def delete_user(user_id: int, db: Session = Depends(deps.get_db)) -> schemas.UserResponse:
    """指定したユーザーを削除するエンドポイント

    Args:
        user_id (int): 削除したいユーザーのユーザーID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: ユーザーが取得できなかった場合に発生

    Returns:
        schemas.UserResponse: 削除されたユーザー
    """
    existing_user = crud.get_user_by_uid(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = crud.delete_user(db, user_id)
    return deleted_user