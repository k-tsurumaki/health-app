from sqlalchemy.orm import Session
from health_app.db import models
from health_app.backend import schemas
from typing import List, Optional
from datetime import date, datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

def create_meal(db: Session, meal: schemas.MealCreate) -> models.Meal:
    """食事を作成する

    Args:
        db (Session): データベースセッション
        meal (schemas.MealCreate): 作成する食事の情報

    Returns:
        models.Meal: 作成された食事のモデル
    """
    db_meal = models.Meal(**meal.model_dump())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def get_meals_by_date_and_meal_type(db:Session, user_id:int, date: Optional[date]=None, meal_type:Optional[schemas.MealType]=None) -> List[models.Meal]:
    """指定したユーザーの食事を取得する。日付や食事の種類が指定されている場合、それに応じた食事を返す

    Args:
        db (Session): データベースセッション
        user_id (int): 対象ユーザーのID
        date (Optional[date]): 食事を取得する日付 (デフォルトはNone)
        meal_type (Optional[date]): 食事を取得する日付 (デフォルトはNone)

    Returns:
        List[models.Meal]: 指定された条件に一致する食事の一覧
    """
    query = db.query(models.Meal).filter(models.Meal.user_id==user_id)

    if date:
        start_of_day = datetime(date.year, date.month, date.day, tzinfo=JST)
        end_of_day = start_of_day + timedelta(days=1)
        query = query.filter(models.Meal.date_time >= start_of_day, models.Meal.date_time < end_of_day)

    if meal_type:
        query = query.filter(models.Meal.meal_type==meal_type)
    
    meals = query.all()
    return meals

def get_meal_by_mid(db:Session, meal_id: int) -> models.Meal:
    return db.query(models.Meal).filter(models.Meal.id==meal_id).first()


def update_meal(db:Session, meal_id: int, meal: schemas.MealUpdate) -> models.Meal:
    """食事情報を更新する

    Args:
        db (Session): データベースセッション
        meal_id (int): 更新する食事の食事ID 
        meal (schemas.MealUpdate): 更新する食事の食事情報

    Returns:
        models.Meal: 更新された食事のモデル
    """
    db_meal = db.query(models.Meal).filter(models.Meal.id==meal_id).first()
    for key, value in meal.model_dump().items():
        setattr(db_meal, key, value)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def delete_meal(db: Session, meal_id: int) -> models.Meal:
    """食事IDで指定した食事を削除する

    Args:
        db (Session): データベースセッション
        meal_id (int): 削除したい食事の食事ID

    Returns:
        models.Meal: 削除した食事のモデル
    """
    db_meal = db.query(models.Meal).filter(models.Meal.id==meal_id).first()
    db.delete(db_meal)
    db.commit()
    return db_meal
