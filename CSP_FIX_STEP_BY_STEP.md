# Пошаговое исправление CSP ошибки

## Анализ проблемы

### Шаг 1: Понимание ошибки

**Ошибка:**
```
Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'self' 'wasm-unsafe-eval' 'inline-speculation-rules' chrome-extension://95fd8110-c545-4e51-81da-e9455f7b1a56/"
```

**Анализ:**
1. Расширение браузера (chrome-extension://95fd8110-c545-4e51-81da-e9455f7b1a56/) пытается выполнить inline скрипт
2. Текущий CSP не разрешает `'unsafe-inline'` для скриптов
3. Расширение устанавливает свой CSP, который конфликтует с нашим

### Шаг 2: Источники CSP

CSP может устанавливаться из нескольких источников:
1. **Meta tag в HTML** - имеет приоритет
2. **HTTP заголовки от сервера** - устанавливаются Vite dev server
3. **Расширения браузера** - могут переопределять CSP

### Шаг 3: Решение

Нужно разрешить:
- `'unsafe-inline'` для скриптов (для Vite HMR и расширений)
- `'unsafe-eval'` для динамического кода
- `chrome-extension:` для расширений браузера
- WebSocket соединения для HMR

---

## Исправления

### ✅ Шаг 1: Добавлен meta tag CSP в index.html

**Файл:** `frontend/index.html`

**Изменение:**
Добавлен meta tag с полной CSP политикой:
```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval' chrome-extension: https:; object-src 'none'; base-uri 'self'; connect-src 'self' http://localhost:8000 http://127.0.0.1:8000 ws://localhost:5173 ws://127.0.0.1:5173; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;">
```

**Что разрешено:**
- `script-src`: 'self', 'unsafe-inline', 'unsafe-eval', 'wasm-unsafe-eval', chrome-extension:, https:
- `connect-src`: 'self', localhost:8000, ws:// для HMR
- `style-src`: 'self', 'unsafe-inline' (для Tailwind)
- `img-src`: 'self', data:, https:
- `font-src`: 'self', data:

### ✅ Шаг 2: Обновлен CSP в vite.config.ts

**Файл:** `frontend/vite.config.ts`

**Изменение:**
Обновлены HTTP заголовки с более полной CSP политикой:
```typescript
headers: {
  'Content-Security-Policy': [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval' chrome-extension: https:",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self' data:",
    "connect-src 'self' http://localhost:8000 http://127.0.0.1:8000 ws://localhost:5173 ws://127.0.0.1:5173",
    "object-src 'none'",
    "base-uri 'self'",
  ].join('; '),
}
```

---

## Применение исправлений

### Шаг 1: Перезапустите frontend

```powershell
# Если запущено в Docker
docker compose restart frontend

# Или если запущено локально
# Остановите dev server (Ctrl+C) и запустите снова
npm run dev
```

### Шаг 2: Очистите кеш браузера

1. Откройте DevTools (F12)
2. Правый клик на кнопке обновления
3. Выберите "Очистить кеш и жесткая перезагрузка"

Или используйте:
- **Chrome/Edge**: Ctrl+Shift+Delete → Очистить кеш
- **Firefox**: Ctrl+Shift+Delete → Очистить кеш

### Шаг 3: Проверьте результат

1. Откройте консоль браузера (F12)
2. Проверьте, что нет CSP ошибок
3. Приложение должно работать нормально

---

## Проверка работы

### Проверка 1: Консоль браузера

Откройте консоль (F12) и проверьте:
- ✅ Нет ошибок CSP
- ✅ Нет ошибок загрузки скриптов
- ✅ HMR работает (hot module replacement)

### Проверка 2: Network tab

В DevTools → Network:
- ✅ Запросы к API проходят успешно
- ✅ WebSocket соединения для HMR работают
- ✅ Нет блокированных ресурсов

### Проверка 3: Функциональность

- ✅ Страницы загружаются
- ✅ API запросы работают
- ✅ Расписание отображается

---

## Если проблема сохраняется

### Вариант 1: Отключите расширение

Если ошибка все еще появляется:
1. Определите расширение по ID: `chrome-extension://95fd8110-c545-4e51-81da-e9455f7b1a56/`
2. Откройте `chrome://extensions/`
3. Найдите расширение и временно отключите его
4. Перезагрузите страницу

### Вариант 2: Используйте режим инкогнито

1. Откройте Chrome в режиме инкогнито (Ctrl+Shift+N)
2. Откройте приложение
3. Расширения по умолчанию отключены в инкогнито

### Вариант 3: Проверьте другие расширения

Некоторые расширения могут устанавливать свой CSP:
- Ad blockers
- Privacy extensions
- Security extensions

Попробуйте отключить их по очереди.

---

## Безопасность

⚠️ **Важно для production:**

Текущая конфигурация разрешает `'unsafe-inline'` и `'unsafe-eval'`, что **небезопасно для production**.

Для production рекомендуется:
1. Использовать nonce для inline скриптов
2. Убрать `'unsafe-inline'` и `'unsafe-eval'`
3. Использовать хеши для inline скриптов
4. Ограничить `connect-src` только нужными доменами

Пример для production:
```html
<meta http-equiv="Content-Security-Policy" content="script-src 'self' 'nonce-{RANDOM_NONCE}'; ...">
```

---

## Резюме

✅ **Исправлено:**
1. Добавлен meta tag CSP в `index.html`
2. Обновлен CSP в `vite.config.ts`
3. Разрешены необходимые директивы для работы с расширениями

✅ **Результат:**
- CSP ошибки должны исчезнуть
- Расширения браузера могут работать
- HMR работает корректно
- API запросы проходят успешно

