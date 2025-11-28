"""API для поиска."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Dict, Any
from app.db.session import get_db
from app.models import Lecturer, Discipline, Room, Building

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
def search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    """Поиск по ФИО, дисциплине, аудитории, адресу, корпусу."""
    query_lower = q.lower()

    results: Dict[str, List[Dict[str, Any]]] = {
        "lecturers": [],
        "disciplines": [],
        "rooms": [],
        "buildings": [],
    }

    # Поиск преподавателей
    lecturers = (
        db.query(Lecturer)
        .filter(Lecturer.fio.ilike(f"%{q}%"), Lecturer.active == True)
        .limit(10)
        .all()
    )
    results["lecturers"] = [{"id": l.id, "fio": l.fio, "chair": l.chair} for l in lecturers]

    # Поиск дисциплин
    disciplines = (
        db.query(Discipline)
        .filter(
            or_(
                Discipline.name.ilike(f"%{q}%"),
                Discipline.short_name.ilike(f"%{q}%"),
            ),
            Discipline.active == True,
        )
        .limit(10)
        .all()
    )
    results["disciplines"] = [
        {"id": d.id, "name": d.name, "short_name": d.short_name} for d in disciplines
    ]

    # Поиск аудиторий
    rooms = (
        db.query(Room)
        .filter(Room.number.ilike(f"%{q}%"), Room.active == True)
        .limit(10)
        .all()
    )
    results["rooms"] = [
        {
            "id": r.id,
            "number": r.number,
            "building": {"id": r.building.id, "name": r.building.name} if r.building else None,
        }
        for r in rooms
    ]

    # Поиск корпусов
    buildings = (
        db.query(Building)
        .filter(
            or_(
                Building.name.ilike(f"%{q}%"),
                Building.address.ilike(f"%{q}%"),
                Building.code.ilike(f"%{q}%"),
            )
        )
        .limit(10)
        .all()
    )
    results["buildings"] = [
        {
            "id": b.id,
            "name": b.name,
            "code": b.code,
            "address": b.address,
        }
        for b in buildings
    ]

    return results

