"""API для уведомлений."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.schemas import Notification, NotificationSettings, NotificationSettingsUpdate
from app.models import User, Notification as NotificationModel, NotificationSettings as NotificationSettingsModel

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("", response_model=List[Notification])
def get_notifications(
    read: bool = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить уведомления пользователя."""
    query = db.query(NotificationModel).filter(NotificationModel.user_id == current_user.id)
    if read is not None:
        query = query.filter(NotificationModel.read == read)
    return query.order_by(NotificationModel.created_at.desc()).limit(100).all()


@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить количество непрочитанных уведомлений."""
    count = db.query(NotificationModel).filter(
        NotificationModel.user_id == current_user.id,
        NotificationModel.read == False,
    ).count()
    return {"count": count}


@router.post("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Отметить уведомление как прочитанное."""
    notification = db.query(NotificationModel).filter(
        NotificationModel.id == notification_id,
        NotificationModel.user_id == current_user.id,
    ).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено",
        )
    notification.read = True
    db.commit()
    return {"message": "Уведомление отмечено как прочитанное"}


@router.post("/mark-all-read")
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Отметить все уведомления как прочитанные."""
    db.query(NotificationModel).filter(
        NotificationModel.user_id == current_user.id,
        NotificationModel.read == False,
    ).update({"read": True})
    db.commit()
    return {"message": "Все уведомления отмечены как прочитанные"}


@router.get("/settings", response_model=NotificationSettings)
def get_notification_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить настройки уведомлений."""
    settings = db.query(NotificationSettingsModel).filter(
        NotificationSettingsModel.user_id == current_user.id,
    ).first()
    if not settings:
        # Создаем настройки по умолчанию
        settings = NotificationSettingsModel(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.put("/settings", response_model=NotificationSettings)
def update_notification_settings(
    settings_data: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Обновить настройки уведомлений."""
    settings = db.query(NotificationSettingsModel).filter(
        NotificationSettingsModel.user_id == current_user.id,
    ).first()
    if not settings:
        settings = NotificationSettingsModel(user_id=current_user.id, **settings_data.model_dump())
        db.add(settings)
    else:
        for key, value in settings_data.model_dump().items():
            setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings

