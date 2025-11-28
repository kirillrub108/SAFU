import { useQuery } from '@tanstack/react-query'
import { api, EventDetail } from '../lib/api'
import { useFiltersStore } from '../store/filters'
import { logger } from '../utils/logger'

export const useTimetable = () => {
  const filters = useFiltersStore()

  const isEnabled = !!(filters.dateFrom && filters.dateTo)

  return useQuery<EventDetail[]>({
    queryKey: [
      'timetable',
      filters.dateFrom,
      filters.dateTo,
      filters.groupId,
      filters.lecturerId,
      filters.roomId,
      filters.buildingId,
      filters.streamId,
    ],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (filters.dateFrom) params.append('date_from', filters.dateFrom)
      if (filters.dateTo) params.append('date_to', filters.dateTo)
      if (filters.groupId) params.append('group_id', filters.groupId.toString())
      if (filters.lecturerId) params.append('lecturer_id', filters.lecturerId.toString())
      if (filters.roomId) params.append('room_id', filters.roomId.toString())
      if (filters.buildingId) params.append('building_id', filters.buildingId.toString())
      if (filters.streamId) params.append('stream_id', filters.streamId.toString())

      const url = `/api/timetable?${params.toString()}`
      logger.log('[useTimetable] Fetching timetable:', url)
      
      try {
        const response = await api.get<EventDetail[]>('/api/timetable', { params })
        logger.log('[useTimetable] Response received:', {
          count: response.data?.length || 0,
          firstEvent: response.data?.[0] || null,
        })
        return response.data
      } catch (error) {
        logger.error('[useTimetable] Error fetching timetable:', error)
        throw error
      }
    },
    enabled: isEnabled,
    staleTime: 0, // Всегда считаем данные устаревшими, чтобы запрашивать при изменении фильтров
    refetchOnMount: true, // Всегда запрашиваем при монтировании
    refetchOnWindowFocus: false, // Не запрашиваем при фокусе окна
  })
}

