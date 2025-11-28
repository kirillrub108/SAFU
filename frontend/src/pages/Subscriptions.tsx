import { useState } from 'react'
import { api } from '../lib/api'

export default function Subscriptions() {
  const [filterKind, setFilterKind] = useState<'group' | 'lecturer' | 'stream'>('group')
  const [filterId, setFilterId] = useState('')
  const [subscription, setSubscription] = useState<any>(null)

  const handleSubscribe = async () => {
    if (!filterId) return

    try {
      const response = await api.get('/api/calendar/subscribe', {
        params: {
          filter_kind: filterKind,
          filter_id: parseInt(filterId),
        },
      })
      setSubscription(response.data)
    } catch (error) {
      console.error('Ошибка создания подписки', error)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Подписки на календарь</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Тип фильтра
          </label>
          <select
            value={filterKind}
            onChange={(e) => setFilterKind(e.target.value as any)}
            className="border rounded px-3 py-2"
          >
            <option value="group">Группа</option>
            <option value="lecturer">Преподаватель</option>
            <option value="stream">Поток</option>
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            ID
          </label>
          <input
            type="number"
            value={filterId}
            onChange={(e) => setFilterId(e.target.value)}
            className="border rounded px-3 py-2"
            placeholder="Введите ID"
          />
        </div>
        <button
          onClick={handleSubscribe}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Создать подписку
        </button>

        {subscription && (
          <div className="mt-6 p-4 bg-gray-50 rounded">
            <p className="font-semibold mb-2">Подписка создана</p>
            <p className="text-sm text-gray-600 mb-2">
              URL для подписки в календаре:
            </p>
            <code className="block p-2 bg-white border rounded break-all">
              {subscription.ics_url}
            </code>
          </div>
        )}
      </div>
    </div>
  )
}

