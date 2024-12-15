from passlib.context import CryptContext
from sqlalchemy.orm import Session
from health_app.db import models
from health_app.backend.app import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """ユーザーを作成するCRUD操作

    Args:
        db (Session): データベースセッション
        user (schemas.UserCreate): 作成するユーザーの情報

    Returns:
        UserModel: 作成されたユーザーのモデル
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        gender=user.gender,
        date_of_birth=user.date_of_birth,
        height_cm=user.height_cm,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    