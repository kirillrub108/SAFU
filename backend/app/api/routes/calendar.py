"""API для календаря (ICS)."""
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from typing import Optional
import secrets
from app.db.session import get_db
from app.services.ics import ICSService
from app.services.cache import cache_service
from app.models.calendar_subscription import CalendarSubscription, FilterKind

router = APIRouter(prefix="/api/calendar", tags=["calendar"])


@router.get("/ics")
def get_ics(
    group_id: Optional[int] = Query(None),
    lecturer_id: Optional[int] = Query(None),
    stream_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """Получить ICS календарь."""
    cache_key = f"calendar:ics:{group_id}:{lecturer_id}:{stream_id}"
    cached = cache_service.get(cache_key)
    if cached:
        ics_content = cached
    else:
        if group_id:
            ics_content = ICSService.generate_ics_for_group(db, group_id)
        elif lecturer_id:
            ics_content = ICSService.generate_ics_for_lecturer(db, lecturer_id)
        elif stream_id:
            ics_content = ICSService.generate_ics_for_stream(db, stream_id)
        else:
            return {"error": "Необходимо указать group_id, lecturer_id или stream_id"}

        cache_service.set(cache_key, ics_content, ttl=3600)

    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=schedule.ics"},
    )


@router.get("/subscribe")
def create_subscription(
    filter_kind: FilterKind = Query(...),
    filter_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Создать подписку на календарь."""
    token = secrets.token_urlsafe(32)
    subscription = CalendarSubscription(
        token=token,
        filter_kind=filter_kind,
        filter_id=filter_id,
        active=True,
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    # Формируем URL подписки
    base_url = "http://localhost:8000"  # TODO: из конфига
    ics_url = f"{base_url}/api/calendar/ics?{filter_kind.value}_id={filter_id}"

    return {
        "token": token,
        "ics_url": ics_url,
        "subscription_id": subscription.id,
    }

