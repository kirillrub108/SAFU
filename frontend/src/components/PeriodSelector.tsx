import { useState, useEffect } from 'react'
import { format, startOfWeek, endOfWeek, eachDayOfInterval, isSameDay, parseISO, addDays } from 'date-fns'
import { ru } from 'date-fns/locale'
import { useFiltersStore } from '../store/filters'

export default function PeriodSelector() {
  const filters = useFiltersStore()
  const [isOpen, setIsOpen] = useState(false)
  const [selectedStart, setSelectedStart] = useState<Date | null>(
    filters.dateFrom ? parseISO(filters.dateFrom) : null
  )
  const [selectedEnd, setSelectedEnd] = useState<Date | null>(
    filters.dateTo ? parseISO(filters.dateTo) : null
  )
  const [currentMonth, setCurrentMonth] = useState(
    filters.dateFrom ? parseISO(filters.dateFrom) : new Date()
  )

  // Синхронизируем выбранные даты с фильтрами
  useEffect(() => {
    if (filters.dateFrom) {
      const start = parseISO(filters.dateFrom)
      setSelectedStart(start)
      setCurrentMonth(start)
    }
    if (filters.dateTo) {
      setSelectedEnd(parseISO(filters.dateTo))
    }
  }, [filters.dateFrom, filters.dateTo])

  const handleDateClick = (date: Date) => {
    // При клике на любую дату выбираем всю неделю (понедельник - воскресенье)
    const weekStart = startOfWeek(date, { weekStartsOn: 1 })
    const weekEnd = endOfWeek(date, { weekStartsOn: 1 })
    setSelectedStart(weekStart)
    setSelectedEnd(weekEnd)
  }

  const handleApply = () => {
    if (selectedStart && selectedEnd) {
      // Убеждаемся, что выбранная неделя начинается с понедельника
      const weekStart = startOfWeek(selectedStart, { weekStartsOn: 1 })
      const weekEnd = endOfWeek(selectedStart, { weekStartsOn: 1 })
      filters.setDateFrom(format(weekStart, 'yyyy-MM-dd'))
      filters.setDateTo(format(weekEnd, 'yyyy-MM-dd'))
      setIsOpen(false)
    }
  }

  const handleReset = () => {
    filters.setCurrentWeek()
    setSelectedStart(null)
    setSelectedEnd(null)
    setIsOpen(false)
  }

  const getDaysInMonth = () => {
    const year = currentMonth.getFullYear()
    const month = currentMonth.getMonth()
    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)
    const start = startOfWeek(firstDay, { weekStartsOn: 1 })
    const end = endOfWeek(lastDay, { weekStartsOn: 1 })
    try {
      return eachDayOfInterval({ start, end })
    } catch (e) {
      // Fallback если что-то пошло не так
      const days: Date[] = []
      let current = new Date(start)
      while (current <= end) {
        days.push(new Date(current))
        current = addDays(current, 1)
      }
      return days
    }
  }

  const isDateInRange = (date: Date) => {
    if (!selectedStart || !selectedEnd) return false
    return date >= selectedStart && date <= selectedEnd
  }

  const isDateSelected = (date: Date) => {
    if (!selectedStart || !selectedEnd) return false
    // Подсвечиваем начало и конец недели
    return isSameDay(date, selectedStart) || isSameDay(date, selectedEnd)
  }

  const isDateDisabled = (date: Date) => {
    // Отключаем даты вне текущего месяца для лучшего UX
    return date.getMonth() !== currentMonth.getMonth()
  }

  const monthName = format(currentMonth, 'LLLL yyyy', { locale: ru })
  const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2 text-sm font-medium"
      >
        <span>📅</span>
        <span>
          {filters.dateFrom && filters.dateTo
            ? `${format(parseISO(filters.dateFrom), 'd MMM')} - ${format(parseISO(filters.dateTo), 'd MMM yyyy')}`
            : 'Выбрать период'}
        </span>
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute top-full left-0 mt-2 bg-white rounded-lg shadow-xl border border-gray-200 z-50 p-3 md:p-4 w-[calc(100vw-2rem)] md:w-80 max-h-[90vh] overflow-y-auto">
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <button
                  onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
                  className="p-1 hover:bg-gray-100 rounded"
                >
                  ←
                </button>
                <h3 className="font-semibold text-xl">{monthName}</h3>
                <button
                  onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
                  className="p-1 hover:bg-gray-100 rounded"
                >
                  →
                </button>
              </div>
              <p className="text-base text-gray-700 text-center mb-2 font-medium">
                Выберите неделю
              </p>
            </div>

            <div className="grid grid-cols-7 gap-1 mb-4">
              {weekDays.map((day) => (
                <div key={day} className="text-center text-sm font-semibold text-gray-600 py-1">
                  {day}
                </div>
              ))}
              {getDaysInMonth().map((date) => {
                const isCurrentMonth = date.getMonth() === currentMonth.getMonth()
                const inRange = isDateInRange(date)
                const selected = isDateSelected(date)
                const disabled = isDateDisabled(date)
                const isToday = isSameDay(date, new Date())

                return (
                  <button
                    key={date.toISOString()}
                    onClick={() => !disabled && handleDateClick(date)}
                    disabled={disabled}
                    className={`
                      p-2.5 text-base rounded transition-colors
                      ${!isCurrentMonth ? 'text-gray-300' : ''}
                      ${disabled ? 'opacity-30 cursor-not-allowed' : 'hover:bg-blue-50 cursor-pointer'}
                      ${selected ? 'bg-blue-600 text-white font-bold' : ''}
                      ${inRange && !selected ? 'bg-blue-100' : ''}
                      ${isToday && !selected ? 'border-2 border-blue-400' : ''}
                    `}
                  >
                    {format(date, 'd')}
                  </button>
                )
              })}
            </div>

            {selectedStart && selectedEnd && (
              <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <div className="text-base font-semibold text-blue-800 mb-1">
                  Выбранная неделя:
                </div>
                <div className="text-base text-blue-700">
                  {format(selectedStart, 'd MMMM', { locale: ru })} - {format(selectedEnd, 'd MMMM yyyy', { locale: ru })}
                </div>
              </div>
            )}

            <div className="flex gap-2">
              <button
                onClick={handleApply}
                disabled={!selectedStart || !selectedEnd}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-base font-medium"
              >
                Применить
              </button>
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 text-base"
              >
                Сброс
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 text-base"
              >
                Отмена
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

