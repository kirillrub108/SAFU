import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { format } from 'date-fns'

interface ChangeLog {
  id: number
  entity: string
  entity_id: number
  actor?: string
  change_at: string
  reason?: string
  diff_before?: any
  diff_after?: any
  source?: string
}

export default function AdminHistory() {
  const { data: changelog, isLoading } = useQuery<ChangeLog[]>({
    queryKey: ['changelog'],
    queryFn: async () => {
      const response = await api.get('/api/changelog')
      return response.data
    },
  })

  if (isLoading) {
    return <div className="text-center py-8">Загрузка...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">История изменений</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">Дата</th>
              <th className="px-4 py-2 text-left">Сущность</th>
              <th className="px-4 py-2 text-left">ID</th>
              <th className="px-4 py-2 text-left">Автор</th>
              <th className="px-4 py-2 text-left">Причина</th>
              <th className="px-4 py-2 text-left">Источник</th>
            </tr>
          </thead>
          <tbody>
            {changelog?.map((log) => (
              <tr key={log.id} className="border-t">
                <td className="px-4 py-2">
                  {format(new Date(log.change_at), 'dd.MM.yyyy HH:mm')}
                </td>
                <td className="px-4 py-2">{log.entity}</td>
                <td className="px-4 py-2">{log.entity_id}</td>
                <td className="px-4 py-2">{log.actor || '-'}</td>
                <td className="px-4 py-2">{log.reason || '-'}</td>
                <td className="px-4 py-2">{log.source || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

