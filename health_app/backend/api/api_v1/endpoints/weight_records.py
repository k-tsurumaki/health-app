from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from health_app.backend import crud, schemas
from health_app.backend.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.WeightRecordResponse, status_code=201)
async def create_weight_record_endpoint(
    weight_record: schemas.WeightRecordCreate, db: Session = Depends(deps.get_db)
) -> schemas.WeightRecordResponse:
    """体重記録を作成するエンドポイント

    Args:
        weight_record (schemas.WeightRecordCreate): 作成する体重記録の情報
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 体重記録が作成できなかった場合に発生

    Returns:
        schemas.WeightRecordResponse: 作成された体重記録
    """
    created_record = crud.create_weight_record(db, weight_record)
    if created_record:
        return created_record
    raise HTTPException(status_code=400, detail="Weight record could not be created")

@router.get("/", response_model=List[schemas.WeightRecordResponse])
async def read_weight_records(
    user_id: int,
    date: Optional[date] = None,
    db: Session = Depends(deps.get_db)
) -> List[schemas.WeightRecordResponse]:
    """指定したユーザーの体重記録を取得するエンドポイント

    Args:
        user_id (int): 取得したいユーザーのユーザーID
        date (Optional[date], optional): 取得したい体重記録の日付. Defaults to None.
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Returns:
        List[schemas.WeightRecordResponse]: 取得された体重記録
    """
    records = crud.get_weight_records_by_date(db, user_id, date)
    if not records:
        raise HTTPException(status_code=404, detail="No weight records found")
    return records

@router.patch("/{weight_record_id}", response_model=schemas.WeightRecordResponse)
async def update_weight_record(
    weight_record_id: int,
    weight_record: schemas.WeightRecordUpdate,
    db: Session = Depends(deps.get_db)
) -> schemas.WeightRecordResponse:
    """指定した体重記録を更新するエンドポイント

    Args:
        weight_record_id (int): 更新する体重記録のID
        weight_record (schemas.WeightRecordUpdate): 更新内容
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 体重記録が見つからない場合に発生

    Returns:
        schemas.WeightRecordResponse: 更新された体重記録
    """
    existing_record = crud.get_weight_record_by_id(db, weight_record_id)
    if existing_record is None:
        raise HTTPException(status_code=404, detail="Weight record not found")
    updated_record = crud.update_weight_record(db, weight_record_id, weight_record)
    return updated_record

@router.delete("/{weight_record_id}", response_model=schemas.WeightRecordResponse)
async def delete_weight_record(
    weight_record_id: int, db: Session = Depends(deps.get_db)
) -> schemas.WeightRecordResponse:
    """指定した体重記録を削除するエンドポイント

    Args:
        weight_record_id (int): 削除する体重記録のID
        db (Session, optional): DBセッション. Defaults to Depends(deps.get_db).

    Raises:
        HTTPException: 体重記録が見つからない場合に発生

    Returns:
        schemas.WeightRecordResponse: 削除された体重記録
    """
    existing_record = crud.get_weight_record_by_id(db, weight_record_id)
    if existing_record is None:
        raise HTTPException(status_code=404, detail="Weight record not found")
    deleted_record = crud.delete_weight_record(db, weight_record_id)
    return deleted_record
