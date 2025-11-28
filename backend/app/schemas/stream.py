"""Схемы для потоков."""
from pydantic import BaseModel
from typing import Optional, List


class StreamBase(BaseModel):
    name: str
    active: bool = True


class StreamCreate(StreamBase):
    group_ids: Optional[List[int]] = None


class Stream(StreamBase):
    id: int

    class Config:
        from_attributes = True


class StreamMember(BaseModel):
    stream_id: int
    group_id: int

    class Config:
        from_attributes = True

