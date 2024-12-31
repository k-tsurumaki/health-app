from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from health_app.backend import (
    crud, 
    schemas,
)

from health_app.backend.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.MealResponse, status_code=201)
async def create_meal_endpoint(
    meal: schemas.MealCreate, db: Session = Depends(deps.get_db)
) -> schemas.MealResponse:
    """食事を作成するエンドポイント

    Args:
        meal (schemas.MealCreate): 作成する食事の情報
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 食事が作成出来なかった場合に発生

    Returns:
        schemas.MealResponse: 作成された食事の情報
    """
    created_meal = crud.create_meal(db, meal)
    if created_meal:
        return created_meal
    raise HTTPException(status_code=400, detail="Meal could not be created") 

@router.get("/", response_model=List[schemas.MealResponse])
async def read_meals(
    user_id: int,
    date: Optional[date] = None,
    meal_type: Optional[schemas.MealType] = None,
    db: Session = Depends(deps.get_db),
) -> List[schemas.MealResponse]:
    """指定したユーザーの食事を取得するエンドポイント

    Args:
        user_id (int): 取得したいユーザーのユーザーID
        date (Optional[date], optional): 取得したい食事の日付. Defaults to None.
        meal_type (Optional[schemas.MealType], optional): 取得したい食事の種類. Defaults to None.
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 食事が取得できなかった場合に発生

    Returns:
        List[schemas.MealResponse]: 取得された食事
    """
    meals = crud.get_meals_by_date_and_meal_type(db, user_id, date, meal_type)
    if meals is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meals

@router.patch("/{meal_id}", response_model=schemas.MealResponse)
async def update_meal(
    meal_id: int,
    meal: schemas.MealUpdate,
    db: Session = Depends(deps.get_db)
) -> schemas.MealResponse:
    """指定した食事を更新するエンドポイント

    Args:
        meal_id (int): _description_
        meal (schemas.MealUpdate): _description_
        db (Session, optional): _description_. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: _description_

    Returns:
        schemas.MealResponse: _description_
    """
    existing_meal = crud.get_meal_by_mid(db, meal_id)
    if existing_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    updated_meal = crud.update_meal(db, meal_id, meal)
    return updated_meal
    
@router.delete("/{meal_id}", response_model=schemas.MealResponse)
async def delete_meal(meal_id: int, db: Session = Depends(deps.get_db)) -> schemas.MealResponse:
    """指定した食事を削除するエンドポイント

    Args:
        meal_id (int): 削除したい食事の食事ID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 食事が取得できなかった場合に発生

    Returns:
        schemas.UserResponse: 削除された食事
    """
    existing_meal = crud.get_meal_by_mid(db, meal_id)
    if existing_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    deleted_meal = crud.delete_meal(db, meal_id)
    return deleted_meal