"""API для избранного."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.schemas import Favorite, FavoriteCreate
from app.models import User, Favorite as FavoriteModel

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


@router.get("", response_model=List[Favorite])
def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Получить список избранного пользователя."""
    return db.query(FavoriteModel).filter(FavoriteModel.user_id == current_user.id).all()


@router.post("", response_model=Favorite)
def create_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Создать избранное."""
    favorite = FavoriteModel(
        user_id=current_user.id,
        name=favorite_data.name,
        filters=favorite_data.filters,
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Удалить избранное."""
    favorite = db.query(FavoriteModel).filter(
        FavoriteModel.id == favorite_id,
        FavoriteModel.user_id == current_user.id,
    ).first()
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Избранное не найдено",
        )
    db.delete(favorite)
    db.commit()
    return {"message": "Избранное удалено"}

