"""Seeds для преподавателей."""
from sqlalchemy.orm import Session
from app.models import Lecturer


def seed_lecturers(db: Session) -> list[Lecturer]:
    """Заполнение преподавателей."""
    lecturers_data = [
        {"fio": "Минеева Т.А.", "chair": "Кафедра информатики"},
        {"fio": "Протасова С.В.", "chair": "Кафедра информатики"},
        {"fio": "Слуцков В.А.", "chair": "Кафедра математики"},
        {"fio": "Быков А.В.", "chair": "Кафедра физики"},
        {"fio": "Иванов И.И.", "chair": "Кафедра информатики"},
        {"fio": "Петрова П.П.", "chair": "Кафедра математики"},
        {"fio": "Сидоров С.С.", "chair": "Кафедра физики"},
    ]

    lecturers = []
    for data in lecturers_data:
        lecturer = db.query(Lecturer).filter(Lecturer.fio == data["fio"]).first()
        if not lecturer:
            lecturer = Lecturer(**data)
            db.add(lecturer)
            lecturers.append(lecturer)
        else:
            lecturers.append(lecturer)

    db.flush()
    return lecturers

