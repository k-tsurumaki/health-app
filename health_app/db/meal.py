from datetime import datetime, timezone, timedelta
from datetime import datetime
from health_app.db.base_class import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

JST = timezone(timedelta(hours=9))

class Meal(Base):
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    meal_type = Column(String(50), nullable=False)  # 食事の種類（例：朝食、昼食、夕食、間食）
    meal_name = Column(String(50), nullable=False)
    calories = Column(Float, nullable=False)  
    date_time = Column(DateTime, default=datetime.now, nullable=False) 
    
    user = relationship("User", back_populates="meals")  # ユーザーとのリレーションシップ
    
    created_at = Column(DateTime, default=datetime.now(JST))
    updated_at = Column(DateTime, default=datetime.now(JST), onupdate=datetime.now(JST))
