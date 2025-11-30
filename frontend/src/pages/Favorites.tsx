import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

interface Favorite {
  id: number
  name: string
  filters: Record<string, any>
  created_at: string
}

export default function Favorites() {
  const { data: favorites, isLoading } = useQuery<Favorite[]>({
    queryKey: ['favorites'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      if (!token) return []
      const response = await api.get('/api/favorites', {
        headers: { Authorization: `Bearer ${token}` },
      })
      return response.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Избранное</h1>
      {favorites && favorites.length > 0 ? (
        <div className="space-y-4">
          {favorites.map((favorite) => (
            <div key={favorite.id} className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold mb-2">{favorite.name}</h3>
              <pre className="text-xs text-gray-600">
                {JSON.stringify(favorite.filters, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          Нет сохраненных избранных расписаний
        </div>
      )}
    </div>
  )
}

