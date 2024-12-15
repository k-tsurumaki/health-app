from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
    

@router.get("/")
async def read_users():
    return {"message": "This is an empty endpoint"}