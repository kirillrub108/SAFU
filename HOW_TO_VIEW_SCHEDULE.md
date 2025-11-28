# Как посмотреть занятия и расписание

## Способ 1: Через веб-интерфейс (Frontend)

### Вариант A: Список всех групп

1. Откройте http://localhost:5173
2. Нажмите на **"Группы"** в меню или **"Все группы"** на главной
3. Выберите нужную группу (например, 521428)
4. Откроется расписание этой группы

### Вариант B: Поиск

1. На главной странице введите в поиск:
   - Код группы (например, `521428`)
   - ФИО преподавателя (например, `Минеева`)
   - Название дисциплины
2. Выберите из результатов

### Вариант C: Фильтры на странице расписания

1. Перейдите на страницу **"Расписание"**
2. Используйте фильтры:
   - **Группа** - выберите из списка
   - **Дата от / до** - укажите период
   - **Преподаватель** - выберите из списка
   - **Корпус** - выберите здание
3. Расписание обновится автоматически

---

## Способ 2: Через API (для разработчиков)

### Получить все события

```bash
GET http://localhost:8000/api/timetable
```

### Расписание конкретной группы

```bash
GET http://localhost:8000/api/timetable?group_id=1
```

Или через специальный endpoint:

```bash
GET http://localhost:8000/api/timetable/group/1
```

### Расписание на период

```bash
GET http://localhost:8000/api/timetable?date_from=2025-11-17&date_to=2025-11-22
```

### Расписание преподавателя

```bash
GET http://localhost:8000/api/timetable?lecturer_id=1
```

Или:

```bash
GET http://localhost:8000/api/timetable/lecturer/1
```

### Пример через curl

```powershell
# Все события
curl http://localhost:8000/api/timetable

# Группа 521428 (нужно узнать ID группы)
curl http://localhost:8000/api/timetable?group_id=1

# На неделю
curl "http://localhost:8000/api/timetable?date_from=2025-11-17&date_to=2025-11-22"
```

### Через браузер

Откройте в браузере:
- http://localhost:8000/api/timetable
- http://localhost:8000/api/timetable/group/1
- http://localhost:8000/api/timetable?date_from=2025-11-17&date_to=2025-11-22

### Swagger UI (интерактивная документация)

1. Откройте http://localhost:8000/docs
2. Найдите endpoint `/api/timetable`
3. Нажмите **"Try it out"**
4. Заполните параметры (group_id, date_from, date_to и т.д.)
5. Нажмите **"Execute"**

---

## Способ 3: Через SQL в pgAdmin

### Подключитесь к БД (см. PGADMIN_CONNECTION.md)

### Просмотр всех событий

```sql
SELECT 
    e.id,
    d.name as discipline,
    wk.name as work_kind,
    g.code as group_code,
    l.fio as lecturer,
    r.number as room,
    b.name as building,
    ts.date,
    ts.pair_number,
    ts.time_start,
    ts.time_end
FROM events e
JOIN disciplines d ON e.discipline_id = d.id
JOIN work_kinds wk ON e.work_kind_id = wk.id
JOIN rooms r ON e.room_id = r.id
JOIN buildings b ON r.building_id = b.id
JOIN time_slots ts ON e.time_slot_id = ts.id
LEFT JOIN event_groups eg ON e.id = eg.event_id
LEFT JOIN groups g ON eg.group_id = g.id
LEFT JOIN event_lecturers el ON e.id = el.event_id
LEFT JOIN lecturers l ON el.lecturer_id = l.id
WHERE e.status = 'scheduled'
ORDER BY ts.date, ts.pair_number;
```

### Расписание конкретной группы

```sql
SELECT 
    ts.date,
    ts.pair_number,
    ts.time_start,
    ts.time_end,
    d.name as discipline,
    wk.name as work_kind,
    wk.color_hex,
    l.fio as lecturer,
    r.number as room,
    b.name as building,
    b.address
FROM events e
JOIN event_groups eg ON e.id = eg.event_id
JOIN groups g ON eg.group_id = g.id
JOIN disciplines d ON e.discipline_id = d.id
JOIN work_kinds wk ON e.work_kind_id = wk.id
JOIN rooms r ON e.room_id = r.id
JOIN buildings b ON r.building_id = b.id
JOIN time_slots ts ON e.time_slot_id = ts.id
LEFT JOIN event_lecturers el ON e.id = el.event_id
LEFT JOIN lecturers l ON el.lecturer_id = l.id
WHERE g.code = '521428'
  AND e.status = 'scheduled'
ORDER BY ts.date, ts.pair_number;
```

### Список всех групп с количеством занятий

```sql
SELECT 
    g.id,
    g.code,
    g.name,
    COUNT(DISTINCT e.id) as events_count
FROM groups g
LEFT JOIN event_groups eg ON g.id = eg.group_id
LEFT JOIN events e ON eg.event_id = e.id AND e.status = 'scheduled'
GROUP BY g.id, g.code, g.name
ORDER BY g.code;
```

### Расписание на конкретную дату

```sql
SELECT 
    ts.date,
    ts.pair_number,
    ts.time_start,
    ts.time_end,
    d.name as discipline,
    wk.name as work_kind,
    g.code as group_code,
    l.fio as lecturer,
    r.number as room
FROM events e
JOIN time_slots ts ON e.time_slot_id = ts.id
JOIN disciplines d ON e.discipline_id = d.id
JOIN work_kinds wk ON e.work_kind_id = wk.id
JOIN rooms r ON e.room_id = r.id
LEFT JOIN event_groups eg ON e.id = eg.event_id
LEFT JOIN groups g ON eg.group_id = g.id
LEFT JOIN event_lecturers el ON e.id = el.event_id
LEFT JOIN lecturers l ON el.lecturer_id = l.id
WHERE ts.date = '2025-11-17'
  AND e.status = 'scheduled'
ORDER BY ts.pair_number;
```

### Расписание преподавателя

```sql
SELECT 
    ts.date,
    ts.pair_number,
    ts.time_start,
    ts.time_end,
    d.name as discipline,
    wk.name as work_kind,
    g.code as group_code,
    r.number as room,
    b.name as building
FROM events e
JOIN event_lecturers el ON e.id = el.event_id
JOIN lecturers l ON el.lecturer_id = l.id
JOIN disciplines d ON e.discipline_id = d.id
JOIN work_kinds wk ON e.work_kind_id = wk.id
JOIN rooms r ON e.room_id = r.id
JOIN buildings b ON r.building_id = b.id
JOIN time_slots ts ON e.time_slot_id = ts.id
LEFT JOIN event_groups eg ON e.id = eg.event_id
LEFT JOIN groups g ON eg.group_id = g.id
WHERE l.fio = 'Минеева Т.А.'
  AND e.status = 'scheduled'
ORDER BY ts.date, ts.pair_number;
```

---

## Как узнать ID группы/преподавателя

### Через API

```bash
# Все группы
GET http://localhost:8000/api/groups

# Все преподаватели
GET http://localhost:8000/api/lecturers
```

### Через SQL

```sql
-- Список групп
SELECT id, code, name FROM groups ORDER BY code;

-- Список преподавателей
SELECT id, fio, chair FROM lecturers ORDER BY fio;
```

---

## Быстрые ссылки

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Все группы**: http://localhost:5173/groups
- **Расписание**: http://localhost:5173/timetable
- **API расписание**: http://localhost:8000/api/timetable

