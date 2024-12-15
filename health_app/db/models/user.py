from datetime import datetime, timezone, timedelta
from health_app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Date, Float, TIMESTAMP
from sqlalchemy.orm import relationship

JST = timezone(timedelta(hours=9))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    height_cm = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(JST))
    updated_at = Column(TIMESTAMP, default=lambda: datetime.now(JST), onupdate=lambda: datetime.now(JST))

    # リレーションシップ
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan") # userが削除されると関連するmealが自動的に削除される
    weight_records = relationship("WeightRecord", back_populates="user", cascade="all, delete-orphan")
