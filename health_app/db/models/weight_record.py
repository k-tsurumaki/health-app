from datetime import datetime, timezone, timedelta
from datetime import datetime
from health_app.db.base_class import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# JST = timezone(timedelta(hours=9))

class WeightRecord(Base):
    __tablename__ = "weight_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ユーザーID
    weight = Column(Float, nullable=False)  # 体重
    date_time = Column(DateTime, default=lambda: datetime.now(), nullable=False)  # 体重測定日時
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    
    user = relationship("User", back_populates="weight_records")  # ユーザーとのリレーションシップ

