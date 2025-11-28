"""Схемы для временных слотов."""
from pydantic import BaseModel
from datetime import date, time


class TimeSlotBase(BaseModel):
    date: date
    pair_number: int
    time_start: time
    time_end: time
    timezone: str = "Europe/Moscow"


class TimeSlotCreate(TimeSlotBase):
    pass


class TimeSlot(TimeSlotBase):
    id: int

    class Config:
        from_attributes = True

