from passlib.context import CryptContext
from sqlalchemy.orm import Session
from health_app.db import models
from health_app.backend.app import schemas
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """ユーザーを作成する

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


def get_users(db: Session) -> List[models.User]:
    """ユーザーの一覧を取得する

    Args:
        db (Session): データベースセッション

    Returns:
        List[models.User]: 取得されたユーザーモデルの一覧
    """
    return db.query(models.User).all()


def get_user_by_uid(db:Session, user_id: int) -> models.User:
    """ユーザーIDで指定したユーザーを取得する

    Args:
        db (Session): データベースセッション
        user_id (int): 取得したいユーザーのユーザーIDID

    Returns:
        models.User: 取得されたユーザーのモデル
    """
    return db.query(models.User).filter(models.User.id == user_id).first()