# САФУ Расписание - MVP

Производственный MVP системы расписания для САФУ с современной архитектурой, готовой для масштабирования.

## Технологический стек

### Backend
- **FastAPI** (Python 3.12) - современный веб-фреймворк
- **SQLAlchemy** + **Pydantic v2** - ORM и валидация данных
- **Alembic** - миграции БД
- **PostgreSQL 16** - основная БД
- **Redis** - кэширование
- **pytest** - тестирование

### Frontend
- **React 18** + **TypeScript** + **Vite** - UI фреймворк
- **Zustand** - управление состоянием
- **TanStack Query** - работа с API
- **Tailwind CSS** - стилизация
- **React Router** - маршрутизация

### DevOps
- **Docker Compose** - оркестрация сервисов
- **Makefile** - команды разработки
- **GitHub Actions** (CI) - автоматизация тестов

## Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- Make (Linux/Mac) или PowerShell (Windows)

### Установка и запуск

1. **Клонируйте репозиторий** (если еще не сделано)

2. **Настройте переменные окружения** (опционально)
   ```bash
   # Linux/Mac
   cp .env.example .env
   # Windows PowerShell
   Copy-Item .env.example .env
   # Отредактируйте .env при необходимости
   ```

3. **Соберите и запустите сервисы**

   **Linux/Mac:**
   ```bash
   make build
   make up
   ```

   **Windows PowerShell:**
   ```powershell
   .\build.ps1 build
   .\build.ps1 up
   ```

   **Или напрямую через Docker Compose:**
   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Примените миграции**

   **Linux/Mac:**
   ```bash
   make migrate
   ```

   **Windows PowerShell:**
   ```powershell
   .\build.ps1 migrate
   ```

   **Или напрямую:**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

5. **Заполните тестовыми данными**

   **Linux/Mac:**
   ```bash
   make seed
   ```

   **Windows PowerShell:**
   ```powershell
   .\build.ps1 seed
   ```

   **Или напрямую:**
   ```bash
   docker compose exec backend python -m app.seeds.main
   ```

6. **Откройте в браузере**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

> **Для Windows пользователей:** См. также [QUICKSTART.md](QUICKSTART.md) для подробных инструкций.

## Команды Make

- `make build` - собрать Docker образы
- `make up` - запустить все сервисы
- `make down` - остановить все сервисы
- `make migrate` - применить миграции БД
- `make seed` - заполнить БД тестовыми данными
- `make test` - запустить тесты
- `make fmt` - отформатировать код (black, isort)
- `make lint` - проверить код линтером
- `make clean` - удалить контейнеры и volumes
- `make logs` - показать логи всех сервисов

## API Endpoints

### Справочники
- `GET /api/buildings` - список корпусов
- `GET /api/rooms` - список аудиторий
- `GET /api/lecturers` - список преподавателей
- `GET /api/disciplines` - список дисциплин
- `GET /api/groups` - список групп
- `GET /api/streams` - список потоков
- `GET /api/work-kinds` - виды занятий

### Расписание
- `GET /api/timetable?date_from&date_to&group_id&lecturer_id&room_id&building_id&stream_id` - расписание с фильтрами
- `GET /api/timetable/day/{date}` - расписание на день (YYYY-MM-DD)
- `GET /api/timetable/week/{year}/{week}` - расписание на неделю
- `GET /api/timetable/group/{id}` - расписание группы
- `GET /api/timetable/lecturer/{id}` - расписание преподавателя

### События
- `POST /api/events` - создать событие
- `PUT /api/events/{id}` - обновить событие
- `DELETE /api/events/{id}` - удалить событие (soft delete)

### История
- `GET /api/events/{id}/history` - история изменений события
- `GET /api/changelog?entity=event&actor&date_from&date_to` - журнал изменений

### Календарь (ICS)
- `GET /api/calendar/ics?group_id={id}` - ICS для группы
- `GET /api/calendar/ics?lecturer_id={id}` - ICS для преподавателя
- `GET /api/calendar/ics?stream_id={id}` - ICS для потока
- `GET /api/calendar/subscribe?filter_kind={kind}&filter_id={id}` - создать подписку

### Импорт
- `POST /api/import/html` - импорт HTML расписания
- `GET /api/import/status` - статус последнего импорта

### Поиск
- `GET /api/search?q={query}` - поиск по ФИО, дисциплине, аудитории, адресу

## Frontend Routes

- `/` - главная страница (выбор роли, быстрый поиск)
- `/timetable` - расписание (недели/дни, фильтры)
- `/timetable/group/:id` - расписание группы
- `/timetable/lecturer/:id` - расписание преподавателя
- `/admin/history` - история изменений (админ)
- `/admin/import` - импорт HTML (админ)
- `/calendar/subscriptions` - подписки на календарь

## Цвета видов занятий

- **Лекция** (lecture): `#28a745` (зеленый)
- **Практика** (practice): `#ffc107` (желтый)
- **Лабораторная** (lab): `#17a2b8` (голубой)
- **Аттестация** (attestation): `#dc3545` (красный)

## Валидация конфликтов

Система проверяет:
- Пересечение аудиторий в одно время
- Пересечение преподавателей (не может вести два занятия одновременно)
- Пересечение групп/подгрупп/потоков
- Вместимость аудитории
- Соответствие типа аудитории виду занятия
- Географические предупреждения (подряд пары в разных корпусах)

## Импорт HTML

Система поддерживает импорт из текущего HTML-расписания:
- Парсинг дней/дат, пар, времени
- Распознавание вида занятия, дисциплины, преподавателя
- Обработка групп/подгрупп/потоков
- Нормализация аудиторий (включая диапазоны типа "305-309")
- Отчет о распознавании и проблемах

## Тестирование

```bash
make test
```

Тесты покрывают:
- Валидацию конфликтов (аудитории, преподаватели, группы)
- Парсер HTML
- Генерацию ICS
- API endpoints

## Разработка

### Backend
```bash
# Форматирование
make fmt

# Линтинг
make lint

# Тесты
make test
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Структура проекта

```
safu-timetable/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Конфигурация
│   │   ├── db/           # БД сессии
│   │   ├── models/       # SQLAlchemy модели
│   │   ├── schemas/      # Pydantic схемы
│   │   ├── services/     # Бизнес-логика
│   │   ├── validators/   # Валидация
│   │   ├── seeds/        # Тестовые данные
│   │   └── tests/        # Тесты
│   ├── alembic/          # Миграции
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React компоненты
│   │   ├── pages/        # Страницы
│   │   ├── hooks/        # Custom hooks
│   │   ├── store/        # Zustand store
│   │   └── styles/       # Стили
│   └── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env
└── README.md
```

## Лицензия

Внутренний проект САФУ.

