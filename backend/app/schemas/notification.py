"""Схемы для уведомлений."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.notification import NotificationType


class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: str
    event_id: Optional[int] = None


class Notification(NotificationBase):
    id: int
    user_id: int
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationSettingsBase(BaseModel):
    schedule_changes: bool = True
    event_cancelled: bool = True
    event_added: bool = True
    event_modified: bool = True
    room_changed: bool = True
    time_changed: bool = True


class NotificationSettings(NotificationSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationSettingsUpdate(NotificationSettingsBase):
    pass

