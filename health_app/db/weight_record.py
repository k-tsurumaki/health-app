from datetime import datetime, timezone, timedelta
from datetime import datetime
from health_app.db.base_class import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

JST = timezone(timedelta(hours=9))

class WeightRecord(Base):
    __tablename__ = "weight_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ユーザーID
    weight = Column(Float, nullable=False)  # 体重
    date_time = Column(DateTime, default=datetime.now, nullable=False)  # 体重測定日時
    
    user = relationship("User", back_populates="weight_records")  # ユーザーとのリレーションシップ

    created_at = Column(DateTime, default=datetime.now(JST))
    updated_at = Column(DateTime, default=datetime.now(JST), onupdate=datetime.now(JST))
