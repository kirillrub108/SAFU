"""Seeds для видов занятий."""
from sqlalchemy.orm import Session
from app.models import WorkKind


def seed_work_kinds(db: Session) -> list[WorkKind]:
    """Заполнение видов занятий."""
    work_kinds_data = [
        {"name": "Лекция", "color_hex": "#28a745"},
        {"name": "Практика", "color_hex": "#ffc107"},
        {"name": "Лабораторная", "color_hex": "#17a2b8"},
        {"name": "Аттестация", "color_hex": "#dc3545"},
    ]

    work_kinds = []
    for data in work_kinds_data:
        work_kind = db.query(WorkKind).filter(WorkKind.name == data["name"]).first()
        if not work_kind:
            work_kind = WorkKind(**data)
            db.add(work_kind)
            work_kinds.append(work_kind)
        else:
            work_kinds.append(work_kind)

    db.flush()
    return work_kinds

