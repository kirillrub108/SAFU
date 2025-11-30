import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api, Building, Group, Lecturer, WorkKind } from '../lib/api'
import { useFiltersStore } from '../store/filters'

interface FiltersBarProps {
  isOpen: boolean
}

export default function FiltersBar({ isOpen }: FiltersBarProps) {
  const filters = useFiltersStore()

  const { data: buildings } = useQuery<Building[]>({
    queryKey: ['buildings'],
    queryFn: async () => {
      const response = await api.get('/api/buildings')
      return response.data
    },
  })

  const { data: groups } = useQuery<Group[]>({
    queryKey: ['groups'],
    queryFn: async () => {
      const response = await api.get('/api/groups')
      return response.data
    },
  })

  const [selectedChair, setSelectedChair] = useState<string>('')

  const { data: lecturers } = useQuery<Lecturer[]>({
    queryKey: ['lecturers'],
    queryFn: async () => {
      const response = await api.get('/api/lecturers')
      return response.data
    },
  })

  // Получаем уникальные кафедры
  const chairs = Array.from(
    new Set(lecturers?.filter((l) => l.chair).map((l) => l.chair) || [])
  ).filter(Boolean) as string[]

  // Фильтруем преподавателей по выбранной кафедре
  const filteredLecturers = selectedChair
    ? lecturers?.filter((l) => l.chair === selectedChair)
    : lecturers

  const { data: workKinds } = useQuery<WorkKind[]>({
    queryKey: ['work-kinds'],
    queryFn: async () => {
      const response = await api.get('/api/work-kinds')
      return response.data
    },
  })

  if (!isOpen) {
    return null
  }

  return (
    <div className="bg-white p-3 md:p-4 rounded-lg shadow mb-4 md:mb-6">
      <h3 className="text-lg md:text-xl font-semibold mb-3 md:mb-4">Фильтры</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        <div>
          <label className="block text-sm md:text-base font-medium text-gray-700 mb-1">
            Группа
          </label>
          <select
            value={filters.groupId || ''}
            onChange={(e) =>
              filters.setGroupId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-base"
          >
            <option value="">Все</option>
            {groups?.map((group) => (
              <option key={group.id} value={group.id}>
                {group.code}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm md:text-base font-medium text-gray-700 mb-1">
            Кафедра
          </label>
          <select
            value={selectedChair}
            onChange={(e) => {
              setSelectedChair(e.target.value)
              filters.setLecturerId(null) // Сбрасываем выбор преподавателя при смене кафедры
            }}
            className="w-full border rounded px-2 md:px-3 py-2 text-base"
          >
            <option value="">Все кафедры</option>
            {chairs.map((chair) => (
              <option key={chair} value={chair}>
                {chair}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm md:text-base font-medium text-gray-700 mb-1">
            Преподаватель
          </label>
          <select
            value={filters.lecturerId || ''}
            onChange={(e) =>
              filters.setLecturerId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-base"
            disabled={!selectedChair && chairs.length > 0}
          >
            <option value="">Все</option>
            {filteredLecturers?.map((lecturer) => (
              <option key={lecturer.id} value={lecturer.id}>
                {lecturer.fio}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm md:text-base font-medium text-gray-700 mb-1">
            Вид занятия
          </label>
          <select
            value={filters.workKindId || ''}
            onChange={(e) =>
              filters.setWorkKindId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-base"
          >
            <option value="">Все</option>
            {workKinds?.map((wk) => (
              <option key={wk.id} value={wk.id}>
                {wk.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm md:text-base font-medium text-gray-700 mb-1">
            Корпус
          </label>
          <select
            value={filters.buildingId || ''}
            onChange={(e) =>
              filters.setBuildingId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-base"
          >
            <option value="">Все</option>
            {buildings?.map((building) => (
              <option key={building.id} value={building.id}>
                {building.name}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-end gap-2 md:col-span-1 lg:col-span-4">
          <button
            onClick={() => filters.reset()}
            className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded text-base"
          >
            Сбросить фильтры
          </button>
          <button
            onClick={async () => {
              const token = localStorage.getItem('token')
              if (!token) {
                alert('Необходимо войти в систему для сохранения в избранное')
                return
              }
              const favoriteName = prompt('Введите название для избранного:')
              if (!favoriteName) return
              try {
                await api.post(
                  '/api/favorites',
                  {
                    name: favoriteName,
                    filters: {
                      group_id: filters.groupId,
                      lecturer_id: filters.lecturerId,
                      work_kind_id: filters.workKindId,
                      building_id: filters.buildingId,
                    },
                  },
                  {
                    headers: { Authorization: `Bearer ${token}` },
                  }
                )
                alert('Добавлено в избранное!')
              } catch (err: any) {
                alert(err.response?.data?.detail || 'Ошибка при сохранении')
              }
            }}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-base font-semibold"
          >
            ❤️ Добавить в избранное
          </button>
        </div>
      </div>
      <div className="mt-3 md:mt-4 text-sm md:text-base text-gray-600">
        Период: {filters.dateFrom} - {filters.dateTo}
      </div>
    </div>
  )
}

