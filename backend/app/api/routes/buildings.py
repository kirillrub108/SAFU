"""API для корпусов."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Building, BuildingCreate, BuildingUpdate
from app.models import Building as BuildingModel

router = APIRouter(prefix="/api/buildings", tags=["buildings"])


@router.get("", response_model=List[Building])
def get_buildings(db: Session = Depends(get_db)):
    """Получить список корпусов."""
    return db.query(BuildingModel).all()


@router.post("", response_model=Building)
def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    """Создать корпус."""
    db_building = BuildingModel(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


@router.get("/{building_id}", response_model=Building)
def get_building(building_id: int, db: Session = Depends(get_db)):
    """Получить корпус по ID."""
    return db.query(BuildingModel).filter(BuildingModel.id == building_id).first()

