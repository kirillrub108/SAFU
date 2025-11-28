import { useState } from 'react'
import { api } from '../lib/api'

export default function Import() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post('/api/import/html', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (error: any) {
      setResult({ error: error.response?.data?.detail || 'Ошибка загрузки' })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Импорт HTML расписания</h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Выберите HTML файл
          </label>
          <input
            type="file"
            accept=".html,.htm"
            onChange={handleFileChange}
            className="border rounded px-3 py-2"
          />
        </div>
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {uploading ? 'Загрузка...' : 'Загрузить'}
        </button>

        {result && (
          <div className="mt-6 p-4 bg-gray-50 rounded">
            {result.error ? (
              <div className="text-red-600">{result.error}</div>
            ) : (
              <div>
                <p className="font-semibold">Импорт завершен</p>
                <p>Создано событий: {result.events_created}</p>
                <p>Ошибок: {result.errors_count}</p>
                <p>Предупреждений: {result.warnings_count}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

