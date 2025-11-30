"""Seeds для групп."""
from sqlalchemy.orm import Session
from app.models import Group, Subgroup, Faculty


def seed_groups(db: Session, faculties: list[Faculty]) -> list[Group]:
    """Заполнение групп."""
    # Находим факультеты
    faculty_sevmash = next((f for f in faculties if "Севмашвтуз" in f.name), None)
    
    groups_data = [
        {"code": "521428", "name": "521428", "year": 2, "faculty_id": None},
        {"code": "521423", "name": "521423", "year": 2, "faculty_id": None},
        {"code": "521424", "name": "521424", "year": 2, "faculty_id": None},
        {"code": "521425", "name": "521425", "year": 2, "faculty_id": None},
        {"code": "521427", "name": "521427", "year": 2, "faculty_id": None},
        # Институт судостроения и морской арктической техники (Севмашвтуз)
        {
            "code": "521523",
            "name": "521523 Кораблестроение, океанотехника и системотехника объектов морской инфраструктуры",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521524",
            "name": "521524 Машиностроение",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521525",
            "name": "521525 Управление в технических системах",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521527",
            "name": "521527 Конструкторско-технологическое обеспечение машиностроительных производств",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521528",
            "name": "521528 Информатика и вычислительная техника",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521530",
            "name": "521530 Проектирование и постройка кораблей, судов и объектов океанотехники",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521532",
            "name": "521532 Проектирование, изготовление и ремонт энергетических установок и систем автоматизации кораблей и судов",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521536",
            "name": "521536 Кораблестроение, океанотехника и системотехника объектов морской инфраструктуры",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "521539",
            "name": "521539 Проектирование и постройка кораблей, судов и объектов океанотехники",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        # Заочная форма обучения
        {
            "code": "523524",
            "name": "523524 Машиностроение (заочная форма)",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "523530",
            "name": "523530 Проектирование и постройка кораблей, судов и объектов океанотехники (заочная форма)",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
        {
            "code": "523532",
            "name": "523532 Проектирование, изготовление и ремонт энергетических установок и систем автоматизации кораблей и судов (заочная форма)",
            "year": 2,
            "faculty_id": faculty_sevmash.id if faculty_sevmash else None,
        },
    ]

    groups = []
    for data in groups_data:
        group = db.query(Group).filter(Group.code == data["code"]).first()
        if not group:
            group = Group(**data)
            db.add(group)
            groups.append(group)
        else:
            groups.append(group)

    db.flush()

    # Создаем подгруппы для 521428
    group_521428 = next((g for g in groups if g.code == "521428"), None)
    if group_521428:
        for i in [1, 2]:
            subgroup_code = f"521428-{i}"
            subgroup = db.query(Subgroup).filter(Subgroup.code == subgroup_code).first()
            if not subgroup:
                subgroup = Subgroup(group_id=group_521428.id, code=subgroup_code)
                db.add(subgroup)

    db.flush()
    return groups

