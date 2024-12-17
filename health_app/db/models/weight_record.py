from datetime import datetime, date, timezone, timedelta
from health_app.db.base_class import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# JST = timezone(timedelta(hours=9))


class WeightRecord(Base):
    __tablename__ = "weight_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(Date, default=lambda: date.today(), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(
        DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()
    )

    user = relationship("User", back_populates="weight_records")
