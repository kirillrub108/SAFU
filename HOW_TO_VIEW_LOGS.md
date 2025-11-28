# Как посмотреть логи

## Основные команды

### 1. Логи всех сервисов
```powershell
docker compose logs
```

### 2. Логи конкретного сервиса
```powershell
# Backend
docker compose logs backend

# Frontend
docker compose logs frontend

# База данных
docker compose logs db

# Redis
docker compose logs redis
```

### 3. Последние N строк (tail)
```powershell
# Последние 50 строк backend
docker compose logs backend --tail 50

# Последние 100 строк всех сервисов
docker compose logs --tail 100
```

### 4. Логи в реальном времени (follow)
```powershell
# Следить за логами backend в реальном времени
docker compose logs -f backend

# Следить за всеми сервисами
docker compose logs -f
```

### 5. Логи с временными метками
```powershell
docker compose logs -t backend
```

### 6. Логи за определенный период
```powershell
# Логи за последний час
docker compose logs --since 1h backend

# Логи за последние 30 минут
docker compose logs --since 30m backend
```

## Поиск ошибок

### Найти ошибки в логах
```powershell
# Ищем "error" или "Error" в логах backend
docker compose logs backend | Select-String -Pattern "error" -CaseSensitive:$false

# Ищем "500" или "Exception"
docker compose logs backend | Select-String -Pattern "500|Exception"
```

### Сохранить логи в файл
```powershell
# Сохранить логи backend в файл
docker compose logs backend > backend_logs.txt

# Сохранить с временными метками
docker compose logs -t backend > backend_logs_with_time.txt
```

## Исправленная ошибка

**Проблема**: `table name "time_slots" specified more than once`

**Причина**: В коде делался двойной `join(TimeSlot)` - один раз для `date_from`, второй раз для `date_to`.

**Решение**: Объединены условия фильтрации по дате - `join` делается только один раз, если есть хотя бы одно условие по дате.

**Файл**: `backend/app/api/routes/timetable.py`

## Проверка исправления

После исправления проверьте API:

```powershell
# Проверка через curl
curl http://localhost:8000/api/timetable?date_from=2024-11-18&date_to=2024-11-24

# Или через браузер
# http://localhost:8000/api/timetable?date_from=2024-11-18&date_to=2024-11-24
```

Если ошибка 500 все еще есть, проверьте логи:

```powershell
docker compose logs backend --tail 20
```

## Полезные команды для отладки

### Перезапустить сервис
```powershell
# Перезапустить backend
docker compose restart backend

# Перезапустить все сервисы
docker compose restart
```

### Войти в контейнер
```powershell
# Войти в контейнер backend
docker compose exec backend bash

# Выполнить команду в контейнере
docker compose exec backend python -c "print('Hello')"
```

### Проверить статус контейнеров
```powershell
docker compose ps
```

