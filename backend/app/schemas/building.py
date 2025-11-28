"""Схемы для корпусов."""
from pydantic import BaseModel
from typing import Optional


class BuildingBase(BaseModel):
    name: str
    code: Optional[str] = None
    address: str
    lat: Optional[float] = None
    lon: Optional[float] = None


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class Building(BuildingBase):
    id: int

    class Config:
        from_attributes = True

