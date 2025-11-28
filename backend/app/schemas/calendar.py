"""Схемы для календаря."""
from pydantic import BaseModel
from datetime import datetime
from app.models.calendar_subscription import FilterKind


class CalendarSubscriptionBase(BaseModel):
    filter_kind: FilterKind
    filter_id: int
    active: bool = True


class CalendarSubscriptionCreate(CalendarSubscriptionBase):
    pass


class CalendarSubscription(CalendarSubscriptionBase):
    id: int
    token: str
    created_at: datetime

    class Config:
        from_attributes = True

