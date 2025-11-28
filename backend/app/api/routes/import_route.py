"""API для импорта."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.parser import ParserService
from app.services.cache import cache_service

router = APIRouter(prefix="/api/import", tags=["import"])

# Глобальная переменная для хранения статуса последнего импорта
_last_import_status = None


@router.post("/html")
def import_html(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Импорт HTML расписания."""
    global _last_import_status

    if not file.filename.endswith((".html", ".htm")):
        raise HTTPException(status_code=400, detail="Файл должен быть HTML")

    content = file.file.read().decode("utf-8")

    try:
        result = ParserService.parse_html(db, content)
        db.commit()

        _last_import_status = {
            "events_created": result.events_created,
            "errors": result.errors,
            "warnings": result.warnings,
            "entities_created": result.entities_created,
        }

        # Инвалидация кэша
        cache_service.invalidate_timetable_cache()

        return {
            "message": "Импорт завершен",
            "events_created": result.events_created,
            "errors_count": len(result.errors),
            "warnings_count": len(result.warnings),
            "entities_created": result.entities_created,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка импорта: {str(e)}")


@router.get("/status")
def get_import_status():
    """Получить статус последнего импорта."""
    global _last_import_status
    if _last_import_status is None:
        return {"message": "Импорт еще не выполнялся"}
    return _last_import_status

