"""API для потоков."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import Stream, StreamCreate
from app.models import Stream as StreamModel, StreamMember

router = APIRouter(prefix="/api/streams", tags=["streams"])


@router.get("", response_model=List[Stream])
def get_streams(db: Session = Depends(get_db)):
    """Получить список потоков."""
    return db.query(StreamModel).filter(StreamModel.active == True).all()


@router.post("", response_model=Stream)
def create_stream(stream: StreamCreate, db: Session = Depends(get_db)):
    """Создать поток."""
    db_stream = StreamModel(name=stream.name, active=stream.active)
    db.add(db_stream)
    db.flush()

    if stream.group_ids:
        for group_id in stream.group_ids:
            member = StreamMember(stream_id=db_stream.id, group_id=group_id)
            db.add(member)

    db.commit()
    db.refresh(db_stream)
    return db_stream


@router.get("/{stream_id}", response_model=Stream)
def get_stream(stream_id: int, db: Session = Depends(get_db)):
    """Получить поток по ID."""
    return db.query(StreamModel).filter(StreamModel.id == stream_id).first()

