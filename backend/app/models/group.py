"""Модели группы и подгруппы."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Group(Base):
    """Группа."""

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    subgroups = relationship("Subgroup", back_populates="group")


class Subgroup(Base):
    """Подгруппа."""

    __tablename__ = "subgroups"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    active = Column(Boolean, default=True, nullable=False)

    group = relationship("Group", back_populates="subgroups")

