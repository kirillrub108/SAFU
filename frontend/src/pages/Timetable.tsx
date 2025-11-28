import { useEffect, useRef } from 'react'
import { useTimetable } from '../hooks/useTimetable'
import ScheduleGrid from '../components/ScheduleGrid'
import FiltersBar from '../components/FiltersBar'
import WeekSelector from '../components/WeekSelector'
import DebugInfo from '../components/DebugInfo'
import { useFiltersStore } from '../store/filters'
import { logger } from '../utils/logger'

export default function Timetable() {
  const filters = useFiltersStore()
  const initializedRef = useRef(false)
  
  // Устанавливаем текущую неделю при первой загрузке
  useEffect(() => {
    if (!initializedRef.current) {
      logger.log('[Timetable] Initializing with current week')
      filters.setCurrentWeek()
      initializedRef.current = true
    }
  }, [filters])

  const { data: events, isLoading, error, isFetching } = useTimetable()

  // Отладочная информация
  useEffect(() => {
    logger.log('[Timetable] State update:', {
      isLoading,
      isFetching,
      hasEvents: !!events,
      eventsCount: events?.length || 0,
      dateFrom: filters.dateFrom,
      dateTo: filters.dateTo,
      weekDate: filters.weekDate,
      error: error ? String(error) : null,
    })
    
    if (events && events.length > 0) {
      logger.log('[Timetable] Events details:', {
        count: events.length,
        firstEvent: events[0] ? {
          id: events[0].id,
          date: events[0].time_slot?.date,
          pair: events[0].time_slot?.pair_number,
          discipline: events[0].discipline?.name,
        } : null,
        allDates: [...new Set(events.map(e => e.time_slot?.date).filter(Boolean))],
      })
    }
  }, [events, isLoading, isFetching, error, filters.dateFrom, filters.dateTo, filters.weekDate])


  // Показываем загрузку только при первой загрузке, не при обновлении
  if (isLoading && !events) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Загрузка расписания...</p>
      </div>
    )
  }

  if (error) {
    logger.error('[Timetable] Error:', error)
    return (
      <div className="text-center py-8 text-red-600 bg-red-50 rounded-lg p-6">
        <p className="font-semibold text-lg mb-2">Ошибка загрузки расписания</p>
        <p className="text-sm mt-2">{String(error)}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Перезагрузить страницу
        </button>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl md:text-3xl font-bold mb-4 md:mb-6">Расписание</h1>
      <WeekSelector />
      <FiltersBar />
      <DebugInfo events={events} />
      
      {isFetching && events && (
        <div className="mb-4 text-sm text-blue-600 bg-blue-50 p-2 rounded">
          Обновление данных...
        </div>
      )}
      
      {events && events.length > 0 ? (
        <>
          <div className="mb-4 text-xs md:text-sm text-gray-600 px-1">
            Найдено событий: <span className="font-semibold">{events.length}</span> на период{' '}
            <span className="font-semibold">{filters.dateFrom}</span> -{' '}
            <span className="font-semibold">{filters.dateTo}</span>
          </div>
          <ScheduleGrid events={events} weekStart={filters.weekDate} />
        </>
      ) : !isLoading ? (
        <div className="text-center py-6 md:py-8 text-gray-500 bg-white rounded-lg shadow p-4 md:p-6">
          <p className="text-base md:text-lg mb-2 font-semibold">Нет событий для отображения</p>
          <p className="text-xs md:text-sm mb-4">
            На период <span className="font-semibold">{filters.dateFrom}</span> -{' '}
            <span className="font-semibold">{filters.dateTo}</span>
          </p>
          <div className="text-xs text-gray-400 mt-4">
            <p>Проверьте:</p>
            <ul className="list-disc list-inside mt-2 space-y-1">
              <li>Правильность выбранной недели</li>
              <li>Наличие событий в базе данных на эти даты</li>
              <li>Консоль браузера (F12) для отладочной информации</li>
              <li>Сеть (Network tab) для проверки запросов к API</li>
            </ul>
          </div>
        </div>
      ) : null}
    </div>
  )
}

