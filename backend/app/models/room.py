"""Модель аудитории."""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base


class Room(Base):
    """Аудитория."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False, index=True)
    number = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # lecture, practice, lab, sport, etc.
    features = Column(JSON, nullable=True)  # {"projector": true, "computers": 20}
    active = Column(Boolean, default=True, nullable=False)

    building = relationship("Building", backref="rooms")

