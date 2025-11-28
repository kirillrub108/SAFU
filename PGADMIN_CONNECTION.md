# Подключение к БД через pgAdmin

## Вариант 1: pgAdmin в Docker (рекомендуется)

### Шаг 1: Запуск pgAdmin

pgAdmin уже добавлен в `docker-compose.yml`. Просто запустите:

```powershell
docker compose up -d pgadmin
```

Или перезапустите все сервисы:

```powershell
docker compose up -d
```

### Шаг 2: Откройте pgAdmin в браузере

http://localhost:5050

### Шаг 3: Вход в pgAdmin

- **Email**: `admin@safu.ru` (или значение из `.env` переменной `PGADMIN_EMAIL`)
- **Password**: `admin` (или значение из `.env` переменной `PGADMIN_PASSWORD`)

### Шаг 4: Добавление сервера

1. Правой кнопкой на **Servers** → **Register** → **Server**

2. Вкладка **General**:
   - **Name**: `SAFU Database` (любое имя)

3. Вкладка **Connection**:
   - **Host name/address**: `db` (имя сервиса из docker-compose)
   - **Port**: `5432`
   - **Maintenance database**: `safu_timetable`
   - **Username**: `safu`
   - **Password**: `safu_password`
   - ✅ **Save password** (чтобы не вводить каждый раз)

4. Нажмите **Save**

### Готово!

Теперь вы можете просматривать и редактировать базу данных через pgAdmin.

---

## Вариант 2: Внешний pgAdmin (установлен локально)

Если у вас уже установлен pgAdmin на компьютере:

### Параметры подключения:

- **Host**: `localhost` (или `127.0.0.1`)
- **Port**: `5432`
- **Database**: `safu_timetable`
- **Username**: `safu`
- **Password**: `safu_password`

### Шаги:

1. Откройте pgAdmin
2. Правой кнопкой на **Servers** → **Register** → **Server**
3. Вкладка **General**:
   - **Name**: `SAFU Database`
4. Вкладка **Connection**:
   - **Host name/address**: `localhost`
   - **Port**: `5432`
   - **Maintenance database**: `safu_timetable`
   - **Username**: `safu`
   - **Password**: `safu_password`
   - ✅ **Save password**
5. Нажмите **Save**

---

## Вариант 3: DBeaver, DataGrip или другой клиент

Используйте те же параметры:

```
Host: localhost
Port: 5432
Database: safu_timetable
Username: safu
Password: safu_password
```

---

## Проверка подключения

После подключения вы должны увидеть:

- ✅ **Databases** → `safu_timetable`
- ✅ **Schemas** → `public`
- ✅ **Tables**: 
  - `buildings`
  - `rooms`
  - `lecturers`
  - `groups`
  - `subgroups`
  - `streams`
  - `disciplines`
  - `work_kinds`
  - `time_slots`
  - `events`
  - `event_lecturers`
  - `event_groups`
  - `event_subgroups`
  - `event_streams`
  - `change_log`
  - `attachments`
  - `calendar_subscriptions`

---

## Изменение настроек pgAdmin

Если хотите изменить email/пароль для pgAdmin, добавьте в `.env`:

```env
PGADMIN_EMAIL=your@email.com
PGADMIN_PASSWORD=your_password
PGADMIN_PORT=5050
```

Затем пересоздайте контейнер:

```powershell
docker compose down pgadmin
docker compose up -d pgadmin
```

---

## Полезные SQL запросы

### Просмотр всех событий

```sql
SELECT 
    e.id,
    d.name as discipline,
    wk.name as work_kind,
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
WHERE e.status = 'scheduled'
ORDER BY ts.date, ts.pair_number;
```

### Просмотр расписания группы

```sql
SELECT 
    ts.date,
    ts.pair_number,
    d.name as discipline,
    wk.name as work_kind,
    r.number as room,
    b.name as building,
    l.fio as lecturer
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

### Статистика по группам

```sql
SELECT 
    g.code,
    g.name,
    COUNT(DISTINCT e.id) as events_count
FROM groups g
LEFT JOIN event_groups eg ON g.id = eg.group_id
LEFT JOIN events e ON eg.event_id = e.id AND e.status = 'scheduled'
GROUP BY g.id, g.code, g.name
ORDER BY g.code;
```

