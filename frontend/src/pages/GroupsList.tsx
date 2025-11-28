import { useQuery } from '@tanstack/react-query'
import { api, Group } from '../lib/api'
import { useNavigate } from 'react-router-dom'

export default function GroupsList() {
  const navigate = useNavigate()

  const { data: groups, isLoading } = useQuery<Group[]>({
    queryKey: ['groups'],
    queryFn: async () => {
      const response = await api.get('/api/groups')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Список групп</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {groups?.map((group) => (
          <div
            key={group.id}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => navigate(`/timetable/group/${group.id}`)}
          >
            <h3 className="text-xl font-semibold text-blue-600 mb-2">
              {group.code}
            </h3>
            <p className="text-gray-600">{group.name}</p>
            <button
              className="mt-4 text-blue-600 hover:text-blue-800 font-medium"
              onClick={(e) => {
                e.stopPropagation()
                navigate(`/timetable/group/${group.id}`)
              }}
            >
              Посмотреть расписание →
            </button>
          </div>
        ))}
      </div>
      {groups && groups.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          Группы не найдены
        </div>
      )}
    </div>
  )
}

