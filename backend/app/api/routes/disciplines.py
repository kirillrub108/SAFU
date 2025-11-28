"""API для дисциплин."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Discipline, DisciplineCreate
from app.models import Discipline as DisciplineModel

router = APIRouter(prefix="/api/disciplines", tags=["disciplines"])


@router.get("", response_model=List[Discipline])
def get_disciplines(db: Session = Depends(get_db)):
    """Получить список дисциплин."""
    return db.query(DisciplineModel).filter(DisciplineModel.active == True).all()


@router.post("", response_model=Discipline)
def create_discipline(discipline: DisciplineCreate, db: Session = Depends(get_db)):
    """Создать дисциплину."""
    db_discipline = DisciplineModel(**discipline.model_dump())
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline


@router.get("/{discipline_id}", response_model=Discipline)
def get_discipline(discipline_id: int, db: Session = Depends(get_db)):
    """Получить дисциплину по ID."""
    return db.query(DisciplineModel).filter(DisciplineModel.id == discipline_id).first()

