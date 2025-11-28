"""Схемы для журнала изменений."""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ChangeLog(BaseModel):
    id: int
    entity: str
    entity_id: int
    actor: Optional[str] = None
    change_at: datetime
    reason: Optional[str] = None
    diff_before: Optional[Dict[str, Any]] = None
    diff_after: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True


class ChangeLogFilter(BaseModel):
    entity: Optional[str] = None
    entity_id: Optional[int] = None
    actor: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

