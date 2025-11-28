import { useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api, EventDetail, Lecturer } from '../lib/api'
import ScheduleGrid from '../components/ScheduleGrid'
import WeekSelector from '../components/WeekSelector'
import { useFiltersStore } from '../store/filters'
import { logger } from '../utils/logger'

export default function TimetableLecturer() {
  const { id } = useParams<{ id: string }>()
  const filters = useFiltersStore()

  // Устанавливаем текущую неделю и преподавателя при загрузке
  useEffect(() => {
    logger.log('[TimetableLecturer] Initializing with lecturer:', id)
    if (!filters.dateFrom || !filters.dateTo) {
      filters.setCurrentWeek()
    }
    if (id) {
      const lecturerIdNum = parseInt(id)
      if (lecturerIdNum !== filters.lecturerId) {
        filters.setLecturerId(lecturerIdNum)
      }
    }
  }, [id, filters])

  const { data: lecturer } = useQuery<Lecturer>({
    queryKey: ['lecturer', id],
    queryFn: async () => {
      const response = await api.get(`/api/lecturers/${id}`)
      return response.data
    },
    enabled: !!id,
  })

  const { data: events, isLoading, isFetching } = useQuery<EventDetail[]>({
    queryKey: ['timetable', 'lecturer', id, filters.dateFrom, filters.dateTo],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (filters.dateFrom) params.append('date_from', filters.dateFrom)
      if (filters.dateTo) params.append('date_to', filters.dateTo)
      if (id) params.append('lecturer_id', id)
      
      const url = `/api/timetable?${params.toString()}`
      logger.log('[TimetableLecturer] Fetching timetable:', url)
      
      try {
        const response = await api.get('/api/timetable', { params })
        logger.log('[TimetableLecturer] Response received:', {
          count: response.data?.length || 0,
        })
        return response.data
      } catch (error) {
        logger.error('[TimetableLecturer] Error:', error)
        throw error
      }
    },
    enabled: !!id && !!filters.dateFrom && !!filters.dateTo,
    staleTime: 0,
    refetchOnMount: true,
  })

  if (isLoading && !events) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Загрузка расписания...</p>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-2">
        Расписание преподавателя
      </h1>
      {lecturer && (
        <p className="text-gray-600 mb-6">{lecturer.fio}</p>
      )}
      <WeekSelector />
      
      {isFetching && events && (
        <div className="mb-4 text-sm text-blue-600 bg-blue-50 p-2 rounded">
          Обновление данных...
        </div>
      )}
      
      {events && events.length > 0 ? (
        <>
          <div className="mb-4 text-sm text-gray-600">
            Найдено событий: <span className="font-semibold">{events.length}</span>
          </div>
          <ScheduleGrid events={events} weekStart={filters.weekDate} />
        </>
      ) : !isLoading ? (
        <div className="text-center py-8 text-gray-500 bg-white rounded-lg shadow p-6">
          <p className="text-lg mb-2 font-semibold">Нет событий для этого преподавателя</p>
          <p className="text-sm">
            На период <span className="font-semibold">{filters.dateFrom}</span> -{' '}
            <span className="font-semibold">{filters.dateTo}</span>
          </p>
        </div>
      ) : null}
    </div>
  )
}

