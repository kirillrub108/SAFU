"""Seeds для корпусов."""
from sqlalchemy.orm import Session
from app.models import Building


def seed_buildings(db: Session) -> list[Building]:
    """Заполнение корпусов."""
    buildings_data = [
        {
            "name": "корп. А",
            "code": "A",
            "address": "ул. Капитана Воронина, д.6",
            "lat": 64.5361,
            "lon": 40.5153,
        },
        {
            "name": "корп. Б",
            "code": "B",
            "address": "ул. Капитана Воронина, д.6а",
            "lat": 64.5365,
            "lon": 40.5155,
        },
        {
            "name": "спортзал-Г",
            "code": "G",
            "address": "ул. Капитана Воронина, д.6а в",
            "lat": 64.5363,
            "lon": 40.5154,
        },
        {
            "name": "Карла Маркса, 36",
            "code": "KM36",
            "address": "ул. Карла Маркса, д.36",
            "lat": 64.5370,
            "lon": 40.5160,
        },
    ]

    buildings = []
    for data in buildings_data:
        building = db.query(Building).filter(Building.code == data["code"]).first()
        if not building:
            building = Building(**data)
            db.add(building)
            buildings.append(building)
        else:
            buildings.append(building)

    db.flush()
    return buildings

