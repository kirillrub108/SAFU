# Запуск проекта САФУ Расписание с нуля

## Шаг 1: Проверка Docker

Убедитесь, что **Docker Desktop** запущен и работает:

```powershell
docker --version
docker compose version
```

Если Docker не запущен:
1. Откройте **Docker Desktop** из меню Пуск
2. Дождитесь полного запуска (иконка в трее станет зеленой)
3. Повторите проверку команд выше

## Шаг 2: Переход в директорию проекта

```powershell
cd C:\Users\Aser\Desktop\SAFU
```

## Шаг 3: Очистка (если нужно начать заново)

Если были старые контейнеры, удалите их:

```powershell
docker compose down -v
```

## Шаг 4: Автоматический запуск (рекомендуется)

Используйте готовый скрипт, который сделает всё автоматически:

```powershell
.\first-run.ps1
```

Скрипт выполнит:
1. ✅ Сборку Docker образов (~5-10 минут первый раз)
2. ✅ Запуск всех сервисов
3. ✅ Ожидание готовности БД
4. ✅ Применение миграций
5. ✅ Заполнение тестовыми данными

## Шаг 5: Ручной запуск (если скрипт не работает)

### 5.1. Сборка образов

```powershell
docker compose build
```

**Время:** 5-10 минут (первый раз)

### 5.2. Запуск сервисов

```powershell
docker compose up -d
```

### 5.3. Проверка статуса

```powershell
docker compose ps
```

Все сервисы должны быть в статусе "Up" или "healthy".

### 5.4. Применение миграций БД

Подождите 10-15 секунд после запуска, затем:

```powershell
docker compose exec backend alembic upgrade head
```

### 5.5. Заполнение тестовыми данными

```powershell
docker compose exec backend python -m app.seeds.main
```

Вы должны увидеть:
```
Заполнение корпусов...
Создано корпусов: 4
Заполнение аудиторий...
Создано аудиторий: 13
...
Заполнение завершено успешно!
```

## Шаг 6: Проверка работы

Откройте в браузере:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Что создается в тестовых данных

После выполнения `seed` в базе будет:

- ✅ **4 корпуса** (корп. А, корп. Б, спортзал-Г, Карла Маркса 36)
- ✅ **13 аудиторий** (301-302, 305-309, 311, 313a, 319, 405, 417-419, 308, 7, 202, 216, 218)
- ✅ **4 вида занятий** (Лекция, Практика, Лабораторная, Аттестация)
- ✅ **6 дисциплин** (Информатика, Математика, Физика, Программирование, Базы данных, Физкультура)
- ✅ **7 преподавателей** (Минеева Т.А., Протасова С.В., Слуцков В.А., Быков А.В., и др.)
- ✅ **5 групп** (521428, 521423, 521424, 521425, 521427)
- ✅ **Подгруппы** (521428-1, 521428-2)
- ✅ **1 поток** (521423, 521424, 521425, 521427, 521428)
- ✅ **12 событий** на неделю 17-22 ноября 2025

## Полезные команды

### Просмотр логов
```powershell
# Все сервисы
docker compose logs -f

# Конкретный сервис
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### Остановка сервисов
```powershell
docker compose down
```

### Перезапуск
```powershell
docker compose restart
```

### Полная переустановка (удалить всё и начать заново)
```powershell
docker compose down -v
docker compose build --no-cache
docker compose up -d
Start-Sleep -Seconds 15
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seeds.main
```

## Решение проблем

### Ошибка: "Docker не запущен"
- Откройте Docker Desktop
- Дождитесь полного запуска
- Проверьте: `docker ps`

### Ошибка: "Port already in use"
Измените порты в `.env`:
```
BACKEND_PORT=8001
FRONTEND_PORT=5174
```
Затем пересоздайте контейнеры:
```powershell
docker compose down
docker compose up -d
```

### Ошибка: "Container name already in use"
```powershell
docker compose down
docker compose up -d
```

### Миграции не применяются
```powershell
# Удалите volumes и пересоздайте
docker compose down -v
docker compose up -d db
Start-Sleep -Seconds 15
docker compose exec backend alembic upgrade head
```

### Frontend не открывается
Проверьте логи:
```powershell
docker compose logs frontend
```

Убедитесь, что контейнер запущен:
```powershell
docker compose ps frontend
```

## Быстрая команда для первого запуска

Скопируйте и выполните всё сразу:

```powershell
docker compose down -v
docker compose build
docker compose up -d
Start-Sleep -Seconds 15
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seeds.main
Write-Host "Готово! Откройте http://localhost:5173" -ForegroundColor Green
```

