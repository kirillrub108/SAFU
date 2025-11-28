# Исправление отображения расписания

## Проблема
Пары не отображаются, потому что события созданы на 17-22 ноября 2025, а текущая неделя - ноябрь 2024.

## Решение

### Шаг 1: Обновить данные в БД

Перезапустите seed для создания событий на текущую неделю:

```powershell
docker compose exec backend python -m app.seeds.main
```

Это создаст события:
- На текущую неделю (автоматически определяется)
- На тестовую неделю 17-22 ноября 2025

### Шаг 2: Проверить отображение

1. Откройте http://localhost:5173/timetable
2. Должна отображаться текущая неделя
3. Если событий нет - переключитесь на неделю 17-22 ноября 2025

### Шаг 3: Отладка

Если пары все еще не отображаются:

1. Откройте консоль браузера (F12)
2. Проверьте Debug Info на странице расписания
3. Проверьте:
   - Правильность дат в фильтрах
   - Количество полученных событий
   - Формат дат в событиях

### Шаг 4: Проверка через API

Проверьте, что события есть в БД:

```powershell
# Все события
curl http://localhost:8000/api/timetable

# События на текущую неделю
curl "http://localhost:8000/api/timetable?date_from=2024-11-18&date_to=2024-11-24"
```

### Шаг 5: Проверка через SQL

В pgAdmin выполните:

```sql
SELECT 
    ts.date,
    ts.pair_number,
    d.name as discipline,
    g.code as group_code
FROM events e
JOIN time_slots ts ON e.time_slot_id = ts.id
JOIN disciplines d ON e.discipline_id = d.id
LEFT JOIN event_groups eg ON e.id = eg.event_id
LEFT JOIN groups g ON eg.group_id = g.id
WHERE e.status = 'scheduled'
ORDER BY ts.date, ts.pair_number
LIMIT 20;
```

## Что было исправлено

1. ✅ Добавлены события на текущую неделю в seeds
2. ✅ Улучшена обработка ошибок в компонентах
3. ✅ Добавлен DebugInfo компонент для отладки
4. ✅ Исправлена логика сравнения дат
5. ✅ Добавлено условие enabled в useTimetable

## Если проблема сохраняется

1. Проверьте логи backend:
   ```powershell
   docker compose logs backend
   ```

2. Проверьте, что даты в фильтрах правильные (откройте Debug Info)

3. Убедитесь, что события созданы:
   ```powershell
   docker compose exec backend python -c "from app.db.session import SessionLocal; from app.models import Event; db = SessionLocal(); print(f'Events: {db.query(Event).count()}')"
   ```

