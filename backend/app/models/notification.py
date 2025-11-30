"""Модель уведомлений."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class NotificationType(str, enum.Enum):
    """Типы уведомлений."""
    SCHEDULE_CHANGE = "schedule_change"
    EVENT_CANCELLED = "event_cancelled"
    EVENT_ADDED = "event_added"
    EVENT_MODIFIED = "event_modified"
    ROOM_CHANGED = "room_changed"
    TIME_CHANGED = "time_changed"


class Notification(Base):
    """Уведомление."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="notifications")
    event = relationship("Event")


class NotificationSettings(Base):
    """Настройки уведомлений пользователя."""

    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    schedule_changes = Column(Boolean, default=True, nullable=False)
    event_cancelled = Column(Boolean, default=True, nullable=False)
    event_added = Column(Boolean, default=True, nullable=False)
    event_modified = Column(Boolean, default=True, nullable=False)
    room_changed = Column(Boolean, default=True, nullable=False)
    time_changed = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="notification_settings")

