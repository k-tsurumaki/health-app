from datetime import date
from pydantic import BaseModel
from typing import Optional


class WeightRecordBase(BaseModel):
    user_id: int
    weight: float
    date: date


class WeightRecordCreate(WeightRecordBase):
    pass


class WeightRecordResponse(WeightRecordBase):
    model_config = {"from_attributes": True}


class WeightRecordUpdate(BaseModel):
    pass
