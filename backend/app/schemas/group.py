"""Схемы для групп и подгрупп."""
from pydantic import BaseModel
from typing import Optional


class GroupBase(BaseModel):
    code: str
    name: str
    year: Optional[int] = None
    active: bool = True


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True


class SubgroupBase(BaseModel):
    group_id: int
    code: str
    active: bool = True


class SubgroupCreate(SubgroupBase):
    pass


class Subgroup(SubgroupBase):
    id: int

    class Config:
        from_attributes = True

