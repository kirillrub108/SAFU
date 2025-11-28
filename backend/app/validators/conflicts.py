"""Валидация конфликтов расписания."""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, time
from typing import List, Optional
from app.models import Event, TimeSlot, Room, Lecturer, Group, Subgroup, Stream
from app.models.event import EventLecturer, EventGroup, EventSubgroup, EventStream


class ConflictError(Exception):
    """Ошибка конфликта расписания."""

    def __init__(self, message: str, conflict_type: str):
        self.message = message
        self.conflict_type = conflict_type
        super().__init__(message)


class ValidationService:
    """Сервис валидации конфликтов."""

    @staticmethod
    def check_time_overlap(
        time_start1: time,
        time_end1: time,
        time_start2: time,
        time_end2: time,
    ) -> bool:
        """Проверка пересечения временных интервалов."""
        # Интервалы пересекаются, если:
        # start1 < end2 AND start2 < end1
        return time_start1 < time_end2 and time_start2 < time_end1

    @staticmethod
    def check_room_conflict(
        db: Session,
        room_id: int,
        time_slot_id: int,
        exclude_event_id: Optional[int] = None,
    ) -> Optional[ConflictError]:
        """Проверка конфликта аудитории (включая пересекающиеся временные интервалы)."""
        time_slot = db.query(TimeSlot).filter(TimeSlot.id == time_slot_id).first()
        if not time_slot:
            return None

        # Проверяем события в той же аудитории на ту же дату
        query = (
            db.query(Event)
            .join(TimeSlot)
            .filter(
                Event.room_id == room_id,
                Event.status == "scheduled",
                TimeSlot.date == time_slot.date,
            )
        )

        if exclude_event_id:
            query = query.filter(Event.id != exclude_event_id)

        conflicting_events = query.all()
        
        # Проверяем пересечение временных интервалов
        for conflicting in conflicting_events:
            if conflicting.time_slot:
                if ValidationService.check_time_overlap(
                    time_slot.time_start,
                    time_slot.time_end,
                    conflicting.time_slot.time_start,
                    conflicting.time_slot.time_end,
                ):
                    return ConflictError(
                        f"Аудитория занята в пересекающееся время (событие #{conflicting.id}, {conflicting.time_slot.time_start.strftime('%H:%M')}-{conflicting.time_slot.time_end.strftime('%H:%M')})",
                        "room_conflict",
                    )
        
        return None

    @staticmethod
    def check_lecturer_conflict(
        db: Session,
        lecturer_ids: List[int],
        time_slot_id: int,
        exclude_event_id: Optional[int] = None,
    ) -> Optional[ConflictError]:
        """Проверка конфликта преподавателей (включая пересекающиеся временные интервалы)."""
        if not lecturer_ids:
            return None

        time_slot = db.query(TimeSlot).filter(TimeSlot.id == time_slot_id).first()
        if not time_slot:
            return None

        query = (
            db.query(Event)
            .join(TimeSlot)
            .join(EventLecturer)
            .filter(
                EventLecturer.lecturer_id.in_(lecturer_ids),
                Event.status == "scheduled",
                TimeSlot.date == time_slot.date,
            )
        )

        if exclude_event_id:
            query = query.filter(Event.id != exclude_event_id)

        conflicting_events = query.all()
        
        # Проверяем пересечение временных интервалов
        for conflicting in conflicting_events:
            if conflicting.time_slot:
                if ValidationService.check_time_overlap(
                    time_slot.time_start,
                    time_slot.time_end,
                    conflicting.time_slot.time_start,
                    conflicting.time_slot.time_end,
                ):
                    return ConflictError(
                        f"Преподаватель уже ведет занятие в пересекающееся время (событие #{conflicting.id}, {conflicting.time_slot.time_start.strftime('%H:%M')}-{conflicting.time_slot.time_end.strftime('%H:%M')})",
                        "lecturer_conflict",
                    )
        
        return None

    @staticmethod
    def check_group_conflict(
        db: Session,
        group_ids: List[int],
        subgroup_ids: List[int],
        stream_ids: List[int],
        time_slot_id: int,
        exclude_event_id: Optional[int] = None,
    ) -> Optional[ConflictError]:
        """Проверка конфликта групп/подгрупп/потоков."""
        time_slot = db.query(TimeSlot).filter(TimeSlot.id == time_slot_id).first()
        if not time_slot:
            return None

        # Проверка групп (включая пересекающиеся временные интервалы)
        if group_ids:
            query = (
                db.query(Event)
                .join(TimeSlot)
                .join(EventGroup)
                .filter(
                    EventGroup.group_id.in_(group_ids),
                    Event.status == "scheduled",
                    TimeSlot.date == time_slot.date,
                )
            )
            if exclude_event_id:
                query = query.filter(Event.id != exclude_event_id)
            
            conflicting_events = query.all()
            
            # Проверяем пересечение временных интервалов
            for conflicting in conflicting_events:
                if conflicting.time_slot:
                    if ValidationService.check_time_overlap(
                        time_slot.time_start,
                        time_slot.time_end,
                        conflicting.time_slot.time_start,
                        conflicting.time_slot.time_end,
                    ):
                        return ConflictError(
                            f"Группа уже имеет занятие в пересекающееся время (событие #{conflicting.id}, {conflicting.time_slot.time_start.strftime('%H:%M')}-{conflicting.time_slot.time_end.strftime('%H:%M')})",
                            "group_conflict",
                        )

        # Проверка подгрупп (включая пересекающиеся временные интервалы)
        if subgroup_ids:
            query = (
                db.query(Event)
                .join(TimeSlot)
                .join(EventSubgroup)
                .filter(
                    EventSubgroup.subgroup_id.in_(subgroup_ids),
                    Event.status == "scheduled",
                    TimeSlot.date == time_slot.date,
                )
            )
            if exclude_event_id:
                query = query.filter(Event.id != exclude_event_id)
            
            conflicting_events = query.all()
            
            # Проверяем пересечение временных интервалов
            for conflicting in conflicting_events:
                if conflicting.time_slot:
                    if ValidationService.check_time_overlap(
                        time_slot.time_start,
                        time_slot.time_end,
                        conflicting.time_slot.time_start,
                        conflicting.time_slot.time_end,
                    ):
                        return ConflictError(
                            f"Подгруппа уже имеет занятие в пересекающееся время (событие #{conflicting.id}, {conflicting.time_slot.time_start.strftime('%H:%M')}-{conflicting.time_slot.time_end.strftime('%H:%M')})",
                            "subgroup_conflict",
                        )

        # Проверка потоков (включая пересекающиеся временные интервалы)
        if stream_ids:
            query = (
                db.query(Event)
                .join(TimeSlot)
                .join(EventStream)
                .filter(
                    EventStream.stream_id.in_(stream_ids),
                    Event.status == "scheduled",
                    TimeSlot.date == time_slot.date,
                )
            )
            if exclude_event_id:
                query = query.filter(Event.id != exclude_event_id)
            
            conflicting_events = query.all()
            
            # Проверяем пересечение временных интервалов
            for conflicting in conflicting_events:
                if conflicting.time_slot:
                    if ValidationService.check_time_overlap(
                        time_slot.time_start,
                        time_slot.time_end,
                        conflicting.time_slot.time_start,
                        conflicting.time_slot.time_end,
                    ):
                        return ConflictError(
                            f"Поток уже имеет занятие в пересекающееся время (событие #{conflicting.id}, {conflicting.time_slot.time_start.strftime('%H:%M')}-{conflicting.time_slot.time_end.strftime('%H:%M')})",
                            "stream_conflict",
                        )

        return None

    @staticmethod
    def check_capacity(
        db: Session,
        room_id: int,
        group_ids: List[int],
        stream_ids: List[int],
    ) -> Optional[ConflictError]:
        """Проверка вместимости аудитории."""
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return None

        # Подсчет студентов (упрощенно: для MVP считаем по группам)
        total_students = 0

        if group_ids:
            groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
            # В MVP: предполагаем 25 студентов на группу (можно вынести в настройки)
            total_students += len(groups) * 25

        if stream_ids:
            # Для потоков считаем все группы в потоке
            from app.models.stream import StreamMember
            stream_members = (
                db.query(StreamMember)
                .filter(StreamMember.stream_id.in_(stream_ids))
                .all()
            )
            total_students += len(stream_members) * 25

        if total_students > room.capacity:
            return ConflictError(
                f"Аудитория не вмещает студентов: {total_students} > {room.capacity}",
                "capacity_exceeded",
            )

        return None

    @staticmethod
    def check_room_type(
        db: Session,
        room_id: int,
        work_kind_id: int,
    ) -> Optional[ConflictError]:
        """Проверка соответствия типа аудитории виду занятия."""
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return None

        from app.models import WorkKind

        work_kind = db.query(WorkKind).filter(WorkKind.id == work_kind_id).first()
        if not work_kind:
            return None

        # Простая эвристика: спортзал для физкультуры
        if work_kind.name.lower() in ["физкультура", "спорт"]:
            if "спорт" not in room.type.lower() and "sport" not in room.type.lower():
                return ConflictError(
                    f"Вид занятия '{work_kind.name}' требует спортивную аудиторию",
                    "room_type_mismatch",
                )

        return None

    @staticmethod
    def validate_event(
        db: Session,
        room_id: int,
        time_slot_id: int,
        lecturer_ids: List[int],
        group_ids: List[int],
        subgroup_ids: List[int],
        stream_ids: List[int],
        work_kind_id: int,
        exclude_event_id: Optional[int] = None,
    ) -> List[ConflictError]:
        """Полная валидация события."""
        errors = []

        # Проверка конфликтов
        room_error = ValidationService.check_room_conflict(
            db, room_id, time_slot_id, exclude_event_id
        )
        if room_error:
            errors.append(room_error)

        lecturer_error = ValidationService.check_lecturer_conflict(
            db, lecturer_ids, time_slot_id, exclude_event_id
        )
        if lecturer_error:
            errors.append(lecturer_error)

        group_error = ValidationService.check_group_conflict(
            db, group_ids, subgroup_ids, stream_ids, time_slot_id, exclude_event_id
        )
        if group_error:
            errors.append(group_error)

        # Проверка вместимости
        capacity_error = ValidationService.check_capacity(
            db, room_id, group_ids, stream_ids
        )
        if capacity_error:
            errors.append(capacity_error)

        # Проверка типа аудитории
        type_error = ValidationService.check_room_type(db, room_id, work_kind_id)
        if type_error:
            errors.append(type_error)

        return errors

