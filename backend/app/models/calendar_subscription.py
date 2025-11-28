"""Модель подписки на календарь."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class FilterKind(str, enum.Enum):
    """Тип фильтра подписки."""

    GROUP = "group"
    LECTURER = "lecturer"
    STREAM = "stream"


class CalendarSubscription(Base):
    """Подписка на календарь."""

    __tablename__ = "calendar_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    filter_kind = Column(SQLEnum(FilterKind), nullable=False, index=True)
    filter_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

