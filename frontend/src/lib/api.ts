import axios from 'axios'
import { logger } from '../utils/logger'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 секунд таймаут
})

// Добавляем перехватчик для логирования запросов
api.interceptors.request.use(
  (config) => {
    logger.log('[API] Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      params: config.params,
    })
    return config
  },
  (error) => {
    logger.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Добавляем перехватчик для логирования ответов
api.interceptors.response.use(
  (response) => {
    logger.log('[API] Response:', {
      status: response.status,
      url: response.config.url,
      dataLength: Array.isArray(response.data) ? response.data.length : 'N/A',
    })
    return response
  },
  (error) => {
    logger.error('[API] Response error:', {
      message: error.message,
      status: error.response?.status,
      url: error.config?.url,
      data: error.response?.data,
    })
    return Promise.reject(error)
  }
)

export interface EventDetail {
  id: number
  discipline_id: number
  work_kind_id: number
  room_id: number
  time_slot_id: number
  status: string
  note?: string
  discipline?: { id: number; name: string }
  work_kind?: { id: number; name: string; color_hex: string }
  room?: {
    id: number
    number: string
    building?: { id: number; name: string; address: string }
  }
  time_slot?: {
    id: number
    date: string
    pair_number: number
    time_start: string
    time_end: string
  }
  lecturers?: Array<{ id: number; fio: string }>
  groups?: Array<{ id: number; code: string }>
  subgroups?: Array<{ id: number; code: string }>
  streams?: Array<{ id: number; name: string }>
  has_conflict?: boolean
  conflicting_event_ids?: number[]
}

export interface Building {
  id: number
  name: string
  code?: string
  address: string
}

export interface Room {
  id: number
  building_id: number
  number: string
  capacity: number
  type: string
}

export interface Lecturer {
  id: number
  fio: string
  chair?: string
}

export interface Group {
  id: number
  code: string
  name: string
}

export interface WorkKind {
  id: number
  name: string
  color_hex: string
}

