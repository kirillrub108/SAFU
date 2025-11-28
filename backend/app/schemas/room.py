"""Схемы для аудиторий."""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class RoomBase(BaseModel):
    building_id: int
    number: str
    capacity: int
    type: str
    features: Optional[Dict[str, Any]] = None
    active: bool = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    building_id: Optional[int] = None
    number: Optional[str] = None
    capacity: Optional[int] = None
    type: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    active: Optional[bool] = None


class Room(RoomBase):
    id: int

    class Config:
        from_attributes = True

