"""Схемы для преподавателей."""
from pydantic import BaseModel
from typing import Optional


class LecturerBase(BaseModel):
    fio: str
    chair: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    active: bool = True


class LecturerCreate(LecturerBase):
    pass


class LecturerUpdate(BaseModel):
    fio: Optional[str] = None
    chair: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    active: Optional[bool] = None


class Lecturer(LecturerBase):
    id: int

    class Config:
        from_attributes = True

