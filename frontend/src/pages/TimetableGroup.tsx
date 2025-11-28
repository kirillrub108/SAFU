import { useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api, EventDetail, Group } from '../lib/api'
import ScheduleGrid from '../components/ScheduleGrid'
import WeekSelector from '../components/WeekSelector'
import DebugInfo from '../components/DebugInfo'
import { useFiltersStore } from '../store/filters'
import { logger } from '../utils/logger'

export default function TimetableGroup() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const filters = useFiltersStore()
  const initializedRef = useRef(false)

  // Проверяем наличие id
  useEffect(() => {
    if (!id) {
      logger.error('[TimetableGroup] No group ID in URL params, redirecting to groups list')
      navigate('/groups')
      return
    }
  }, [id, navigate])

  // Устанавливаем текущую неделю и группу при загрузке
  useEffect(() => {
    if (!id) return
    
    logger.log('[TimetableGroup] Initializing with group:', id, {
      currentFilters: {
        dateFrom: filters.dateFrom,
        dateTo: filters.dateTo,
        groupId: filters.groupId,
      },
    })
    
    // Инициализируем даты только один раз
    if (!initializedRef.current) {
      if (!filters.dateFrom || !filters.dateTo) {
        logger.log('[TimetableGroup] Setting current week')
        filters.setCurrentWeek()
      }
      initializedRef.current = true
    }
    
    // Устанавливаем группу
    const groupIdNum = parseInt(id, 10)
    if (!isNaN(groupIdNum) && groupIdNum !== filters.groupId) {
      logger.log('[TimetableGroup] Setting group ID:', groupIdNum)
      filters.setGroupId(groupIdNum)
    }
  }, [id]) // eslint-disable-line react-hooks/exhaustive-deps

  const groupId = id ? parseInt(id, 10) : null
  const isEnabled = !!id && !isNaN(groupId!) && !!filters.dateFrom && !!filters.dateTo

  const { data: group, isLoading: isLoadingGroup } = useQuery<Group>({
    queryKey: ['group', id],
    queryFn: async () => {
      if (!id) throw new Error('Group ID is required')
      logger.log('[TimetableGroup] Fetching group info:', id)
      const response = await api.get(`/api/groups/${id}`)
      logger.log('[TimetableGroup] Group info received:', response.data)
      return response.data
    },
    enabled: !!id && !isNaN(groupId!),
  })

  const { data: events, isLoading, isFetching, error } = useQuery<EventDetail[]>({
    queryKey: ['timetable', 'group', id, filters.dateFrom, filters.dateTo],
    queryFn: async () => {
      if (!id || !groupId) throw new Error('Group ID is required')
      
      const params = new URLSearchParams()
      if (filters.dateFrom) params.append('date_from', filters.dateFrom)
      if (filters.dateTo) params.append('date_to', filters.dateTo)
      params.append('group_id', id)
      
      const url = `/api/timetable?${params.toString()}`
      logger.log('[TimetableGroup] Fetching timetable:', {
        url,
        params: {
          date_from: filters.dateFrom,
          date_to: filters.dateTo,
          group_id: id,
        },
        enabled: isEnabled,
      })
      
      try {
        const response = await api.get('/api/timetable', { params })
        logger.log('[TimetableGroup] Response received:', {
          status: response.status,
          count: response.data?.length || 0,
          firstEvent: response.data?.[0] || null,
          allDates: response.data?.map((e: EventDetail) => e.time_slot?.date).filter(Boolean) || [],
        })
        return response.data
      } catch (error: any) {
        logger.error('[TimetableGroup] Error fetching timetable:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
        })
        throw error
      }
    },
    enabled: isEnabled,
    staleTime: 0,
    refetchOnMount: true,
    refetchOnWindowFocus: false,
  })

  // Логируем состояние запроса
  useEffect(() => {
    logger.log('[TimetableGroup] Query state:', {
      id,
      groupId,
      isEnabled,
      isLoading,
      isFetching,
      hasEvents: !!events,
      eventsCount: events?.length || 0,
      dateFrom: filters.dateFrom,
      dateTo: filters.dateTo,
      error: error ? String(error) : null,
    })
  }, [id, groupId, isEnabled, isLoading, isFetching, events, filters.dateFrom, filters.dateTo, error])

  if (!id) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">Ошибка: ID группы не указан</p>
        <button
          onClick={() => navigate('/groups')}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Вернуться к списку групп
        </button>
      </div>
    )
  }

  if ((isLoading || isLoadingGroup) && !events) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Загрузка расписания...</p>
      </div>
    )
  }

  if (error) {
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
      <h1 className="text-3xl font-bold mb-2">
        Расписание группы {group?.code || id || 'неизвестно'}
      </h1>
      {group?.name && (
        <p className="text-gray-600 mb-6">{group.name}</p>
      )}
      {!group && id && (
        <p className="text-yellow-600 mb-6">Загрузка информации о группе...</p>
      )}
      <WeekSelector />
      <DebugInfo events={events} />
      
      {isFetching && events && (
        <div className="mb-4 text-sm text-blue-600 bg-blue-50 p-2 rounded">
          Обновление данных...
        </div>
      )}
      
      {!isEnabled && (
        <div className="mb-4 text-sm text-yellow-600 bg-yellow-50 p-2 rounded">
          Ожидание данных: {!id ? 'ID группы отсутствует' : !filters.dateFrom || !filters.dateTo ? 'Даты не установлены' : 'Неизвестная ошибка'}
        </div>
      )}
      
      {events && events.length > 0 ? (
        <>
          <div className="mb-4 text-sm text-gray-600">
            Найдено событий: <span className="font-semibold">{events.length}</span> на период{' '}
            <span className="font-semibold">{filters.dateFrom}</span> -{' '}
            <span className="font-semibold">{filters.dateTo}</span>
          </div>
          <ScheduleGrid events={events} weekStart={filters.weekDate} />
        </>
      ) : !isLoading && isEnabled ? (
        <div className="text-center py-8 text-gray-500 bg-white rounded-lg shadow p-6">
          <p className="text-lg mb-2 font-semibold">Нет событий для этой группы</p>
          <p className="text-sm mb-4">
            На период <span className="font-semibold">{filters.dateFrom}</span> -{' '}
            <span className="font-semibold">{filters.dateTo}</span>
          </p>
          <div className="text-xs text-gray-400 mt-4">
            <p>Проверьте:</p>
            <ul className="list-disc list-inside mt-2 space-y-1">
              <li>Правильность выбранной недели</li>
              <li>Наличие событий в БД для группы ID: {id}</li>
              <li>Консоль браузера (F12) для отладочной информации</li>
              <li>Вкладку Network для проверки запросов к API</li>
            </ul>
          </div>
        </div>
      ) : null}
    </div>
  )
}
