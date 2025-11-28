"""API для истории изменений."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.session import get_db
from app.schemas import ChangeLog, ChangeLogFilter
from app.models import ChangeLog as ChangeLogModel

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/events/{event_id}/history", response_model=List[ChangeLog])
def get_event_history(event_id: int, db: Session = Depends(get_db)):
    """Получить историю изменений события."""
    return (
        db.query(ChangeLogModel)
        .filter(ChangeLogModel.entity == "event", ChangeLogModel.entity_id == event_id)
        .order_by(ChangeLogModel.change_at.desc())
        .all()
    )


@router.get("/changelog", response_model=List[ChangeLog])
def get_changelog(
    entity: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    actor: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    """Получить журнал изменений с фильтрами."""
    query = db.query(ChangeLogModel)

    if entity:
        query = query.filter(ChangeLogModel.entity == entity)
    if entity_id:
        query = query.filter(ChangeLogModel.entity_id == entity_id)
    if actor:
        query = query.filter(ChangeLogModel.actor == actor)
    if date_from:
        query = query.filter(ChangeLogModel.change_at >= date_from)
    if date_to:
        query = query.filter(ChangeLogModel.change_at <= date_to)

    return query.order_by(ChangeLogModel.change_at.desc()).limit(100).all()

