from sqlalchemy.orm import Session
from health_app.db import models
from health_app.backend.app import schemas

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """ユーザーを作成するCRUD操作

    Args:
        db (Session): データベースセッション
        user (schemas.UserCreate): 作成するユーザーの情報

    Returns:
        UserModel: 作成されたユーザーのモデル
    """
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    