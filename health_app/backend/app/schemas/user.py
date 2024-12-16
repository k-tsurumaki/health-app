from typing import Optional
from datetime import date
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: Optional[str] = "default_name"
    email: str
    password: str
    gender: str
    date_of_birth: date
    height_cm: float

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    gender: str
    date_of_birth: date
    height_cm: float

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    gender: str
    date_of_birth: date
    height_cm: float
