"""Seeds для событий."""
from sqlalchemy.orm import Session
from datetime import date, time
from app.models import Event, TimeSlot
from app.models.event import EventLecturer, EventGroup, EventSubgroup, EventStream


def seed_events(
    db: Session,
    disciplines: list,
    work_kinds: list,
    rooms: list,
    lecturers: list,
    groups: list,
    streams: list,
) -> list[Event]:
    """Заполнение событий на неделю 17.11-22.11 и текущую неделю."""
    from datetime import datetime, timedelta
    
    # Получаем текущую неделю (понедельник)
    today = datetime.now().date()
    today_weekday = today.weekday()  # 0 = понедельник, 6 = воскресенье
    current_week_start = today - timedelta(days=today_weekday)
    
    # Создаем события на текущую неделю И на тестовую неделю 17-22 ноября 2025
    # Находим нужные сущности
    discipline_inf = next((d for d in disciplines if "Информатика" in d.name), None)
    discipline_mat = next((d for d in disciplines if "Математика" in d.name), None)
    discipline_fiz = next((d for d in disciplines if "Физика" in d.name), None)
    discipline_prog = next((d for d in disciplines if "Программирование" in d.name), None)
    discipline_fizra = next((d for d in disciplines if "Физическая культура" in d.name), None)

    work_kind_lecture = next((w for w in work_kinds if w.name == "Лекция"), None)
    work_kind_practice = next((w for w in work_kinds if w.name == "Практика"), None)
    work_kind_lab = next((w for w in work_kinds if w.name == "Лабораторная"), None)

    lecturer_min = next((l for l in lecturers if "Минеева" in l.fio), None)
    lecturer_prot = next((l for l in lecturers if "Протасова" in l.fio), None)
    lecturer_sl = next((l for l in lecturers if "Слуцков" in l.fio), None)
    lecturer_byk = next((l for l in lecturers if "Быков" in l.fio), None)

    group_521428 = next((g for g in groups if g.code == "521428"), None)
    stream_1 = streams[0] if streams else None

    room_301 = next((r for r in rooms if "301" in r.number), None)
    room_311 = next((r for r in rooms if r.number == "311"), None)
    room_319 = next((r for r in rooms if r.number == "319"), None)
    room_405 = next((r for r in rooms if r.number == "405"), None)
    room_sport = next((r for r in rooms if r.type == "sport"), None)

    # Время пар
    pair_times = {
        1: (time(8, 30), time(10, 0)),
        2: (time(10, 10), time(11, 40)),
        3: (time(12, 10), time(13, 40)),
        4: (time(14, 10), time(15, 40)),
        5: (time(16, 0), time(17, 30)),
    }

    # Функция для создания события
    def create_event_for_date(event_date, pair, discipline, work_kind, lecturer, room, group=None, stream=None):
        """Создает событие для указанной даты (проверяет на дубликаты)."""
        if not all([discipline, work_kind, room]):
            return None
            
        time_start, time_end = pair_times[pair]
        time_slot = (
            db.query(TimeSlot)
            .filter(
                TimeSlot.date == event_date,
                TimeSlot.pair_number == pair,
            )
            .first()
        )
        if not time_slot:
            time_slot = TimeSlot(
                date=event_date,
                pair_number=pair,
                time_start=time_start,
                time_end=time_end,
                timezone="Europe/Moscow",
            )
            db.add(time_slot)
            db.flush()

        # Проверяем, не существует ли уже такое событие
        existing_event = (
            db.query(Event)
            .filter(
                Event.discipline_id == discipline.id,
                Event.work_kind_id == work_kind.id,
                Event.room_id == room.id,
                Event.time_slot_id == time_slot.id,
                Event.status == "scheduled",
            )
            .first()
        )
        
        if existing_event:
            # Если событие уже существует, проверяем связи
            # Если нужно добавить группу/поток/преподавателя, добавляем их
            if group:
                existing_group = (
                    db.query(EventGroup)
                    .filter(
                        EventGroup.event_id == existing_event.id,
                        EventGroup.group_id == group.id,
                    )
                    .first()
                )
                if not existing_group:
                    db.add(EventGroup(event_id=existing_event.id, group_id=group.id))
            
            if stream:
                existing_stream = (
                    db.query(EventStream)
                    .filter(
                        EventStream.event_id == existing_event.id,
                        EventStream.stream_id == stream.id,
                    )
                    .first()
                )
                if not existing_stream:
                    db.add(EventStream(event_id=existing_event.id, stream_id=stream.id))
            
            if lecturer:
                existing_lecturer = (
                    db.query(EventLecturer)
                    .filter(
                        EventLecturer.event_id == existing_event.id,
                        EventLecturer.lecturer_id == lecturer.id,
                    )
                    .first()
                )
                if not existing_lecturer:
                    db.add(EventLecturer(event_id=existing_event.id, lecturer_id=lecturer.id))
            
            db.flush()
            return existing_event

        # Создаем новое событие
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
        if stream:
            db.add(EventStream(event_id=event.id, stream_id=stream.id))

        return event

    events = []
    
    # Создаем события на текущую неделю (понедельник + дни)
    # Исправляем: если сегодня воскресенье, weekDay = 6, нужно вычесть 6 дней
    today_weekday = today.weekday()  # 0 = понедельник, 6 = воскресенье
    current_week_start = today - timedelta(days=today_weekday)
    current_week_dates = [current_week_start + timedelta(days=i) for i in range(7)]
    
    # Понедельник текущей недели
    if group_521428 and discipline_inf and work_kind_lecture and room_301 and lecturer_min:
        evt = create_event_for_date(
            current_week_dates[0], 1, discipline_inf, work_kind_lecture, 
            lecturer_min, room_301, group=group_521428
        )
        if evt: events.append(evt)
    
    # Вторник текущей недели
    if group_521428 and discipline_mat and work_kind_practice and room_311 and lecturer_sl:
        evt = create_event_for_date(
            current_week_dates[1], 2, discipline_mat, work_kind_practice,
            lecturer_sl, room_311, group=group_521428
        )
        if evt: events.append(evt)
    
    # Среда текущей недели
    if group_521428 and discipline_prog and work_kind_lab and room_405 and lecturer_prot:
        evt = create_event_for_date(
            current_week_dates[2], 3, discipline_prog, work_kind_lab,
            lecturer_prot, room_405, group=group_521428
        )
        if evt: events.append(evt)
    
    # Четверг текущей недели
    if group_521428 and discipline_fiz and work_kind_lecture and room_319 and lecturer_byk:
        evt = create_event_for_date(
            current_week_dates[3], 1, discipline_fiz, work_kind_lecture,
            lecturer_byk, room_319, group=group_521428
        )
        if evt: events.append(evt)
    
    # Пятница текущей недели
    if group_521428 and discipline_inf and work_kind_practice and room_311 and lecturer_min:
        evt = create_event_for_date(
            current_week_dates[4], 2, discipline_inf, work_kind_practice,
            lecturer_min, room_311, group=group_521428
        )
        if evt: events.append(evt)

    # Также создаем события на тестовую неделю 17-22 ноября 2025
    events_data = [
        # Понедельник 17.11
        {
            "date": date(2025, 11, 17),
            "pair": 1,
            "discipline": discipline_inf,
            "work_kind": work_kind_lecture,
            "lecturer": lecturer_min,
            "room": room_301,
            "group": group_521428,
        },
        {
            "date": date(2025, 11, 17),
            "pair": 2,
            "discipline": discipline_mat,
            "work_kind": work_kind_practice,
            "lecturer": lecturer_sl,
            "room": room_311,
            "group": group_521428,
        },
        {
            "date": date(2025, 11, 17),
            "pair": 3,
            "discipline": discipline_prog,
            "work_kind": work_kind_lab,
            "lecturer": lecturer_prot,
            "room": room_405,
            "group": group_521428,
        },
        # Вторник 18.11
        {
            "date": date(2025, 11, 18),
            "pair": 1,
            "discipline": discipline_fiz,
            "work_kind": work_kind_lecture,
            "lecturer": lecturer_byk,
            "room": room_319,
            "group": group_521428,
        },
        {
            "date": date(2025, 11, 18),
            "pair": 2,
            "discipline": discipline_inf,
            "work_kind": work_kind_practice,
            "lecturer": lecturer_min,
            "room": room_311,
            "group": group_521428,
        },
        # Среда 19.11
        {
            "date": date(2025, 11, 19),
            "pair": 1,
            "discipline": discipline_fizra,
            "work_kind": work_kind_practice,
            "lecturer": None,
            "room": room_sport,
            "stream": stream_1,
        },
        {
            "date": date(2025, 11, 19),
            "pair": 3,
            "discipline": discipline_mat,
            "work_kind": work_kind_lecture,
            "lecturer": lecturer_sl,
            "room": room_301,
            "stream": stream_1,
        },
        # Четверг 20.11
        {
            "date": date(2025, 11, 20),
            "pair": 2,
            "discipline": discipline_prog,
            "work_kind": work_kind_practice,
            "lecturer": lecturer_prot,
            "room": room_405,
            "group": group_521428,
        },
        {
            "date": date(2025, 11, 20),
            "pair": 4,
            "discipline": discipline_fiz,
            "work_kind": work_kind_lab,
            "lecturer": lecturer_byk,
            "room": room_311,
            "group": group_521428,
        },
        # Пятница 21.11
        {
            "date": date(2025, 11, 21),
            "pair": 1,
            "discipline": discipline_inf,
            "work_kind": work_kind_lecture,
            "lecturer": lecturer_min,
            "room": room_301,
            "stream": stream_1,
        },
        {
            "date": date(2025, 11, 21),
            "pair": 2,
            "discipline": discipline_mat,
            "work_kind": work_kind_practice,
            "lecturer": lecturer_sl,
            "room": room_311,
            "group": group_521428,
        },
        # Суббота 22.11
        {
            "date": date(2025, 11, 22),
            "pair": 1,
            "discipline": discipline_prog,
            "work_kind": work_kind_lab,
            "lecturer": lecturer_prot,
            "room": room_405,
            "group": group_521428,
        },
    ]

    # Создаем события на тестовую неделю 17-22 ноября 2025
    for data in events_data:
        if not all([data["discipline"], data["work_kind"], data["room"]]):
            continue

        evt = create_event_for_date(
            data["date"],
            data["pair"],
            data["discipline"],
            data["work_kind"],
            data.get("lecturer"),
            data["room"],
            group=data.get("group"),
            stream=data.get("stream")
        )
        if evt:
            events.append(evt)

    db.flush()
    return events

