import { EventDetail } from '../lib/api'
import EventCard from './EventCard'
import { format, parseISO, addDays, isToday, startOfWeek } from 'date-fns'
import { logger } from '../utils/logger'

interface ScheduleGridMobileProps {
  events: EventDetail[]
  weekStart: Date
}

// Время пар для САФУ
const PAIR_TIMES: Record<number, { start: string; end: string }> = {
  1: { start: '08:30', end: '10:00' },
  2: { start: '10:10', end: '11:40' },
  3: { start: '12:10', end: '13:40' },
  4: { start: '14:10', end: '15:40' },
  5: { start: '16:00', end: '17:30' },
  6: { start: '17:40', end: '19:10' },
  7: { start: '19:20', end: '20:50' },
  8: { start: '21:00', end: '22:30' },
}

const DAY_NAMES = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
const DAY_NAMES_SHORT = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

export default function ScheduleGridMobile({ events, weekStart }: ScheduleGridMobileProps) {
  // Получаем все дни недели (начинаем с понедельника)
  const weekStartDate = startOfWeek(weekStart, { weekStartsOn: 1 })
  const days = Array.from({ length: 7 }, (_, i) => addDays(weekStartDate, i))

  const getEventsForDay = (day: Date) => {
    if (!events || events.length === 0) return []
    
    const dayYear = day.getFullYear()
    const dayMonth = day.getMonth()
    const dayDate = day.getDate()
    
    const filtered = events.filter((event) => {
      if (!event.time_slot || !event.time_slot.date) {
        logger.warn('[ScheduleGridMobile] Event missing time_slot or date:', event)
        return false
      }
      
      try {
        const eventDateStr = event.time_slot.date
        const [year, month, date] = eventDateStr.split('-').map(Number)
        
        if (isNaN(year) || isNaN(month) || isNaN(date)) {
          logger.warn('[ScheduleGridMobile] Invalid date format:', eventDateStr)
          return false
        }
        
        return year === dayYear && month - 1 === dayMonth && date === dayDate
      } catch (e) {
        logger.error('[ScheduleGridMobile] Error parsing event date:', event.time_slot.date, e, event)
        return false
      }
    })
    
    // Сортируем события по номеру пары
    return filtered.sort((a, b) => {
      const pairA = a.time_slot?.pair_number || 0
      const pairB = b.time_slot?.pair_number || 0
      return pairA - pairB
    })
  }

  return (
    <div className="space-y-4">
      {days.map((day) => {
        const dayEvents = getEventsForDay(day)
        const isCurrentDay = isToday(day)
        // Преобразуем день недели: воскресенье (0) -> 6, остальные -> day - 1
        const dayOfWeek = day.getDay() === 0 ? 6 : day.getDay() - 1
        
        return (
          <div
            key={day.toISOString()}
            className={`bg-white rounded-lg shadow-sm border-2 overflow-hidden ${
              isCurrentDay ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
            }`}
          >
            {/* Заголовок дня */}
            <div
              className={`px-4 py-3 border-b ${
                isCurrentDay
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-lg">
                    {DAY_NAMES[dayOfWeek]}
                  </div>
                  <div
                    className={`text-sm ${
                      isCurrentDay ? 'text-blue-100' : 'text-gray-600'
                    }`}
                  >
                    {format(day, 'd MMMM yyyy')}
                  </div>
                </div>
                {isCurrentDay && (
                  <div className="px-3 py-1 bg-white text-blue-600 rounded-full text-xs font-semibold">
                    Сегодня
                  </div>
                )}
                {dayEvents.length > 0 && (
                  <div
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      isCurrentDay
                        ? 'bg-white text-blue-600'
                        : 'bg-blue-100 text-blue-700'
                    }`}
                  >
                    {dayEvents.length} {dayEvents.length === 1 ? 'занятие' : 'занятий'}
                  </div>
                )}
              </div>
            </div>

            {/* События дня */}
            <div className="p-3">
              {dayEvents.length > 0 ? (
                <div className="space-y-3">
                  {dayEvents.map((event) => {
                    const pairNumber = event.time_slot?.pair_number || 0
                    const pairTime = PAIR_TIMES[pairNumber]
                    
                    return (
                      <div key={event.id} className="flex gap-3">
                        {/* Время пары слева */}
                        <div className="flex-shrink-0 w-20 text-center">
                          <div className="bg-gray-100 rounded-lg p-2">
                            <div className="font-bold text-lg text-gray-800">
                              {pairNumber}
                            </div>
                            {pairTime && (
                              <div className="text-xs text-gray-600 mt-1">
                                <div>{pairTime.start}</div>
                                <div className="text-gray-400">-</div>
                                <div>{pairTime.end}</div>
                              </div>
                            )}
                          </div>
                        </div>
                        
                        {/* Карточка события */}
                        <div className="flex-1 min-w-0">
                          <EventCard event={event} />
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400">
                  <div className="text-4xl mb-2">📅</div>
                  <div className="text-sm">Нет занятий</div>
                </div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

