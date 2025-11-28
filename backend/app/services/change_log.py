"""Сервис журнала изменений."""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.models import ChangeLog, Event
from datetime import datetime
import json


class ChangeLogService:
    """Сервис для работы с журналом изменений."""

    @staticmethod
    def create_diff(
        before: Optional[Dict[str, Any]], after: Optional[Dict[str, Any]]
    ) -> tuple[Optional[Dict], Optional[Dict]]:
        """Создание диффа между состояниями."""
        return before, after

    @staticmethod
    def log_event_change(
        db: Session,
        event_id: int,
        actor: Optional[str],
        reason: Optional[str],
        diff_before: Optional[Dict[str, Any]],
        diff_after: Optional[Dict[str, Any]],
        source: str = "api",
    ) -> ChangeLog:
        """Запись изменения события в журнал."""
        change_log = ChangeLog(
            entity="event",
            entity_id=event_id,
            actor=actor,
            reason=reason,
            diff_before=diff_before,
            diff_after=diff_after,
            source=source,
        )
        db.add(change_log)
        db.commit()
        db.refresh(change_log)
        return change_log

    @staticmethod
    def get_event_state(db: Session, event_id: int) -> Optional[Dict[str, Any]]:
        """Получение текущего состояния события для диффа."""
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Собираем связанные данные
        lecturer_ids = [el.lecturer_id for el in event.lecturers]
        group_ids = [eg.group_id for eg in event.groups]
        subgroup_ids = [es.subgroup_id for es in event.subgroups]
        stream_ids = [est.stream_id for est in event.streams]

        return {
            "discipline_id": event.discipline_id,
            "work_kind_id": event.work_kind_id,
            "room_id": event.room_id,
            "time_slot_id": event.time_slot_id,
            "status": event.status,
            "note": event.note,
            "lecturer_ids": lecturer_ids,
            "group_ids": group_ids,
            "subgroup_ids": subgroup_ids,
            "stream_ids": stream_ids,
        }

