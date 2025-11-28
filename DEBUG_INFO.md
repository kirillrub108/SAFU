# Отключение отладочной информации для разработчиков

## Обзор

В проекте реализована система логирования, которая автоматически скрывает отладочные сообщения в production-режиме, но оставляет их видимыми в режиме разработки.

## Как это работает

### Frontend

В проекте используется утилита `logger` (`frontend/src/utils/logger.ts`), которая:

- **В режиме разработки** (`development`): выводит все логи в консоль браузера
- **В production-режиме**: скрывает `log`, `warn`, `info`, `debug`, но **всегда показывает ошибки** (`error`)

### Использование

Вместо прямого использования `console.log()` используйте `logger`:

```typescript
import { logger } from '../utils/logger'

// Вместо console.log()
logger.log('Информационное сообщение')

// Вместо console.warn()
logger.warn('Предупреждение')

// Вместо console.error()
logger.error('Ошибка') // Всегда видна, даже в production

// Вместо console.info()
logger.info('Информация')

// Вместо console.debug()
logger.debug('Отладочное сообщение')
```

## Отключение Debug Info на странице

Компонент `DebugInfo` автоматически скрывается в production-режиме:

```typescript
// frontend/src/components/DebugInfo.tsx
if (import.meta.env.PROD) {
  return null
}
```

Это означает, что желтый блок с отладочной информацией будет виден только в режиме разработки.

## Режимы работы

### Режим разработки (Development)

- **Определение**: `import.meta.env.DEV === true` или `import.meta.env.MODE === 'development'`
- **Логирование**: Все логи видны в консоли
- **Debug Info**: Отображается на странице

### Production-режим

- **Определение**: `import.meta.env.PROD === true` или `import.meta.env.MODE === 'production'`
- **Логирование**: Только ошибки (`logger.error`) видны в консоли
- **Debug Info**: Скрыт

## Проверка текущего режима

Вы можете проверить текущий режим в коде:

```typescript
// Проверка режима разработки
const isDev = import.meta.env.DEV

// Проверка production-режима
const isProd = import.meta.env.PROD

// Текущий режим
const mode = import.meta.env.MODE // 'development' или 'production'
```

## Переменные окружения Vite

Vite автоматически определяет режим на основе:

1. Команды запуска:
   - `npm run dev` → `development`
   - `npm run build` → `production`

2. Переменной окружения `NODE_ENV`:
   - `NODE_ENV=development` → `development`
   - `NODE_ENV=production` → `production`

## Полное отключение логирования

Если вы хотите полностью отключить логирование (включая ошибки), измените `frontend/src/utils/logger.ts`:

```typescript
export const logger = {
  log: () => {}, // Ничего не делает
  warn: () => {},
  error: () => {}, // ВНИМАНИЕ: не рекомендуется отключать ошибки
  info: () => {},
  debug: () => {},
}
```

**⚠️ Внимание**: Не рекомендуется отключать `logger.error()`, так как это может скрыть критические проблемы.

## Проверка в браузере

1. **В режиме разработки**:
   - Откройте консоль браузера (F12)
   - Вы увидите все логи с префиксами `[API]`, `[Timetable]`, и т.д.
   - На странице расписания виден желтый блок "Debug Info"

2. **В production-режиме**:
   - Откройте консоль браузера (F12)
   - Вы увидите только ошибки (если они есть)
   - На странице расписания нет блока "Debug Info"

## Рекомендации

1. **Для разработки**: Используйте режим `development` - все логи видны
2. **Для тестирования**: Используйте режим `production` - проверьте, что нет лишних логов
3. **Для production**: Убедитесь, что сборка выполнена в режиме `production`

## Примеры

### Правильное использование

```typescript
// ✅ Хорошо - используем logger
logger.log('[Component] Initializing')
logger.error('[Component] Critical error occurred')

// ❌ Плохо - прямое использование console
console.log('[Component] Initializing') // Будет видно в production!
```

### Условное логирование

```typescript
if (import.meta.env.DEV) {
  logger.log('Это сообщение видно только в development')
}
```

## Дополнительная информация

- Документация Vite: https://vitejs.dev/guide/env-and-mode.html
- Все логи в проекте используют префиксы для удобной фильтрации в консоли

