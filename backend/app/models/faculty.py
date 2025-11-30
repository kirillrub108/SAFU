"""Модель факультета."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base


class Faculty(Base):
    """Факультет."""

    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    active = Column(Boolean, default=True, nullable=False)

    groups = relationship("Group", back_populates="faculty")

