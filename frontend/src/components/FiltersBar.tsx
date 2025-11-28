import { useQuery } from '@tanstack/react-query'
import { api, Building, Group, Lecturer, WorkKind } from '../lib/api'
import { useFiltersStore } from '../store/filters'

export default function FiltersBar() {
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

  const { data: lecturers } = useQuery<Lecturer[]>({
    queryKey: ['lecturers'],
    queryFn: async () => {
      const response = await api.get('/api/lecturers')
      return response.data
    },
  })

  const { data: workKinds } = useQuery<WorkKind[]>({
    queryKey: ['work-kinds'],
    queryFn: async () => {
      const response = await api.get('/api/work-kinds')
      return response.data
    },
  })

  return (
    <div className="bg-white p-3 md:p-4 rounded-lg shadow mb-4 md:mb-6">
      <h3 className="text-base md:text-lg font-semibold mb-3 md:mb-4">Фильтры</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        <div>
          <label className="block text-xs md:text-sm font-medium text-gray-700 mb-1">
            Группа
          </label>
          <select
            value={filters.groupId || ''}
            onChange={(e) =>
              filters.setGroupId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-sm md:text-base"
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
          <label className="block text-xs md:text-sm font-medium text-gray-700 mb-1">
            Преподаватель
          </label>
          <select
            value={filters.lecturerId || ''}
            onChange={(e) =>
              filters.setLecturerId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-sm md:text-base"
          >
            <option value="">Все</option>
            {lecturers?.map((lecturer) => (
              <option key={lecturer.id} value={lecturer.id}>
                {lecturer.fio}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-xs md:text-sm font-medium text-gray-700 mb-1">
            Вид занятия
          </label>
          <select
            value={filters.workKindId || ''}
            onChange={(e) =>
              filters.setWorkKindId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-sm md:text-base"
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
          <label className="block text-xs md:text-sm font-medium text-gray-700 mb-1">
            Корпус
          </label>
          <select
            value={filters.buildingId || ''}
            onChange={(e) =>
              filters.setBuildingId(e.target.value ? parseInt(e.target.value) : null)
            }
            className="w-full border rounded px-2 md:px-3 py-2 text-sm md:text-base"
          >
            <option value="">Все</option>
            {buildings?.map((building) => (
              <option key={building.id} value={building.id}>
                {building.name}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-end md:col-span-1 lg:col-span-4">
          <button
            onClick={() => filters.reset()}
            className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded text-sm md:text-base"
          >
            Сбросить фильтры
          </button>
        </div>
      </div>
      <div className="mt-3 md:mt-4 text-xs md:text-sm text-gray-600">
        Период: {filters.dateFrom} - {filters.dateTo}
      </div>
    </div>
  )
}

