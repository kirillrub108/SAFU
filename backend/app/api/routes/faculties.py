"""API для факультетов."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Faculty, FacultyCreate
from app.models import Faculty as FacultyModel

router = APIRouter(prefix="/api/faculties", tags=["faculties"])


@router.get("", response_model=List[Faculty])
def get_faculties(db: Session = Depends(get_db)):
    """Получить список факультетов."""
    return db.query(FacultyModel).filter(FacultyModel.active == True).all()


@router.post("", response_model=Faculty)
def create_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    """Создать факультет."""
    db_faculty = FacultyModel(**faculty.model_dump())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


@router.get("/{faculty_id}", response_model=Faculty)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    """Получить факультет по ID."""
    return db.query(FacultyModel).filter(FacultyModel.id == faculty_id).first()

