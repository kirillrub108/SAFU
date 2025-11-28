"""Модель корпуса."""
from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base


class Building(Base):
    """Корпус."""

    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    code = Column(String, unique=True, index=True)
    address = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

