from typing import Optional, Literal
from datetime import date
from pydantic import BaseModel

GenderType = Literal["man", "woman"]

class UserBase(BaseModel):
    username: str
    email: str
    gender: GenderType
    date_of_birth: date
    height_cm: float

class UserCreate(UserBase):
    username: Optional[str] = "default_name"  # デフォルト値を許可
    password: str  # 新規作成時はパスワードが必須

class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}  # 属性から生成可能

class UserUpdate(UserBase):
    password: str 
