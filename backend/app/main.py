"""Главный файл FastAPI приложения."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import (
    buildings,
    rooms,
    lecturers,
    groups,
    streams,
    disciplines,
    work_kinds,
    timetable,
    events,
    history,
    calendar,
    import_route,
    search,
    auth,
    favorites,
    notifications,
    faculties,
)

app = FastAPI(
    title="САФУ Расписание API",
    description="API для системы расписания САФУ",
    version="0.1.0",
)

# CORS
# В development режиме разрешаем все origins для удобства разработки
if settings.ENVIRONMENT == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешаем все origins в development
        allow_credentials=False,  # Нельзя использовать credentials с allow_origins=["*"]
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

# Подключение роутов
app.include_router(auth.router)
app.include_router(buildings.router)
app.include_router(rooms.router)
app.include_router(lecturers.router)
app.include_router(faculties.router)
app.include_router(groups.router)
app.include_router(streams.router)
app.include_router(disciplines.router)
app.include_router(work_kinds.router)
app.include_router(timetable.router)
app.include_router(events.router)
app.include_router(history.router)
app.include_router(calendar.router)
app.include_router(import_route.router)
app.include_router(search.router)
app.include_router(favorites.router)
app.include_router(notifications.router)


@app.get("/")
def root():
    """Корневой эндпоинт."""
    return {"message": "САФУ Расписание API", "version": "0.1.0"}


@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}

