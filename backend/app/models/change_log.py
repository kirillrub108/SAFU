"""Модель журнала изменений."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Index
from sqlalchemy.sql import func
from app.db.session import Base


class ChangeLog(Base):
    """Журнал изменений."""

    __tablename__ = "change_log"

    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, nullable=False, index=True)  # "event", "room", etc.
    entity_id = Column(Integer, nullable=False, index=True)
    actor = Column(String, nullable=True)  # user_id или "system"
    change_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reason = Column(String, nullable=True)
    diff_before = Column(JSON, nullable=True)
    diff_after = Column(JSON, nullable=True)
    source = Column(String, nullable=True)  # "api", "import", "admin"

    __table_args__ = (Index("idx_entity_id", "entity", "entity_id"),)

