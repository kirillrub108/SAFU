"""Модели SQLAlchemy."""
from app.models.building import Building
from app.models.room import Room
from app.models.lecturer import Lecturer
from app.models.faculty import Faculty
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
from app.models.user import User, UserRole
from app.models.favorite import Favorite
from app.models.notification import Notification, NotificationType, NotificationSettings

__all__ = [
    "Building",
    "Room",
    "Lecturer",
    "Faculty",
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
    "User",
    "UserRole",
    "Favorite",
    "Notification",
    "NotificationType",
    "NotificationSettings",
]

