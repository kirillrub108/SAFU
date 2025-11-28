"""Модели SQLAlchemy."""
from app.models.building import Building
from app.models.room import Room
from app.models.lecturer import Lecturer
from app.models.group import Group, Subgroup
from app.models.stream import Stream, StreamMember
from app.models.discipline import Discipline
from app.models.work_kind import WorkKind
from app.models.time_slot import TimeSlot
from app.models.event import (
    Event,
    EventLecturer,
    EventGroup,
    EventSubgroup,
    EventStream,
)
from app.models.change_log import ChangeLog
from app.models.attachment import Attachment
from app.models.calendar_subscription import CalendarSubscription

__all__ = [
    "Building",
    "Room",
    "Lecturer",
    "Group",
    "Subgroup",
    "Stream",
    "StreamMember",
    "Discipline",
    "WorkKind",
    "TimeSlot",
    "Event",
    "EventLecturer",
    "EventGroup",
    "EventSubgroup",
    "EventStream",
    "ChangeLog",
    "Attachment",
    "CalendarSubscription",
]

