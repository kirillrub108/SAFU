"""Seeds для факультетов."""
from sqlalchemy.orm import Session
from app.models import Faculty


def seed_faculties(db: Session) -> list[Faculty]:
    """Заполнение факультетов."""
    faculties_data = [
        {"name": "Гуманитарный институт (г. Северодвинск)"},
        {"name": "Научный отдел филиала САФУ в г. Северодвинске"},
        {"name": "Институт судостроения и морской арктической техники (Севмашвтуз) (г. Северодвинск)"},
    ]

    faculties = []
    for data in faculties_data:
        faculty = db.query(Faculty).filter(Faculty.name == data["name"]).first()
        if not faculty:
            faculty = Faculty(**data)
            db.add(faculty)
            faculties.append(faculty)
        else:
            faculties.append(faculty)

    db.flush()
    return faculties

