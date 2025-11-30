import { EventDetail } from '../lib/api'

interface EventCardProps {
  event: EventDetail
  onClick?: () => void
}

export default function EventCard({ event, onClick }: EventCardProps) {
  const color = event.work_kind?.color_hex || '#6c757d'
  const hasConflict = event.has_conflict || false

  // Форматируем время безопасно (ожидаем формат HH:mm)
  const formatTime = (timeStr: string | undefined) => {
    if (!timeStr) return ''
    // Если время уже в формате HH:mm, возвращаем как есть
    if (/^\d{2}:\d{2}$/.test(timeStr)) {
      return timeStr
    }
    // Иначе пытаемся извлечь часы и минуты
    try {
      const match = timeStr.match(/(\d{2}):(\d{2})/)
      if (match) {
        return `${match[1]}:${match[2]}`
      }
      return timeStr
    } catch {
      return timeStr
    }
  }

  return (
    <div
      className={`p-1.5 rounded cursor-pointer hover:shadow-md transition-all border-l-2 ${
        hasConflict ? 'ring-1 ring-red-500 ring-opacity-50' : ''
      }`}
      style={{
        backgroundColor: hasConflict ? `${color}25` : `${color}15`,
        borderLeft: `3px solid ${hasConflict ? '#ef4444' : color}`,
      }}
      onClick={onClick}
      title={hasConflict ? '⚠️ Конфликт расписания: пересекающиеся пары' : undefined}
    >
      {/* Заголовок с дисциплиной */}
      <div className="font-bold text-xs md:text-sm mb-1 flex items-start gap-1" style={{ color }}>
        {hasConflict && <span className="text-red-600 text-sm shrink-0">⚠️</span>}
        <span className="break-words leading-tight line-clamp-2">{event.discipline?.name || 'Дисциплина'}</span>
      </div>
      
      {/* Вид занятия */}
      <div className="text-gray-700 text-xs mb-1 font-medium leading-tight line-clamp-1">
        {event.work_kind?.name || ''}
      </div>
      
      {/* Время (скрыто на мобильных, т.к. показывается слева) */}
      <div className="hidden md:block text-gray-600 text-xs mb-1 font-medium">
        {event.time_slot && (
          <>
            {formatTime(event.time_slot.time_start)}-{formatTime(event.time_slot.time_end)}
          </>
        )}
      </div>
      
      {/* Аудитория */}
      {event.room && (
        <div
          className="text-gray-700 text-xs mb-1 flex items-center gap-0.5 w-full"
          title={
            event.room.building
              ? `Ауд. ${event.room.number} (${event.room.building.name})`
              : `Ауд. ${event.room.number}`
          }
        >
          <span className="text-xs shrink-0">📍</span>
          <span className="font-semibold shrink-0">Ауд. {event.room.number}</span>
          {event.room.building && (
            <span className="text-gray-500 text-xs truncate" title={event.room.building.name}>
              ({event.room.building.name.length > 15 ? event.room.building.name.substring(0, 15) + '...' : event.room.building.name})
            </span>
          )}
        </div>
      )}
      
      {/* Преподаватели */}
      {event.lecturers && event.lecturers.length > 0 && (
        <div className="text-gray-600 text-xs mb-1 flex items-start gap-0.5">
          <span className="text-xs shrink-0 leading-tight">👤</span>
          <span className="break-words leading-tight line-clamp-1">
            {event.lecturers.map((l) => l.fio).join(', ')}
          </span>
        </div>
      )}
      
      {/* Группы */}
      {event.groups && event.groups.length > 0 && (
        <div className="text-gray-500 text-xs mt-1 pt-1 border-t border-gray-200 line-clamp-1">
          <span className="text-xs">👥</span>{' '}
          {event.groups.map((g) => g.code).join(', ')}
        </div>
      )}
    </div>
  )
}

