import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

interface Notification {
  id: number
  type: string
  title: string
  message: string
  read: boolean
  created_at: string
}

export default function Notifications() {
  const { data: notifications, isLoading } = useQuery<Notification[]>({
    queryKey: ['notifications'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      if (!token) return []
      const response = await api.get('/api/notifications', {
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
      <h1 className="text-3xl font-bold mb-6">Уведомления</h1>
      {notifications && notifications.length > 0 ? (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`bg-white p-4 rounded-lg shadow ${
                !notification.read ? 'border-l-4 border-blue-500' : ''
              }`}
            >
              <h3 className="font-semibold mb-1">{notification.title}</h3>
              <p className="text-gray-600 text-sm">{notification.message}</p>
              <p className="text-xs text-gray-400 mt-2">
                {new Date(notification.created_at).toLocaleString('ru-RU')}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          Нет уведомлений
        </div>
      )}
    </div>
  )
}

