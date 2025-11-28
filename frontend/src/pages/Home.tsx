import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { useNavigate } from 'react-router-dom'

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  const { data: searchResults } = useQuery({
    queryKey: ['search', searchQuery],
    queryFn: async () => {
      if (searchQuery.length < 2) return null
      const response = await api.get('/api/search', {
        params: { q: searchQuery },
      })
      return response.data
    },
    enabled: searchQuery.length >= 2,
  })

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">САФУ Расписание</h1>

      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <h2 className="text-xl font-semibold mb-4">Быстрый поиск</h2>
        <input
          type="text"
          placeholder="Поиск по ФИО, дисциплине, аудитории..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full border rounded px-4 py-2 mb-4"
        />

        {searchResults && (
          <div className="space-y-4">
            {searchResults.lecturers && searchResults.lecturers.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Преподаватели</h3>
                <div className="space-y-1">
                  {searchResults.lecturers.map((l: any) => (
                    <div
                      key={l.id}
                      className="p-2 hover:bg-gray-100 cursor-pointer rounded"
                      onClick={() => navigate(`/timetable/lecturer/${l.id}`)}
                    >
                      {l.fio}
                    </div>
                  ))}
                </div>
              </div>
            )}
            {searchResults.groups && searchResults.groups.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Группы</h3>
                <div className="space-y-1">
                  {searchResults.groups.map((g: any) => (
                    <div
                      key={g.id}
                      className="p-2 hover:bg-gray-100 cursor-pointer rounded"
                      onClick={() => navigate(`/timetable/group/${g.id}`)}
                    >
                      {g.code}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Студент</h2>
          <p className="text-gray-600 mb-4">
            Просмотр расписания для вашей группы
          </p>
          <button
            onClick={() => navigate('/groups')}
            className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
          >
            Выбрать группу
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Преподаватель</h2>
          <p className="text-gray-600 mb-4">
            Просмотр вашего расписания
          </p>
          <button
            onClick={() => navigate('/timetable')}
            className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
          >
            Открыть расписание
          </button>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Быстрый доступ</h2>
        <div className="flex gap-4">
          <button
            onClick={() => navigate('/groups')}
            className="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded"
          >
            Все группы
          </button>
          <button
            onClick={() => navigate('/timetable')}
            className="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded"
          >
            Общее расписание
          </button>
        </div>
      </div>
    </div>
  )
}

