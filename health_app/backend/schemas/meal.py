from datetime import date
from pydantic import BaseModel
from enum import Enum

# MealType = Literal["breakfast", "lunch", "dinner", "other"]
class MealType(Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    OTHER = "other"


class MealBase(BaseModel):
    user_id: int
    meal_type: MealType
    meal_name: str
    calories: float
    date: date


class MealCreate(MealBase):
    pass


class MealResponse(MealBase):
    id: int
    model_config = {"from_attributes": True}


class MealUpdate(MealBase):
    pass