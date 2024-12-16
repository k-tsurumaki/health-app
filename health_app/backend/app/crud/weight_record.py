from sqlalchemy.orm import Session
from health_app.db import models
from health_app.backend.app import schemas
from typing import List, Optional
from datetime import date, datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

def create_weight_record(db: Session, weight_record: schemas.WeightRecordCreate) -> models.WeightRecord:
    """体重記録を作成する

    Args:
        db (Session): データベースセッション
        weight_record (schemas.WeightRecordCreate): 作成する体重記録の情報

    Returns:
        models.WeightRecord: 作成された体重記録のモデル
    """
    db_weight_record = models.WeightRecord(**weight_record.model_dump())
    db.add(db_weight_record)
    db.commit()
    db.refresh(db_weight_record)
    return db_weight_record

def get_weight_records_by_date(db: Session, user_id: int, date: Optional[date] = None) -> List[models.WeightRecord]:
    """指定したユーザーの体重記録を取得する。日付が指定されている場合、その日の記録を返す。

    Args:
        db (Session): データベースセッション
        user_id (int): 対象ユーザーのID
        date (Optional[date]): 体重記録を取得する日付 (デフォルトはNone)

    Returns:
        List[models.WeightRecord]: 指定された条件に一致する体重記録の一覧
    """
    query = db.query(models.WeightRecord).filter(models.WeightRecord.user_id == user_id)

    if date:
        start_of_day = datetime(date.year, date.month, date.day, tzinfo=JST)
        end_of_day = start_of_day + timedelta(days=1)
        query = query.filter(models.WeightRecord.date_time >= start_of_day, models.WeightRecord.date_time < end_of_day)

    weight_records = query.all()
    return weight_records

def get_weight_record_by_id(db: Session, record_id: int) -> models.WeightRecord:
    """指定された体重記録IDの体重記録を取得する

    Args:
        db (Session): データベースセッション
        record_id (int): 体重記録ID

    Returns:
        models.WeightRecord: 指定された体重記録
    """
    return db.query(models.WeightRecord).filter(models.WeightRecord.id == record_id).first()

def update_weight_record(db: Session, record_id: int, weight_record: schemas.WeightRecordUpdate) -> models.WeightRecord:
    """体重記録を更新する

    Args:
        db (Session): データベースセッション
        record_id (int): 更新する体重記録のID
        weight_record (schemas.WeightRecordUpdate): 更新する体重記録の情報

    Returns:
        models.WeightRecord: 更新された体重記録のモデル
    """
    db_weight_record = db.query(models.WeightRecord).filter(models.WeightRecord.id == record_id).first()
    for key, value in weight_record.model_dump().items():
        if value is not None:
            setattr(db_weight_record, key, value)
    db.commit()
    db.refresh(db_weight_record)
    return db_weight_record

def delete_weight_record(db: Session, record_id: int) -> models.WeightRecord:
    """体重記録を削除する

    Args:
        db (Session): データベースセッション
        record_id (int): 削除する体重記録のID

    Returns:
        models.WeightRecord: 削除された体重記録のモデル
    """
    db_weight_record = db.query(models.WeightRecord).filter(models.WeightRecord.id == record_id).first()
    db.delete(db_weight_record)
    db.commit()
    return db_weight_record
