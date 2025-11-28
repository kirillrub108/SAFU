"""Тесты генерации ICS."""
import pytest
from datetime import date, time
from app.models import (
    Building,
    Room,
    Lecturer,
    Group,
    Discipline,
    WorkKind,
    TimeSlot,
    Event,
)
from app.models.event import EventLecturer, EventGroup
from app.services.ics import ICSService


def test_ics_generation(db):
    """Тест генерации ICS."""
    # Создаем данные
    building = Building(name="Тест", code="T", address="Тест")
    db.add(building)
    db.flush()

    room = Room(building_id=building.id, number="101", capacity=30, type="lecture")
    db.add(room)
    db.flush()

    lecturer = Lecturer(fio="Тестов Т.Т.")
    db.add(lecturer)
    db.flush()

    group = Group(code="TEST", name="Тест")
    db.add(group)
    db.flush()

    discipline = Discipline(name="Тест", short_name="Т")
    work_kind = WorkKind(name="Лекция", color_hex="#28a745")
    db.add(discipline)
    db.add(work_kind)
    db.flush()

    time_slot = TimeSlot(
        date=date(2025, 11, 17),
        pair_number=1,
        time_start=time(8, 30),
        time_end=time(10, 0),
        timezone="Europe/Moscow",
    )
    db.add(time_slot)
    db.flush()

    event = Event(
        discipline_id=discipline.id,
        work_kind_id=work_kind.id,
        room_id=room.id,
        time_slot_id=time_slot.id,
        status="scheduled",
    )
    db.add(event)
    db.flush()
    db.add(EventLecturer(event_id=event.id, lecturer_id=lecturer.id))
    db.add(EventGroup(event_id=event.id, group_id=group.id))
    db.commit()

    # Генерируем ICS
    ics_content = ICSService.generate_ics_for_group(db, group.id)

    # Проверяем содержимое
    assert "BEGIN:VCALENDAR" in ics_content
    assert "BEGIN:VEVENT" in ics_content
    assert "Тест" in ics_content
    assert "Тестов Т.Т." in ics_content

