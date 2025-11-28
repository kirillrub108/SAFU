"""Модель временного слота."""
from sqlalchemy import Column, Integer, Date, String, Time
from app.db.session import Base


class TimeSlot(Base):
    """Временной слот (пара)."""

    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    pair_number = Column(Integer, nullable=False)  # 1-8
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)
    timezone = Column(String, default="Europe/Moscow", nullable=False)

