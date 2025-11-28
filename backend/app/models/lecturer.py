"""Модель преподавателя."""
from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base


class Lecturer(Base):
    """Преподаватель."""

    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, nullable=False, index=True)
    chair = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

