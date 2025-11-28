"""Pydantic схемы для API."""
from app.schemas.building import Building, BuildingCreate, BuildingUpdate
from app.schemas.room import Room, RoomCreate, RoomUpdate
from app.schemas.lecturer import Lecturer, LecturerCreate, LecturerUpdate
from app.schemas.group import Group, GroupCreate, Subgroup, SubgroupCreate
from app.schemas.stream import Stream, StreamCreate, StreamMember
from app.schemas.discipline import Discipline, DisciplineCreate
from app.schemas.work_kind import WorkKind, WorkKindCreate
from app.schemas.time_slot import TimeSlot, TimeSlotCreate
from app.schemas.event import (
    Event,
    EventCreate,
    EventUpdate,
    EventDetail,
    EventLecturer,
    EventGroup,
    EventSubgroup,
    EventStream,
)
from app.schemas.change_log import ChangeLog, ChangeLogFilter
from app.schemas.calendar import CalendarSubscription, CalendarSubscriptionCreate

__all__ = [
    "Building",
    "BuildingCreate",
    "BuildingUpdate",
    "Room",
    "RoomCreate",
    "RoomUpdate",
    "Lecturer",
    "LecturerCreate",
    "LecturerUpdate",
    "Group",
    "GroupCreate",
    "Subgroup",
    "SubgroupCreate",
    "Stream",
    "StreamCreate",
    "StreamMember",
    "Discipline",
    "DisciplineCreate",
    "WorkKind",
    "WorkKindCreate",
    "TimeSlot",
    "TimeSlotCreate",
    "Event",
    "EventCreate",
    "EventUpdate",
    "EventDetail",
    "EventLecturer",
    "EventGroup",
    "EventSubgroup",
    "EventStream",
    "ChangeLog",
    "ChangeLogFilter",
    "CalendarSubscription",
    "CalendarSubscriptionCreate",
]

