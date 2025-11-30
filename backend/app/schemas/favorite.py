"""Схемы для избранного."""
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class FavoriteBase(BaseModel):
    name: str
    filters: Dict[str, Any]


class FavoriteCreate(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

