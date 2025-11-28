"""Модели событий."""
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base


class Event(Base):
    """Событие (занятие)."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"), nullable=False, index=True)
    work_kind_id = Column(Integer, ForeignKey("work_kinds.id"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, index=True)
    time_slot_id = Column(Integer, ForeignKey("time_slots.id"), nullable=False, index=True)
    status = Column(String, default="scheduled", nullable=False)  # scheduled, cancelled, moved
    note = Column(String, nullable=True)

    discipline = relationship("Discipline")
    work_kind = relationship("WorkKind")
    room = relationship("Room")
    time_slot = relationship("TimeSlot")

    lecturers = relationship("EventLecturer", back_populates="event", cascade="all, delete-orphan")
    groups = relationship("EventGroup", back_populates="event", cascade="all, delete-orphan")
    subgroups = relationship("EventSubgroup", back_populates="event", cascade="all, delete-orphan")
    streams = relationship("EventStream", back_populates="event", cascade="all, delete-orphan")


class EventLecturer(Base):
    """Связь события и преподавателя."""

    __tablename__ = "event_lecturers"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    lecturer_id = Column(Integer, ForeignKey("lecturers.id"), nullable=False, index=True)

    event = relationship("Event", back_populates="lecturers")
    lecturer = relationship("Lecturer")

    __table_args__ = (UniqueConstraint("event_id", "lecturer_id"),)


class EventGroup(Base):
    """Связь события и группы."""

    __tablename__ = "event_groups"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)

    event = relationship("Event", back_populates="groups")
    group = relationship("Group")

    __table_args__ = (UniqueConstraint("event_id", "group_id"),)


class EventSubgroup(Base):
    """Связь события и подгруппы."""

    __tablename__ = "event_subgroups"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    subgroup_id = Column(Integer, ForeignKey("subgroups.id"), nullable=False, index=True)

    event = relationship("Event", back_populates="subgroups")
    subgroup = relationship("Subgroup")

    __table_args__ = (UniqueConstraint("event_id", "subgroup_id"),)


class EventStream(Base):
    """Связь события и потока."""

    __tablename__ = "event_streams"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"), nullable=False, index=True)

    event = relationship("Event", back_populates="streams")
    stream = relationship("Stream")

    __table_args__ = (UniqueConstraint("event_id", "stream_id"),)

