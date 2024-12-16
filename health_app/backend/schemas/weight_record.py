from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class WeightRecordBase(BaseModel):
    user_id: int
    weight: float
    date_time: datetime

class WeightRecordCreate(WeightRecordBase):
    pass

class WeightRecordResponse(WeightRecordBase):
    id: int

    model_config = {"from_attributes": True}

class WeightRecordUpdate(BaseModel):
    weight: Optional[float] = None
    date_time: Optional[datetime] = None
