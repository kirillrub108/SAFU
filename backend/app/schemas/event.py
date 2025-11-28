"""Схемы для событий."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time


class EventLecturer(BaseModel):
    lecturer_id: int

    class Config:
        from_attributes = True


class EventGroup(BaseModel):
    group_id: int

    class Config:
        from_attributes = True


class EventSubgroup(BaseModel):
    subgroup_id: int

    class Config:
        from_attributes = True


class EventStream(BaseModel):
    stream_id: int

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    discipline_id: int
    work_kind_id: int
    room_id: int
    time_slot_id: int
    status: str = "scheduled"
    note: Optional[str] = None


class EventCreate(EventBase):
    lecturer_ids: List[int] = []
    group_ids: List[int] = []
    subgroup_ids: List[int] = []
    stream_ids: List[int] = []
    reason: Optional[str] = None  # Для ChangeLog


class EventUpdate(BaseModel):
    discipline_id: Optional[int] = None
    work_kind_id: Optional[int] = None
    room_id: Optional[int] = None
    time_slot_id: Optional[int] = None
    status: Optional[str] = None
    note: Optional[str] = None
    lecturer_ids: Optional[List[int]] = None
    group_ids: Optional[List[int]] = None
    subgroup_ids: Optional[List[int]] = None
    stream_ids: Optional[List[int]] = None
    reason: Optional[str] = None  # Для ChangeLog


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class EventDetail(Event):
    """Детальная информация о событии с связанными объектами."""
    discipline: Optional[dict] = None
    work_kind: Optional[dict] = None
    room: Optional[dict] = None
    time_slot: Optional[dict] = None
    lecturers: List[dict] = []
    groups: List[dict] = []
    subgroups: List[dict] = []
    streams: List[dict] = []

    class Config:
        from_attributes = True

