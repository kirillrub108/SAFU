"""API для расписания."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.db.session import get_db
from app.schemas import EventDetail
from app.models import Event, TimeSlot
from app.models.event import EventGroup, EventLecturer, EventStream
from app.services.cache import cache_service

router = APIRouter(prefix="/api/timetable", tags=["timetable"])


@router.get("", response_model=List[EventDetail])
def get_timetable(
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    group_id: Optional[int] = Query(None),
    lecturer_id: Optional[int] = Query(None),
    room_id: Optional[int] = Query(None),
    building_id: Optional[int] = Query(None),
    stream_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Получить расписание с фильтрами."""
    cache_key = f"timetable:{date_from}:{date_to}:{group_id}:{lecturer_id}:{room_id}:{building_id}:{stream_id}"
    cached = cache_service.get(cache_key)
    if cached:
        return cached

    query = db.query(Event).filter(Event.status == "scheduled")

    # Объединяем условия по дате, чтобы не делать двойной join
    if date_from or date_to:
        query = query.join(TimeSlot)
        if date_from:
            query = query.filter(TimeSlot.date >= date_from)
        if date_to:
            query = query.filter(TimeSlot.date <= date_to)

    if group_id:
        query = query.join(EventGroup).filter(EventGroup.group_id == group_id)

    if lecturer_id:
        query = query.join(EventLecturer).filter(EventLecturer.lecturer_id == lecturer_id)

    if stream_id:
        query = query.join(EventStream).filter(EventStream.stream_id == stream_id)

    if room_id:
        query = query.filter(Event.room_id == room_id)

    if building_id:
        from app.models import Room

        query = query.join(Room).filter(Room.building_id == building_id)

    events = query.all()

    # Функция для определения конфликтов между событиями
    def detect_conflicts(event_list: List[Event]) -> dict[int, List[int]]:
        """Определяет конфликты между событиями (пересекающиеся временные интервалы)."""
        conflicts = {}
        from app.validators.conflicts import ValidationService
        
        for i, event1 in enumerate(event_list):
            if not event1.time_slot:
                continue
            event_conflicts = []
            for j, event2 in enumerate(event_list):
                if i == j or not event2.time_slot:
                    continue
                # Проверяем пересечение временных интервалов
                if (event1.time_slot.date == event2.time_slot.date and
                    ValidationService.check_time_overlap(
                        event1.time_slot.time_start,
                        event1.time_slot.time_end,
                        event2.time_slot.time_start,
                        event2.time_slot.time_end,
                    )):
                    # Проверяем конфликты по аудитории, преподавателю или группе
                    has_conflict = False
                    # Конфликт аудитории
                    if event1.room_id == event2.room_id:
                        has_conflict = True
                    # Конфликт преподавателя
                    lecturer_ids1 = {el.lecturer_id for el in event1.lecturers}
                    lecturer_ids2 = {el.lecturer_id for el in event2.lecturers}
                    if lecturer_ids1 & lecturer_ids2:
                        has_conflict = True
                    # Конфликт группы
                    group_ids1 = {eg.group_id for eg in event1.groups}
                    group_ids2 = {eg.group_id for eg in event2.groups}
                    if group_ids1 & group_ids2:
                        has_conflict = True
                    
                    if has_conflict:
                        event_conflicts.append(event2.id)
            
            if event_conflicts:
                conflicts[event1.id] = event_conflicts
        
        return conflicts

    # Определяем конфликты
    event_conflicts = detect_conflicts(events)

    # Формируем детальные данные
    result = []
    for event in events:
        event_dict = {
            "id": event.id,
            "discipline_id": event.discipline_id,
            "work_kind_id": event.work_kind_id,
            "room_id": event.room_id,
            "time_slot_id": event.time_slot_id,
            "status": event.status,
            "note": event.note,
        }
        # Добавляем связанные объекты
        event_dict["discipline"] = {
            "id": event.discipline.id,
            "name": event.discipline.name,
        } if event.discipline else None
        event_dict["work_kind"] = {
            "id": event.work_kind.id,
            "name": event.work_kind.name,
            "color_hex": event.work_kind.color_hex,
        } if event.work_kind else None
        event_dict["room"] = {
            "id": event.room.id,
            "number": event.room.number,
            "building": {
                "id": event.room.building.id,
                "name": event.room.building.name,
                "address": event.room.building.address,
            } if event.room.building else None,
        } if event.room else None
        event_dict["time_slot"] = {
            "id": event.time_slot.id,
            "date": event.time_slot.date.isoformat(),
            "pair_number": event.time_slot.pair_number,
            "time_start": event.time_slot.time_start.strftime("%H:%M"),
            "time_end": event.time_slot.time_end.strftime("%H:%M"),
        } if event.time_slot else None
        # Добавляем информацию о конфликтах
        event_dict["has_conflict"] = event.id in event_conflicts
        event_dict["conflicting_event_ids"] = event_conflicts.get(event.id, [])
        event_dict["lecturers"] = [
            {"id": el.lecturer.id, "fio": el.lecturer.fio}
            for el in event.lecturers
            if el.lecturer
        ]
        event_dict["groups"] = [
            {"id": eg.group.id, "code": eg.group.code}
            for eg in event.groups
            if eg.group
        ]
        event_dict["subgroups"] = [
            {"id": es.subgroup.id, "code": es.subgroup.code}
            for es in event.subgroups
            if es.subgroup
        ]
        event_dict["streams"] = [
            {"id": est.stream.id, "name": est.stream.name}
            for est in event.streams
            if est.stream
        ]
        result.append(event_dict)

    cache_service.set(cache_key, result, ttl=300)  # 5 минут
    return result


@router.get("/day/{day_date}", response_model=List[EventDetail])
def get_timetable_day(day_date: date, db: Session = Depends(get_db)):
    """Получить расписание на день."""
    return get_timetable(date_from=day_date, date_to=day_date, db=db)


@router.get("/week/{year}/{week}", response_model=List[EventDetail])
def get_timetable_week(year: int, week: int, db: Session = Depends(get_db)):
    """Получить расписание на неделю."""
    from datetime import timedelta

    # Простой расчет начала недели (ISO week)
    jan1 = date(year, 1, 1)
    days_offset = jan1.weekday()
    week_start = jan1 + timedelta(days=week * 7 - days_offset)
    week_end = week_start + timedelta(days=6)
    return get_timetable(date_from=week_start, date_to=week_end, db=db)


@router.get("/group/{group_id}", response_model=List[EventDetail])
def get_timetable_group(group_id: int, db: Session = Depends(get_db)):
    """Получить расписание группы."""
    return get_timetable(group_id=group_id, db=db)


@router.get("/lecturer/{lecturer_id}", response_model=List[EventDetail])
def get_timetable_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    """Получить расписание преподавателя."""
    return get_timetable(lecturer_id=lecturer_id, db=db)

