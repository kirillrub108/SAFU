"""API для видов занятий."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import WorkKind, WorkKindCreate
from app.models import WorkKind as WorkKindModel

router = APIRouter(prefix="/api/work-kinds", tags=["work-kinds"])


@router.get("", response_model=List[WorkKind])
def get_work_kinds(db: Session = Depends(get_db)):
    """Получить список видов занятий."""
    return db.query(WorkKindModel).filter(WorkKindModel.active == True).all()


@router.post("", response_model=WorkKind)
def create_work_kind(work_kind: WorkKindCreate, db: Session = Depends(get_db)):
    """Создать вид занятия."""
    db_work_kind = WorkKindModel(**work_kind.model_dump())
    db.add(db_work_kind)
    db.commit()
    db.refresh(db_work_kind)
    return db_work_kind


@router.get("/{work_kind_id}", response_model=WorkKind)
def get_work_kind(work_kind_id: int, db: Session = Depends(get_db)):
    """Получить вид занятия по ID."""
    return db.query(WorkKindModel).filter(WorkKindModel.id == work_kind_id).first()

