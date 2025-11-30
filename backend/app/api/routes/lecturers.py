"""API для преподавателей."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Lecturer, LecturerCreate, LecturerUpdate
from app.models import Lecturer as LecturerModel

router = APIRouter(prefix="/api/lecturers", tags=["lecturers"])


@router.get("", response_model=List[Lecturer])
def get_lecturers(db: Session = Depends(get_db)):
    """Получить список преподавателей."""
    return db.query(LecturerModel).filter(LecturerModel.active == True).all()


@router.get("/chairs")
def get_chairs(db: Session = Depends(get_db)):
    """Получить список кафедр."""
    chairs = (
        db.query(LecturerModel.chair)
        .filter(LecturerModel.chair.isnot(None), LecturerModel.active == True)
        .distinct()
        .all()
    )
    return {"chairs": [chair[0] for chair in chairs if chair[0]]}


@router.post("", response_model=Lecturer)
def create_lecturer(lecturer: LecturerCreate, db: Session = Depends(get_db)):
    """Создать преподавателя."""
    db_lecturer = LecturerModel(**lecturer.model_dump())
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer


@router.get("/{lecturer_id}", response_model=Lecturer)
def get_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    """Получить преподавателя по ID."""
    return db.query(LecturerModel).filter(LecturerModel.id == lecturer_id).first()

