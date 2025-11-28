"""Схемы для дисциплин."""
from pydantic import BaseModel
from typing import Optional


class DisciplineBase(BaseModel):
    name: str
    short_name: Optional[str] = None
    active: bool = True


class DisciplineCreate(DisciplineBase):
    pass


class Discipline(DisciplineBase):
    id: int

    class Config:
        from_attributes = True

