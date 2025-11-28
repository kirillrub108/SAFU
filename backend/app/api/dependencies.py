"""Зависимости для API."""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

# Для будущего использования с аутентификацией
# def get_current_user(...):
#     pass

