import { EventDetail } from '../lib/api'
import { useFiltersStore } from '../store/filters'

interface DebugInfoProps {
  events: EventDetail[] | undefined
}

export default function DebugInfo({ events }: DebugInfoProps) {
  const filters = useFiltersStore()
  
  // Показываем только для разработчиков
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  const isDeveloper = user?.role === 'developer'
  
  if (!isDeveloper) {
    return null
  }

  // Вычисляем диапазон недели для отображения
  const weekStart = filters.weekDate
  const weekEnd = new Date(weekStart)
  weekEnd.setDate(weekEnd.getDate() + 6)

  // Получаем уникальные даты из событий
  const uniqueDates = events
    ? [...new Set(events.map(e => e.time_slot?.date).filter(Boolean))]
    : []

  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded p-4 mb-4 text-xs">
      <h4 className="font-bold mb-2 text-yellow-800">🔍 Debug Info (только для разработки):</h4>
      <div className="space-y-2">
        <div>
          <strong className="text-yellow-800">Фильтры:</strong>
          <div className="ml-2 mt-1 space-y-1">
            <div>Даты запроса: <code className="bg-yellow-100 px-1 rounded">{filters.dateFrom}</code> - <code className="bg-yellow-100 px-1 rounded">{filters.dateTo}</code></div>
            <div>Неделя начинается: <code className="bg-yellow-100 px-1 rounded">{weekStart.toISOString().split('T')[0]}</code></div>
            <div>Неделя заканчивается: <code className="bg-yellow-100 px-1 rounded">{weekEnd.toISOString().split('T')[0]}</code></div>
            <div>Группа: {filters.groupId || 'не выбрана'}</div>
            <div>Преподаватель: {filters.lecturerId || 'не выбран'}</div>
          </div>
        </div>
        <div>
          <strong className="text-yellow-800">Данные:</strong>
          <div className="ml-2 mt-1 space-y-1">
            <div>Событий получено: <strong className="text-blue-600">{events?.length || 0}</strong></div>
            {uniqueDates.length > 0 && (
              <div>
                Уникальные даты в событиях: <code className="bg-yellow-100 px-1 rounded">{uniqueDates.join(', ')}</code>
              </div>
            )}
          </div>
        </div>
        {events && events.length > 0 && (
          <div>
            <strong className="text-yellow-800">Первые 3 события:</strong>
            <div className="ml-2 mt-1 space-y-1">
              {events.slice(0, 3).map((e) => (
                <div key={e.id} className="p-2 bg-yellow-100 rounded border border-yellow-300">
                  <div><strong>ID:</strong> {e.id}</div>
                  <div><strong>Дата:</strong> <code>{e.time_slot?.date}</code> | <strong>Пара:</strong> {e.time_slot?.pair_number}</div>
                  <div><strong>Дисциплина:</strong> {e.discipline?.name}</div>
                  <div><strong>Группы:</strong> {e.groups?.map(g => g.code).join(', ') || 'нет'}</div>
                  <div><strong>Аудитория:</strong> {e.room?.number || 'нет'}</div>
                </div>
              ))}
            </div>
          </div>
        )}
        {events && events.length === 0 && (
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-red-700">
            <strong>⚠️ События не найдены!</strong>
            <ul className="list-disc list-inside ml-2 mt-1 space-y-1">
              <li>Проверьте правильность дат в фильтрах</li>
              <li>Проверьте наличие событий в БД на эти даты</li>
              <li>Откройте консоль браузера (F12) для детальной информации</li>
              <li>Проверьте вкладку Network для запросов к API</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
