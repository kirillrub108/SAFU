# Конфигурация CORS

## Настройка CORS для SAFU

CORS (Cross-Origin Resource Sharing) настроен для работы фронтенда с бекендом.

## Текущая конфигурация

### Development режим
В режиме разработки (`ENVIRONMENT=development`) разрешены **все origins** (`*`) для удобства разработки:
- Разрешены все методы HTTP
- Разрешены все заголовки
- `allow_credentials=False` (нельзя использовать с `allow_origins=["*"]`)

### Production режим
В production режиме используются только разрешенные origins из настроек:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)
- `http://127.0.0.1:5173`
- `http://127.0.0.1:3000`

## Файлы конфигурации

### Backend
- `backend/app/main.py` - настройка CORS middleware
- `backend/app/core/config.py` - список разрешенных origins

### Frontend
- `frontend/src/lib/api.ts` - базовый URL API

## Проверка работы CORS

### 1. Проверка через браузер
Откройте консоль браузера (F12) и проверьте:
- Нет ошибок CORS в консоли
- Запросы к API проходят успешно

### 2. Проверка через curl
```powershell
# Проверка OPTIONS запроса (preflight)
curl -X OPTIONS http://localhost:8000/api/timetable \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET" \
  -v

# Проверка GET запроса
curl http://localhost:8000/api/timetable \
  -H "Origin: http://localhost:5173" \
  -v
```

### 3. Проверка в Network tab
В DevTools → Network:
- Проверьте заголовки запросов
- Проверьте заголовки ответов (должны быть `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, etc.)

## Возможные проблемы

### Проблема 1: CORS ошибка в консоли
**Симптом**: `Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:5173' has been blocked by CORS policy`

**Решение**:
1. Убедитесь, что backend запущен
2. Проверьте, что `ENVIRONMENT=development` в docker-compose.yml
3. Перезапустите backend: `docker compose restart backend`

### Проблема 2: Preflight запрос не проходит
**Симптом**: OPTIONS запрос возвращает 405 или ошибку CORS

**Решение**:
- Убедитесь, что `allow_methods` включает `OPTIONS`
- Проверьте, что middleware добавлен до роутов

### Проблема 3: Credentials не работают
**Симптом**: Запросы с credentials не проходят

**Решение**:
- В development режиме `allow_credentials=False` (нельзя использовать с `allow_origins=["*"]`)
- В production используйте конкретные origins с `allow_credentials=True`

## Настройка для production

Для production измените в `backend/app/core/config.py`:

```python
CORS_ORIGINS: list[str] = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

И установите `ENVIRONMENT=production` в `.env` или docker-compose.yml.

## Дополнительная информация

- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

