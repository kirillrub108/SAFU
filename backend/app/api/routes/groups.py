"""API для групп."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Group, GroupCreate, Subgroup, SubgroupCreate
from app.models import Group as GroupModel, Subgroup as SubgroupModel

router = APIRouter(prefix="/api/groups", tags=["groups"])


@router.get("", response_model=List[Group])
def get_groups(db: Session = Depends(get_db)):
    """Получить список групп."""
    return db.query(GroupModel).filter(GroupModel.active == True).all()


@router.post("", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    """Создать группу."""
    db_group = GroupModel(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


@router.get("/{group_id}", response_model=Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    """Получить группу по ID."""
    return db.query(GroupModel).filter(GroupModel.id == group_id).first()


@router.get("/{group_id}/subgroups", response_model=List[Subgroup])
def get_subgroups(group_id: int, db: Session = Depends(get_db)):
    """Получить подгруппы группы."""
    return db.query(SubgroupModel).filter(SubgroupModel.group_id == group_id).all()

