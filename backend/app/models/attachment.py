"""Модель вложения."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class Attachment(Base):
    """Вложение (источник импорта)."""

    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String, nullable=False)  # "html_import", "ics", etc.
    url = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

