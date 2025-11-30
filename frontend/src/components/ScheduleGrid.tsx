import { EventDetail } from '../lib/api'
import EventCard from './EventCard'
import ScheduleGridMobile from './ScheduleGridMobile'
import { format, parseISO, startOfWeek, addDays, isSameDay, isToday } from 'date-fns'
import { logger } from '../utils/logger'
import { useState, useEffect } from 'react'

interface ScheduleGridProps {
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

export default function ScheduleGrid({ events, weekStart }: ScheduleGridProps) {
  const [isMobile, setIsMobile] = useState(false)

  // Определяем, мобильное ли устройство
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768) // md breakpoint в Tailwind
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // На мобильных показываем мобильную версию
  if (isMobile) {
    return <ScheduleGridMobile events={events} weekStart={weekStart} />
  }

  const weekStartDate = startOfWeek(weekStart, { weekStartsOn: 1 })
  const days = Array.from({ length: 7 }, (_, i) => addDays(weekStartDate, i))
  const pairs = [1, 2, 3, 4, 5, 6, 7, 8]

  const getEventsForDayAndPair = (day: Date, pairNumber: number) => {
    if (!events || events.length === 0) return []
    
    // Нормализуем день для сравнения (только дата, без времени)
    const dayYear = day.getFullYear()
    const dayMonth = day.getMonth()
    const dayDate = day.getDate()
    
    const filtered = events.filter((event) => {
      if (!event.time_slot || !event.time_slot.date) {
        logger.warn('[ScheduleGrid] Event missing time_slot or date:', event)
        return false
      }
      
      try {
        // Парсим дату события (формат: YYYY-MM-DD)
        const eventDateStr = event.time_slot.date
        
        // Парсим дату из строки YYYY-MM-DD
        const [year, month, date] = eventDateStr.split('-').map(Number)
        
        if (isNaN(year) || isNaN(month) || isNaN(date)) {
          logger.warn('[ScheduleGrid] Invalid date format:', eventDateStr)
          return false
        }
        
        // Сравниваем даты напрямую
        const sameDay = year === dayYear && month - 1 === dayMonth && date === dayDate
        const samePair = event.time_slot.pair_number === pairNumber
        
        return sameDay && samePair
      } catch (e) {
        logger.error('[ScheduleGrid] Error parsing event date:', event.time_slot.date, e, event)
        return false
      }
    })
    
    if (filtered.length > 0) {
      logger.log(`[ScheduleGrid] Found ${filtered.length} events for ${day.toISOString().split('T')[0]}, pair ${pairNumber}`)
    }
    
    return filtered
  }

  const getDayName = (day: Date) => {
    const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    return dayNames[day.getDay() === 0 ? 6 : day.getDay() - 1]
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden w-full">
      <div className="w-full overflow-hidden">
        <table className="w-full border-collapse" style={{ tableLayout: 'fixed', width: '100%' }}>
          <colgroup>
            <col style={{ width: '60px' }} />
            {days.map((day, index) => (
              <col key={`day-col-${index}`} />
            ))}
          </colgroup>
          <thead>
            <tr>
              <th className="border p-2 bg-gray-100 font-semibold text-center w-16">
                <div className="text-sm">Пара</div>
              </th>
              {days.map((day) => {
                const isCurrentDay = isToday(day)
                return (
                  <th
                    key={day.toISOString()}
                    className={`border p-2 bg-gray-100 ${
                      isCurrentDay ? 'bg-blue-50 border-blue-300' : ''
                    }`}
                  >
                    <div className="text-center">
                      <div className="text-sm font-semibold text-gray-800">
                        {getDayName(day)}
                      </div>
                      <div
                        className={`text-xs ${
                          isCurrentDay ? 'text-blue-600 font-bold' : 'text-gray-600'
                        }`}
                      >
                        {format(day, 'd.MM')}
                      </div>
                      {isCurrentDay && (
                        <div className="text-xs text-blue-600 font-medium mt-0.5">
                          Сегодня
                        </div>
                      )}
                    </div>
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            {pairs.map((pair) => {
              const pairTime = PAIR_TIMES[pair]
              return (
                <tr key={pair} className="hover:bg-gray-50">
                  <td className="border p-1.5 text-center font-semibold bg-gray-50 align-top w-16">
                    <div className="text-base font-bold">{pair}</div>
                    {pairTime && (
                      <div className="text-xs text-gray-500 mt-0.5 leading-tight">
                        {pairTime.start}
                        <br />
                        {pairTime.end}
                      </div>
                    )}
                  </td>
                  {days.map((day) => {
                    const dayEvents = getEventsForDayAndPair(day, pair)
                    const isCurrentDay = isToday(day)
                    return (
                      <td
                        key={day.toISOString()}
                        className={`border p-1.5 align-top ${
                          isCurrentDay ? 'bg-blue-50' : ''
                        }`}
                        style={{ minHeight: '80px' }}
                      >
                        <div className="space-y-1.5 h-full">
                          {dayEvents.length > 0 ? (
                            dayEvents.map((event) => (
                              <EventCard key={event.id} event={event} />
                            ))
                          ) : (
                            <div className="text-xs text-gray-400 text-center py-1">
                              —
                            </div>
                          )}
                        </div>
                      </td>
                    )
                  })}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

