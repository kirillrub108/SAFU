"""Модели потока."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.session import Base


class Stream(Base):
    """Поток."""

    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    active = Column(Boolean, default=True, nullable=False)

    members = relationship("StreamMember", back_populates="stream")


class StreamMember(Base):
    """Участник потока (группа)."""

    __tablename__ = "stream_members"

    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("streams.id"), nullable=False, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)

    stream = relationship("Stream", back_populates="members")
    group = relationship("Group")

    __table_args__ = (UniqueConstraint("stream_id", "group_id"),)

