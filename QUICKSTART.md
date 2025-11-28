# Быстрый старт для Windows

## Предварительные требования
- Docker Desktop для Windows
- PowerShell

## Установка и запуск

### Вариант 1: Использование PowerShell скрипта

```powershell
# Сборка образов
.\build.ps1 build

# Запуск сервисов
.\build.ps1 up

# Применение миграций
.\build.ps1 migrate

# Заполнение тестовыми данными
.\build.ps1 seed
```

### Вариант 2: Использование Docker Compose напрямую

```powershell
# Сборка образов
docker compose build

# Запуск сервисов
docker compose up -d

# Применение миграций
docker compose exec backend alembic upgrade head

# Заполнение тестовыми данными
docker compose exec backend python -m app.seeds.main
``` 

## Доступ к приложению

После запуска:
- **Frontend**: http://localhost: работалое 5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Полезные команды

```powershell
# Просмотр логов
docker compose logs -f

# Остановка сервисов
docker compose down

# Перезапуск сервисов
docker compose restart

# Очистка (удаление контейнеров и volumes)
docker compose down -v
```

## Решение проблем

### Если порты заняты
Измените порты в файле `.env`:
```
BACKEND_PORT=8001
FRONTEND_PORT=5174
```

### Если контейнеры не запускаются
Проверьте логи:
```powershell
docker compose logs backend
docker compose logs frontend
docker compose logs db
```

### Пересоздание БД
```powershell
docker compose down -v
docker compose up -d db
.\build.ps1 migrate
.\build.ps1 seed
```

