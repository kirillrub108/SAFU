"""Модель дисциплины."""
from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class Discipline(Base):
    """Дисциплина."""

    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    short_name = Column(String, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

