from typing import Optional
from datetime import date
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, Float, TIMESTAMP

class UserCreate(BaseModel):
    username: Optional[str] = "default_name"
    email: str
    password: str
    gender: str
    date_of_birth: date
    height_cm: float
    

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    gender: str
    date_of_birth: date
    height_cm: float

    model_config = {"from_attributes": True}
