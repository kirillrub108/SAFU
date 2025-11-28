"""API для событий."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Event, EventCreate, EventUpdate, EventDetail
from app.models import Event as EventModel
from app.models.event import EventLecturer, EventGroup, EventSubgroup, EventStream
from app.validators.conflicts import ValidationService, ConflictError
from app.services.change_log import ChangeLogService
from app.services.cache import cache_service

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """Создать событие."""
    # Валидация конфликтов
    errors = ValidationService.validate_event(
        db=db,
        room_id=event.room_id,
        time_slot_id=event.time_slot_id,
        lecturer_ids=event.lecturer_ids,
        group_ids=event.group_ids,
        subgroup_ids=event.subgroup_ids,
        stream_ids=event.stream_ids,
        work_kind_id=event.work_kind_id,
    )

    if errors:
        raise HTTPException(
            status_code=400,
            detail={"message": "Конфликты расписания", "errors": [e.message for e in errors]},
        )

    # Создание события
    db_event = EventModel(
        discipline_id=event.discipline_id,
        work_kind_id=event.work_kind_id,
        room_id=event.room_id,
        time_slot_id=event.time_slot_id,
        status=event.status,
        note=event.note,
    )
    db.add(db_event)
    db.flush()

    # Связи
    for lecturer_id in event.lecturer_ids:
        db.add(EventLecturer(event_id=db_event.id, lecturer_id=lecturer_id))
    for group_id in event.group_ids:
        db.add(EventGroup(event_id=db_event.id, group_id=group_id))
    for subgroup_id in event.subgroup_ids:
        db.add(EventSubgroup(event_id=db_event.id, subgroup_id=subgroup_id))
    for stream_id in event.stream_ids:
        db.add(EventStream(event_id=db_event.id, stream_id=stream_id))

    db.commit()
    db.refresh(db_event)

    # Запись в ChangeLog
    event_state = ChangeLogService.get_event_state(db, db_event.id)
    ChangeLogService.log_event_change(
        db=db,
        event_id=db_event.id,
        actor=None,  # TODO: из сессии пользователя
        reason=event.reason or "Создание события",
        diff_before=None,
        diff_after=event_state,
        source="api",
    )

    # Инвалидация кэша
    cache_service.invalidate_timetable_cache()

    return db_event


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    """Обновить событие."""
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    # Получаем старое состояние для диффа
    old_state = ChangeLogService.get_event_state(db, event_id)

    # Обновление полей
    update_data = event.model_dump(exclude_unset=True, exclude={"lecturer_ids", "group_ids", "subgroup_ids", "stream_ids", "reason"})
    for field, value in update_data.items():
        setattr(db_event, field, value)

    # Обновление связей
    if event.lecturer_ids is not None:
        db.query(EventLecturer).filter(EventLecturer.event_id == event_id).delete()
        for lecturer_id in event.lecturer_ids:
            db.add(EventLecturer(event_id=event_id, lecturer_id=lecturer_id))

    if event.group_ids is not None:
        db.query(EventGroup).filter(EventGroup.event_id == event_id).delete()
        for group_id in event.group_ids:
            db.add(EventGroup(event_id=event_id, group_id=group_id))

    if event.subgroup_ids is not None:
        db.query(EventSubgroup).filter(EventSubgroup.event_id == event_id).delete()
        for subgroup_id in event.subgroup_ids:
            db.add(EventSubgroup(event_id=event_id, subgroup_id=subgroup_id))

    if event.stream_ids is not None:
        db.query(EventStream).filter(EventStream.stream_id == event_id).delete()
        for stream_id in event.stream_ids:
            db.add(EventStream(event_id=event_id, stream_id=stream_id))

    # Валидация конфликтов (если изменились время/аудитория)
    if event.room_id or event.time_slot_id:
        room_id = event.room_id or db_event.room_id
        time_slot_id = event.time_slot_id or db_event.time_slot_id
        lecturer_ids = event.lecturer_ids if event.lecturer_ids is not None else [el.lecturer_id for el in db_event.lecturers]
        group_ids = event.group_ids if event.group_ids is not None else [eg.group_id for eg in db_event.groups]
        subgroup_ids = event.subgroup_ids if event.subgroup_ids is not None else [es.subgroup_id for es in db_event.subgroups]
        stream_ids = event.stream_ids if event.stream_ids is not None else [est.stream_id for est in db_event.streams]
        work_kind_id = event.work_kind_id or db_event.work_kind_id

        errors = ValidationService.validate_event(
            db=db,
            room_id=room_id,
            time_slot_id=time_slot_id,
            lecturer_ids=lecturer_ids,
            group_ids=group_ids,
            subgroup_ids=subgroup_ids,
            stream_ids=stream_ids,
            work_kind_id=work_kind_id,
            exclude_event_id=event_id,
        )

        if errors:
            raise HTTPException(
                status_code=400,
                detail={"message": "Конфликты расписания", "errors": [e.message for e in errors]},
            )

    db.commit()
    db.refresh(db_event)

    # Запись в ChangeLog
    new_state = ChangeLogService.get_event_state(db, event_id)
    ChangeLogService.log_event_change(
        db=db,
        event_id=event_id,
        actor=None,
        reason=event.reason or "Обновление события",
        diff_before=old_state,
        diff_after=new_state,
        source="api",
    )

    # Инвалидация кэша
    cache_service.invalidate_timetable_cache()

    return db_event


@router.delete("/{event_id}")
def delete_event(event_id: int, reason: str = None, db: Session = Depends(get_db)):
    """Удалить событие (soft delete)."""
    db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    old_state = ChangeLogService.get_event_state(db, event_id)

    # Soft delete
    db_event.status = "cancelled"
    db.commit()

    # Запись в ChangeLog
    new_state = ChangeLogService.get_event_state(db, event_id)
    ChangeLogService.log_event_change(
        db=db,
        event_id=event_id,
        actor=None,
        reason=reason or "Удаление события",
        diff_before=old_state,
        diff_after=new_state,
        source="api",
    )

    # Инвалидация кэша
    cache_service.invalidate_timetable_cache()

    return {"message": "Событие удалено"}


@router.get("/{event_id}", response_model=EventDetail)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Получить событие по ID."""
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    # Формируем детальные данные (аналогично timetable.py)
    event_dict = {
        "id": event.id,
        "discipline_id": event.discipline_id,
        "work_kind_id": event.work_kind_id,
        "room_id": event.room_id,
        "time_slot_id": event.time_slot_id,
        "status": event.status,
        "note": event.note,
        "discipline": {"id": event.discipline.id, "name": event.discipline.name} if event.discipline else None,
        "work_kind": {"id": event.work_kind.id, "name": event.work_kind.name, "color_hex": event.work_kind.color_hex} if event.work_kind else None,
        "room": {
            "id": event.room.id,
            "number": event.room.number,
            "building": {"id": event.room.building.id, "name": event.room.building.name, "address": event.room.building.address} if event.room.building else None,
        } if event.room else None,
        "time_slot": {
            "id": event.time_slot.id,
            "date": event.time_slot.date.isoformat(),
            "pair_number": event.time_slot.pair_number,
            "time_start": event.time_slot.time_start.strftime("%H:%M"),
            "time_end": event.time_slot.time_end.strftime("%H:%M"),
        } if event.time_slot else None,
        "lecturers": [{"id": el.lecturer.id, "fio": el.lecturer.fio} for el in event.lecturers if el.lecturer],
        "groups": [{"id": eg.group.id, "code": eg.group.code} for eg in event.groups if eg.group],
        "subgroups": [{"id": es.subgroup.id, "code": es.subgroup.code} for es in event.subgroups if es.subgroup],
        "streams": [{"id": est.stream.id, "name": est.stream.name} for est in event.streams if est.stream],
    }
    return event_dict

