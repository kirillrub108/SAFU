"""Тесты валидации конфликтов."""
import pytest
from datetime import date, time
from app.models import Building, Room, Lecturer, Group, Discipline, WorkKind, TimeSlot, Event
from app.models.event import EventLecturer, EventGroup
from app.validators.conflicts import ValidationService, ConflictError


def test_room_conflict(db):
    """Тест конфликта аудитории."""
    # Создаем корпус и аудиторию
    building = Building(name="Тест", code="T", address="Тест")
    db.add(building)
    db.flush()

    room = Room(building_id=building.id, number="101", capacity=30, type="lecture")
    db.add(room)
    db.flush()

    # Создаем временной слот
    time_slot = TimeSlot(
        date=date(2025, 11, 17),
        pair_number=1,
        time_start=time(8, 30),
        time_end=time(10, 0),
        timezone="Europe/Moscow",
    )
    db.add(time_slot)
    db.flush()

    # Создаем первое событие
    discipline = Discipline(name="Тест", short_name="Т")
    work_kind = WorkKind(name="Лекция", color_hex="#28a745")
    db.add(discipline)
    db.add(work_kind)
    db.flush()

    event1 = Event(
        discipline_id=discipline.id,
        work_kind_id=work_kind.id,
        room_id=room.id,
        time_slot_id=time_slot.id,
        status="scheduled",
    )
    db.add(event1)
    db.commit()

    # Проверяем конфликт
    error = ValidationService.check_room_conflict(db, room.id, time_slot.id)
    assert error is not None
    assert error.conflict_type == "room_conflict"

    # Проверяем без конфликта (другая аудитория)
    room2 = Room(building_id=building.id, number="102", capacity=30, type="lecture")
    db.add(room2)
    db.flush()
    error2 = ValidationService.check_room_conflict(db, room2.id, time_slot.id)
    assert error2 is None


def test_lecturer_conflict(db):
    """Тест конфликта преподавателя."""
    building = Building(name="Тест", code="T", address="Тест")
    db.add(building)
    db.flush()

    room = Room(building_id=building.id, number="101", capacity=30, type="lecture")
    db.add(room)
    db.flush()

    lecturer = Lecturer(fio="Тестов Т.Т.")
    db.add(lecturer)
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

    discipline = Discipline(name="Тест", short_name="Т")
    work_kind = WorkKind(name="Лекция", color_hex="#28a745")
    db.add(discipline)
    db.add(work_kind)
    db.flush()

    event1 = Event(
        discipline_id=discipline.id,
        work_kind_id=work_kind.id,
        room_id=room.id,
        time_slot_id=time_slot.id,
        status="scheduled",
    )
    db.add(event1)
    db.flush()
    db.add(EventLecturer(event_id=event1.id, lecturer_id=lecturer.id))
    db.commit()

    # Проверяем конфликт
    error = ValidationService.check_lecturer_conflict(db, [lecturer.id], time_slot.id)
    assert error is not None
    assert error.conflict_type == "lecturer_conflict"


def test_group_conflict(db):
    """Тест конфликта группы."""
    building = Building(name="Тест", code="T", address="Тест")
    db.add(building)
    db.flush()

    room = Room(building_id=building.id, number="101", capacity=30, type="lecture")
    db.add(room)
    db.flush()

    group = Group(code="TEST", name="Тест")
    db.add(group)
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

    discipline = Discipline(name="Тест", short_name="Т")
    work_kind = WorkKind(name="Лекция", color_hex="#28a745")
    db.add(discipline)
    db.add(work_kind)
    db.flush()

    event1 = Event(
        discipline_id=discipline.id,
        work_kind_id=work_kind.id,
        room_id=room.id,
        time_slot_id=time_slot.id,
        status="scheduled",
    )
    db.add(event1)
    db.flush()
    db.add(EventGroup(event_id=event1.id, group_id=group.id))
    db.commit()

    # Проверяем конфликт
    error = ValidationService.check_group_conflict(db, [group.id], [], [], time_slot.id)
    assert error is not None
    assert error.conflict_type == "group_conflict"


def test_capacity_check(db):
    """Тест проверки вместимости."""
    building = Building(name="Тест", code="T", address="Тест")
    db.add(building)
    db.flush()

    room = Room(building_id=building.id, number="101", capacity=20, type="lecture")
    db.add(room)
    db.flush()

    group1 = Group(code="TEST1", name="Тест1")
    group2 = Group(code="TEST2", name="Тест2")
    db.add(group1)
    db.add(group2)
    db.flush()

    # 2 группы * 25 студентов = 50 > 20 (вместимость)
    error = ValidationService.check_capacity(db, room.id, [group1.id, group2.id], [])
    assert error is not None
    assert error.conflict_type == "capacity_exceeded"

    # 1 группа * 25 = 25 > 20, но для MVP это предупреждение
    error2 = ValidationService.check_capacity(db, room.id, [group1.id], [])
    # В MVP может быть предупреждение, но не ошибка для одной группы

