"""Модель вида занятия."""
from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class WorkKind(Base):
    """Вид занятия."""

    __tablename__ = "work_kinds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    color_hex = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)

