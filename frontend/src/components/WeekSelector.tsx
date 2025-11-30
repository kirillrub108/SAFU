import { format, startOfWeek, isSameWeek } from 'date-fns'
import { useFiltersStore } from '../store/filters'
import { logger } from '../utils/logger'
import PeriodSelector from './PeriodSelector'

interface WeekSelectorProps {
  onFiltersToggle?: () => void
  filtersOpen?: boolean
}

export default function WeekSelector({ onFiltersToggle, filtersOpen }: WeekSelectorProps) {
  const filters = useFiltersStore()
  const weekStart = filters.weekDate
  const weekEnd = new Date(weekStart)
  weekEnd.setDate(weekEnd.getDate() + 6)

  const isCurrentWeek = () => {
    const today = new Date()
    const currentWeekStart = startOfWeek(today, { weekStartsOn: 1 })
    return isSameWeek(weekStart, currentWeekStart, { weekStartsOn: 1 })
  }

  const handlePrevWeek = () => {
    logger.log('[WeekSelector] Previous week clicked')
    filters.prevWeek()
  }

  const handleNextWeek = () => {
    logger.log('[WeekSelector] Next week clicked')
    filters.nextWeek()
  }

  const handleCurrentWeek = () => {
    logger.log('[WeekSelector] Current week clicked')
    filters.setCurrentWeek()
  }

  return (
    <div className="bg-white p-3 md:p-4 rounded-lg shadow mb-4">
      {/* Мобильная версия */}
      <div className="md:hidden space-y-3">
        {/* Период недели */}
        <div className="text-center">
          <div className="font-semibold text-lg">
            {format(weekStart, 'd MMM')} - {format(weekEnd, 'd MMM yyyy')}
          </div>
          {isCurrentWeek() && (
            <div className="text-sm text-blue-600 font-medium mt-1">Текущая неделя</div>
          )}
        </div>
        
        {/* Кнопки навигации */}
        <div className="flex items-center justify-between gap-2">
          <button
            onClick={handlePrevWeek}
            className="flex-1 px-3 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors font-medium text-base"
          >
            ← Пред.
          </button>
          <button
            onClick={handleCurrentWeek}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-base"
          >
            Сегодня
          </button>
          <button
            onClick={handleNextWeek}
            className="flex-1 px-3 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors font-medium text-base"
          >
            След. →
          </button>
        </div>
      </div>
      
      {/* Десктопная версия */}
      <div className="hidden md:flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={handlePrevWeek}
            className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded transition-colors"
          >
            ← Предыдущая
          </button>
          <div className="text-center">
            <div className="font-semibold text-xl">
              {format(weekStart, 'd MMM')} - {format(weekEnd, 'd MMM yyyy')}
            </div>
            {isCurrentWeek() && (
              <div className="text-sm text-blue-600 font-medium">Текущая неделя</div>
            )}
          </div>
          <button
            onClick={handleNextWeek}
            className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded transition-colors"
          >
            Следующая →
          </button>
        </div>
        <div className="flex items-center gap-2">
          <PeriodSelector />
          <button
            onClick={handleCurrentWeek}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            Сегодня
          </button>
          <button
            onClick={onFiltersToggle}
            className={`px-4 py-2 rounded transition-colors ${
              filtersOpen
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            🔍 Фильтры
          </button>
        </div>
      </div>
      
      {/* Мобильная версия с кнопками */}
      <div className="md:hidden mt-3 flex items-center gap-2">
        <PeriodSelector />
        <button
          onClick={onFiltersToggle}
          className={`flex-1 px-4 py-2 rounded transition-colors ${
            filtersOpen
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          🔍 Фильтры
        </button>
      </div>
    </div>
  )
}

