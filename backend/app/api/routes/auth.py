"""API для авторизации."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.models import User, UserRole, NotificationSettings
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя."""
    # Проверяем, существует ли пользователь с таким email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    # Создаем пользователя
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        fio=user_data.fio,
        role=user_data.role,
        group_id=user_data.group_id,
        lecturer_id=user_data.lecturer_id,
    )
    db.add(db_user)
    db.flush()

    # Создаем настройки уведомлений
    notification_settings = NotificationSettings(user_id=db_user.id)
    db.add(notification_settings)

    # Если это студент с группой, создаем избранное для его группы
    if user_data.role == UserRole.STUDENT and user_data.group_id:
        from app.models import Favorite
        favorite = Favorite(
            user_id=db_user.id,
            name="Моя группа",
            filters={"group_id": user_data.group_id},
        )
        db.add(favorite)

    db.commit()
    db.refresh(db_user)

    # Создаем токен
    access_token = create_access_token(data={"sub": db_user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(db_user),
    }


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Вход в систему."""
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен",
        )

    # Создаем токен
    access_token = create_access_token(data={"sub": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Получить информацию о текущем пользователе."""
    return UserResponse.model_validate(current_user)

