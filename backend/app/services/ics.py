"""Сервис генерации ICS календарей."""
from icalendar import Calendar, Event as ICalEvent
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Event, TimeSlot, Room, Building, Discipline, WorkKind, Lecturer
from app.models.event import EventLecturer, EventGroup, EventSubgroup, EventStream
from app.models.group import Group, Subgroup
from app.models.stream import Stream
import pytz


class ICSService:
    """Сервис генерации ICS файлов."""

    @staticmethod
    def generate_ics_for_events(
        db: Session, events: List[Event], title: str = "Расписание САФУ"
    ) -> str:
        """Генерация ICS календаря для списка событий."""
        cal = Calendar()
        cal.add("prodid", "-//САФУ Расписание//RU")
        cal.add("version", "2.0")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")

        moscow_tz = pytz.timezone("Europe/Moscow")

        for event in events:
            ical_event = ICalEvent()
            ical_event.add("uid", f"event-{event.id}@safu.ru")

            # Время
            time_slot = event.time_slot
            date_obj = time_slot.date
            start_time = datetime.combine(date_obj, time_slot.time_start)
            end_time = datetime.combine(date_obj, time_slot.time_end)

            # Применяем таймзону
            start_dt = moscow_tz.localize(start_time)
            end_dt = moscow_tz.localize(end_time)

            ical_event.add("dtstart", start_dt)
            ical_event.add("dtend", end_dt)
            ical_event.add("dtstamp", datetime.now(moscow_tz))

            # Название
            discipline = db.query(Discipline).filter(Discipline.id == event.discipline_id).first()
            work_kind = db.query(WorkKind).filter(WorkKind.id == event.work_kind_id).first()
            summary = f"{discipline.name if discipline else 'Дисциплина'}"
            if work_kind:
                summary += f" ({work_kind.name})"
            ical_event.add("summary", summary)

            # Описание
            lecturers = (
                db.query(Lecturer)
                .join(EventLecturer)
                .filter(EventLecturer.event_id == event.id)
                .all()
            )
            lecturer_names = ", ".join([l.fio for l in lecturers])

            groups = (
                db.query(Group)
                .join(EventGroup)
                .filter(EventGroup.event_id == event.id)
                .all()
            )
            group_codes = ", ".join([g.code for g in groups])

            subgroups = (
                db.query(Subgroup)
                .join(EventSubgroup)
                .filter(EventSubgroup.event_id == event.id)
                .all()
            )
            subgroup_codes = ", ".join([sg.code for sg in subgroups])

            streams = (
                db.query(Stream)
                .join(EventStream)
                .filter(EventStream.event_id == event.id)
                .all()
            )
            stream_names = ", ".join([s.name for s in streams])

            description_parts = []
            if lecturer_names:
                description_parts.append(f"Преподаватель: {lecturer_names}")
            if group_codes:
                description_parts.append(f"Группы: {group_codes}")
            if subgroup_codes:
                description_parts.append(f"Подгруппы: {subgroup_codes}")
            if stream_names:
                description_parts.append(f"Потоки: {stream_names}")
            if event.note:
                description_parts.append(f"Примечание: {event.note}")

            ical_event.add("description", "\n".join(description_parts))

            # Место
            room = db.query(Room).filter(Room.id == event.room_id).first()
            if room:
                building = db.query(Building).filter(Building.id == room.building_id).first()
                location_parts = []
                if building:
                    location_parts.append(building.name)
                    if building.address:
                        location_parts.append(building.address)
                location_parts.append(f"Ауд. {room.number}")
                ical_event.add("location", ", ".join(location_parts))

            cal.add_component(ical_event)

        return cal.to_ical().decode("utf-8")

    @staticmethod
    def generate_ics_for_group(db: Session, group_id: int) -> str:
        """Генерация ICS для группы."""
        events = (
            db.query(Event)
            .join(EventGroup)
            .filter(EventGroup.group_id == group_id, Event.status == "scheduled")
            .all()
        )
        group = db.query(Group).filter(Group.id == group_id).first()
        title = f"Расписание группы {group.code if group else group_id}"
        return ICSService.generate_ics_for_events(db, events, title)

    @staticmethod
    def generate_ics_for_lecturer(db: Session, lecturer_id: int) -> str:
        """Генерация ICS для преподавателя."""
        events = (
            db.query(Event)
            .join(EventLecturer)
            .filter(EventLecturer.lecturer_id == lecturer_id, Event.status == "scheduled")
            .all()
        )
        lecturer = db.query(Lecturer).filter(Lecturer.id == lecturer_id).first()
        title = f"Расписание {lecturer.fio if lecturer else lecturer_id}"
        return ICSService.generate_ics_for_events(db, events, title)

    @staticmethod
    def generate_ics_for_stream(db: Session, stream_id: int) -> str:
        """Генерация ICS для потока."""
        events = (
            db.query(Event)
            .join(EventStream)
            .filter(EventStream.stream_id == stream_id, Event.status == "scheduled")
            .all()
        )
        stream = db.query(Stream).filter(Stream.id == stream_id).first()
        title = f"Расписание потока {stream.name if stream else stream_id}"
        return ICSService.generate_ics_for_events(db, events, title)

