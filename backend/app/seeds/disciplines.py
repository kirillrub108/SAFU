"""Seeds для дисциплин."""
from sqlalchemy.orm import Session
from app.models import Discipline


def seed_disciplines(db: Session) -> list[Discipline]:
    """Заполнение дисциплин."""
    disciplines_data = [
        {"name": "Информатика", "short_name": "Инф"},
        {"name": "Математика", "short_name": "Мат"},
        {"name": "Физика", "short_name": "Физ"},
        {"name": "Программирование", "short_name": "Прог"},
        {"name": "Базы данных", "short_name": "БД"},
        {"name": "Физическая культура", "short_name": "Физ-ра"},
    ]

    disciplines = []
    for data in disciplines_data:
        discipline = db.query(Discipline).filter(Discipline.name == data["name"]).first()
        if not discipline:
            discipline = Discipline(**data)
            db.add(discipline)
            disciplines.append(discipline)
        else:
            disciplines.append(discipline)

    db.flush()
    return disciplines

