import { create } from 'zustand'
import { startOfWeek, endOfWeek, format, addWeeks, subWeeks } from 'date-fns'
import { logger } from '../utils/logger'

// Функция для получения начала и конца недели
const getWeekRange = (date: Date) => {
  const weekStart = startOfWeek(date, { weekStartsOn: 1 }) // Понедельник
  const weekEnd = endOfWeek(date, { weekStartsOn: 1 }) // Воскресенье
  return {
    start: format(weekStart, 'yyyy-MM-dd'),
    end: format(weekEnd, 'yyyy-MM-dd'),
    date: weekStart,
  }
}

// Текущая неделя по умолчанию
const currentWeek = getWeekRange(new Date())

interface FiltersState {
  weekDate: Date // Дата начала недели
  dateFrom: string | null
  dateTo: string | null
  groupId: number | null
  lecturerId: number | null
  roomId: number | null
  buildingId: number | null
  streamId: number | null
  workKindId: number | null
  setWeekDate: (date: Date) => void
  setCurrentWeek: () => void
  nextWeek: () => void
  prevWeek: () => void
  setDateFrom: (date: string | null) => void
  setDateTo: (date: string | null) => void
  setGroupId: (id: number | null) => void
  setLecturerId: (id: number | null) => void
  setRoomId: (id: number | null) => void
  setBuildingId: (id: number | null) => void
  setStreamId: (id: number | null) => void
  setWorkKindId: (id: number | null) => void
  reset: () => void
}

export const useFiltersStore = create<FiltersState>((set, get) => ({
  weekDate: currentWeek.date,
  dateFrom: currentWeek.start,
  dateTo: currentWeek.end,
  groupId: null,
  lecturerId: null,
  roomId: null,
  buildingId: null,
  streamId: null,
  workKindId: null,
  setWeekDate: (date) => {
    const week = getWeekRange(date)
    logger.log('[FiltersStore] setWeekDate:', { date, week })
    set({ weekDate: week.date, dateFrom: week.start, dateTo: week.end })
  },
  setCurrentWeek: () => {
    const week = getWeekRange(new Date())
    logger.log('[FiltersStore] setCurrentWeek:', week)
    set({ weekDate: week.date, dateFrom: week.start, dateTo: week.end })
  },
  nextWeek: () => {
    const current = get().weekDate
    const next = addWeeks(current, 1)
    const week = getWeekRange(next)
    logger.log('[FiltersStore] nextWeek:', { current, next, week })
    set({ weekDate: week.date, dateFrom: week.start, dateTo: week.end })
  },
  prevWeek: () => {
    const current = get().weekDate
    const prev = subWeeks(current, 1)
    const week = getWeekRange(prev)
    logger.log('[FiltersStore] prevWeek:', { current, prev, week })
    set({ weekDate: week.date, dateFrom: week.start, dateTo: week.end })
  },
  setDateFrom: (date) => set({ dateFrom: date }),
  setDateTo: (date) => set({ dateTo: date }),
  setGroupId: (id) => set({ groupId: id }),
  setLecturerId: (id) => set({ lecturerId: id }),
  setRoomId: (id) => set({ roomId: id }),
  setBuildingId: (id) => set({ buildingId: id }),
  setStreamId: (id) => set({ streamId: id }),
  setWorkKindId: (id) => set({ workKindId: id }),
  reset: () => {
    const week = getWeekRange(new Date())
    set({
      weekDate: week.date,
      dateFrom: week.start,
      dateTo: week.end,
      groupId: null,
      lecturerId: null,
      roomId: null,
      buildingId: null,
      streamId: null,
      workKindId: null,
    })
  },
}))

