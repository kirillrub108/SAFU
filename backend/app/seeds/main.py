"""Главный файл для заполнения БД тестовыми данными."""
from app.db.session import SessionLocal
from app.seeds.buildings import seed_buildings
from app.seeds.rooms import seed_rooms
from app.seeds.lecturers import seed_lecturers
from app.seeds.groups import seed_groups
from app.seeds.streams import seed_streams
from app.seeds.disciplines import seed_disciplines
from app.seeds.work_kinds import seed_work_kinds
from app.seeds.events import seed_events


def main():
    """Заполнение БД."""
    db = SessionLocal()
    try:
        print("Заполнение корпусов...")
        buildings = seed_buildings(db)
        print(f"Создано корпусов: {len(buildings)}")

        print("Заполнение аудиторий...")
        rooms = seed_rooms(db, buildings)
        print(f"Создано аудиторий: {len(rooms)}")

        print("Заполнение видов занятий...")
        work_kinds = seed_work_kinds(db)
        print(f"Создано видов занятий: {len(work_kinds)}")

        print("Заполнение дисциплин...")
        disciplines = seed_disciplines(db)
        print(f"Создано дисциплин: {len(disciplines)}")

        print("Заполнение преподавателей...")
        lecturers = seed_lecturers(db)
        print(f"Создано преподавателей: {len(lecturers)}")

        print("Заполнение групп...")
        groups = seed_groups(db)
        print(f"Создано групп: {len(groups)}")

        print("Заполнение потоков...")
        streams = seed_streams(db, groups)
        print(f"Создано потоков: {len(streams)}")

        print("Заполнение событий...")
        events = seed_events(db, disciplines, work_kinds, rooms, lecturers, groups, streams)
        print(f"Создано событий: {len(events)}")

        db.commit()
        print("Заполнение завершено успешно!")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

