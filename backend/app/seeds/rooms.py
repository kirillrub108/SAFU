"""Seeds для аудиторий."""
from sqlalchemy.orm import Session
from app.models import Room, Building


def seed_rooms(db: Session, buildings: list) -> list[Room]:
    """Заполнение аудиторий."""
    # Находим корпуса по коду
    building_a = next((b for b in buildings if b.code == "A"), None)
    building_b = next((b for b in buildings if b.code == "B"), None)
    building_g = next((b for b in buildings if b.code == "G"), None)

    rooms_data = [
        # Корпус А
        {"building": building_a, "number": "301-302", "capacity": 50, "type": "lecture"},
        {"building": building_a, "number": "305-309", "capacity": 60, "type": "lecture"},
        {"building": building_a, "number": "311", "capacity": 30, "type": "practice"},
        {"building": building_a, "number": "313a", "capacity": 25, "type": "practice"},
        {"building": building_a, "number": "319", "capacity": 40, "type": "lecture"},
        {"building": building_a, "number": "405", "capacity": 35, "type": "practice"},
        {"building": building_a, "number": "417-419", "capacity": 45, "type": "lecture"},
        {"building": building_a, "number": "308", "capacity": 30, "type": "practice"},
        {"building": building_a, "number": "202", "capacity": 20, "type": "practice", "features": {"name": "Проектный офис"}},
        {"building": building_a, "number": "216", "capacity": 30, "type": "practice"},
        {"building": building_a, "number": "218", "capacity": 30, "type": "practice"},
        # Корпус Б
        {"building": building_b, "number": "7", "capacity": 25, "type": "practice"},
        # Спортзал
        {"building": building_g, "number": "1", "capacity": 40, "type": "sport"},
    ]

    rooms = []
    for data in rooms_data:
        if not data["building"]:
            continue
        room = (
            db.query(Room)
            .filter(Room.building_id == data["building"].id, Room.number == data["number"])
            .first()
        )
        if not room:
            room_data = {k: v for k, v in data.items() if k != "building"}
            room = Room(building_id=data["building"].id, **room_data)
            db.add(room)
            rooms.append(room)
        else:
            rooms.append(room)

    db.flush()
    return rooms

