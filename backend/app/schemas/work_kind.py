"""Схемы для видов занятий."""
from pydantic import BaseModel


class WorkKindBase(BaseModel):
    name: str
    color_hex: str
    active: bool = True


class WorkKindCreate(WorkKindBase):
    pass


class WorkKind(WorkKindBase):
    id: int

    class Config:
        from_attributes = True

