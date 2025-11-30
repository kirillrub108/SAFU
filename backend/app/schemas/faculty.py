"""Схемы для факультетов."""
from pydantic import BaseModel


class FacultyBase(BaseModel):
    name: str
    active: bool = True


class FacultyCreate(FacultyBase):
    pass


class Faculty(FacultyBase):
    id: int

    class Config:
        from_attributes = True

