"""Сервис парсинга HTML расписания."""
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, time
from sqlalchemy.orm import Session
from app.models import (
    Building,
    Room,
    Lecturer,
    Group,
    Subgroup,
    Stream,
    Discipline,
    WorkKind,
    TimeSlot,
    Event,
)
from app.models.event import EventLecturer, EventGroup, EventSubgroup, EventStream


class ParseResult:
    """Результат парсинга."""

    def __init__(self):
        self.events_created = 0
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.entities_created: Dict[str, int] = {
            "buildings": 0,
            "rooms": 0,
            "lecturers": 0,
            "groups": 0,
            "subgroups": 0,
            "streams": 0,
            "disciplines": 0,
        }


class ParserService:
    """Сервис парсинга HTML расписания."""

    # Время пар (для САФУ, можно настроить)
    PAIR_TIMES = {
        1: (time(8, 30), time(10, 0)),
        2: (time(10, 10), time(11, 40)),
        3: (time(12, 10), time(13, 40)),
        4: (time(14, 10), time(15, 40)),
        5: (time(16, 0), time(17, 30)),
        6: (time(17, 40), time(19, 10)),
        7: (time(19, 20), time(20, 50)),
        8: (time(21, 0), time(22, 30)),
    }

    @staticmethod
    def parse_html(db: Session, html_content: str) -> ParseResult:
        """Парсинг HTML расписания."""
        result = ParseResult()
        soup = BeautifulSoup(html_content, "lxml")

        # Здесь должна быть логика парсинга конкретного формата HTML
        # Для MVP создадим упрощенный парсер, который ищет таблицы/списки

        # Пример: поиск таблиц с расписанием
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 5:
                    # Попытка распарсить строку
                    try:
                        ParserService._parse_row(db, cells, result)
                    except Exception as e:
                        result.errors.append(
                            {"row": str(row), "error": str(e), "type": "parse_error"}
                        )

        return result

    @staticmethod
    def _parse_row(db: Session, cells: List, result: ParseResult):
        """Парсинг одной строки расписания."""
        # Упрощенная логика - в реальности нужен анализ конкретного формата
        # Пример структуры: дата | пара | дисциплина | вид | преподаватель | группа | аудитория

        if len(cells) < 6:
            return

        # Извлечение данных (пример)
        date_str = cells[0].get_text(strip=True)
        pair_str = cells[1].get_text(strip=True)
        discipline_str = cells[2].get_text(strip=True)
        work_kind_str = cells[3].get_text(strip=True)
        lecturer_str = cells[4].get_text(strip=True)
        group_str = cells[5].get_text(strip=True)
        room_str = cells[6].get_text(strip=True) if len(cells) > 6 else ""

        # Нормализация и создание сущностей
        discipline = ParserService._get_or_create_discipline(db, discipline_str, result)
        work_kind = ParserService._get_or_create_work_kind(db, work_kind_str, result)
        lecturer = ParserService._get_or_create_lecturer(db, lecturer_str, result)
        group = ParserService._get_or_create_group(db, group_str, result)
        room, building = ParserService._get_or_create_room(
            db, room_str, result
        )  # Может быть диапазон

        # Парсинг даты и пары
        try:
            event_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except:
            result.errors.append({"field": "date", "value": date_str, "type": "date_parse"})
            return

        try:
            pair_number = int(pair_str)
        except:
            result.errors.append({"field": "pair", "value": pair_str, "type": "pair_parse"})
            return

        # Создание временного слота
        if pair_number in ParserService.PAIR_TIMES:
            time_start, time_end = ParserService.PAIR_TIMES[pair_number]
            time_slot = ParserService._get_or_create_time_slot(
                db, event_date, pair_number, time_start, time_end
            )
        else:
            result.errors.append(
                {"field": "pair", "value": pair_number, "type": "invalid_pair"}
            )
            return

        # Создание события
        if discipline and work_kind and room and time_slot:
            event = Event(
                discipline_id=discipline.id,
                work_kind_id=work_kind.id,
                room_id=room.id,
                time_slot_id=time_slot.id,
                status="scheduled",
            )
            db.add(event)
            db.flush()

            if lecturer:
                db.add(EventLecturer(event_id=event.id, lecturer_id=lecturer.id))
            if group:
                db.add(EventGroup(event_id=event.id, group_id=group.id))

            result.events_created += 1

    @staticmethod
    def _get_or_create_discipline(db: Session, name: str, result: ParseResult) -> Optional[Discipline]:
        """Получение или создание дисциплины."""
        if not name:
            return None
        discipline = db.query(Discipline).filter(Discipline.name == name).first()
        if not discipline:
            discipline = Discipline(name=name, short_name=name[:20] if len(name) > 20 else name)
            db.add(discipline)
            db.flush()
            result.entities_created["disciplines"] += 1
        return discipline

    @staticmethod
    def _get_or_create_work_kind(db: Session, name: str, result: ParseResult) -> Optional[WorkKind]:
        """Получение или создание вида занятия."""
        if not name:
            return None

        # Нормализация названия
        name_lower = name.lower()
        color_map = {
            "лекция": "#28a745",
            "практика": "#ffc107",
            "лабораторная": "#17a2b8",
            "аттестация": "#dc3545",
        }
        color = color_map.get(name_lower, "#6c757d")

        work_kind = db.query(WorkKind).filter(WorkKind.name == name).first()
        if not work_kind:
            work_kind = WorkKind(name=name, color_hex=color)
            db.add(work_kind)
            db.flush()
        return work_kind

    @staticmethod
    def _get_or_create_lecturer(db: Session, fio: str, result: ParseResult) -> Optional[Lecturer]:
        """Получение или создание преподавателя."""
        if not fio:
            return None
        lecturer = db.query(Lecturer).filter(Lecturer.fio == fio).first()
        if not lecturer:
            lecturer = Lecturer(fio=fio)
            db.add(lecturer)
            db.flush()
            result.entities_created["lecturers"] += 1
        return lecturer

    @staticmethod
    def _get_or_create_group(db: Session, code: str, result: ParseResult) -> Optional[Group]:
        """Получение или создание группы."""
        if not code:
            return None

        # Обработка подгрупп (например, "521428-1")
        if "-" in code:
            parts = code.split("-")
            group_code = parts[0]
            subgroup_code = code
        else:
            group_code = code
            subgroup_code = None

        group = db.query(Group).filter(Group.code == group_code).first()
        if not group:
            group = Group(code=group_code, name=group_code)
            db.add(group)
            db.flush()
            result.entities_created["groups"] += 1

        # Создание подгруппы если нужно
        if subgroup_code and "-" in code:
            subgroup = db.query(Subgroup).filter(Subgroup.code == subgroup_code).first()
            if not subgroup:
                subgroup = Subgroup(group_id=group.id, code=subgroup_code)
                db.add(subgroup)
                db.flush()
                result.entities_created["subgroups"] += 1

        return group

    @staticmethod
    def _get_or_create_room(
        db: Session, room_str: str, result: ParseResult
    ) -> Tuple[Optional[Room], Optional[Building]]:
        """Получение или создание аудитории."""
        if not room_str:
            return None, None

        # Обработка диапазонов типа "305-309", "301-302"
        # Для MVP берем первую аудиторию
        if "-" in room_str and room_str.replace("-", "").isdigit():
            room_number = room_str.split("-")[0]
            result.warnings.append(
                {
                    "type": "room_range",
                    "value": room_str,
                    "resolved": f"Использована аудитория {room_number}",
                }
            )
        else:
            room_number = room_str

        # Поиск корпуса (упрощенно - по умолчанию корп. А)
        building = db.query(Building).filter(Building.code == "A").first()
        if not building:
            building = Building(
                name="корп. А",
                code="A",
                address="ул. Капитана Воронина, д.6",
            )
            db.add(building)
            db.flush()
            result.entities_created["buildings"] += 1

        # Поиск аудитории
        room = (
            db.query(Room)
            .filter(Room.building_id == building.id, Room.number == room_number)
            .first()
        )
        if not room:
            room = Room(
                building_id=building.id,
                number=room_number,
                capacity=30,  # По умолчанию
                type="lecture",
            )
            db.add(room)
            db.flush()
            result.entities_created["rooms"] += 1

        return room, building

    @staticmethod
    def _get_or_create_time_slot(
        db: Session, event_date: date, pair_number: int, time_start: time, time_end: time
    ) -> TimeSlot:
        """Получение или создание временного слота."""
        time_slot = (
            db.query(TimeSlot)
            .filter(
                TimeSlot.date == event_date,
                TimeSlot.pair_number == pair_number,
            )
            .first()
        )
        if not time_slot:
            time_slot = TimeSlot(
                date=event_date,
                pair_number=pair_number,
                time_start=time_start,
                time_end=time_end,
                timezone="Europe/Moscow",
            )
            db.add(time_slot)
            db.flush()
        return time_slot

