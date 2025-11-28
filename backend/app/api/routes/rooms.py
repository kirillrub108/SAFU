"""API для аудиторий."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Room, RoomCreate, RoomUpdate
from app.models import Room as RoomModel

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@router.get("", response_model=List[Room])
def get_rooms(db: Session = Depends(get_db)):
    """Получить список аудиторий."""
    return db.query(RoomModel).all()


@router.post("", response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """Создать аудиторию."""
    db_room = RoomModel(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@router.get("/{room_id}", response_model=Room)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Получить аудиторию по ID."""
    return db.query(RoomModel).filter(RoomModel.id == room_id).first()

