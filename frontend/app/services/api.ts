import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const generateItinerary = async (vacationData: any) => {
  try {
    const response = await api.post('/api/generate-itinerary', vacationData)
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Erro ao gerar itinerário')
  }
}

export const modifyItinerary = async (tripId: string, modificationRequest: string) => {
  try {
    const response = await api.post(`/api/modify-itinerary/${tripId}`, {
      modification_request: modificationRequest
    })
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Erro ao modificar itinerário')
  }
}

export const getTripHistory = async () => {
  try {
    const response = await api.get('/api/trip-history')
    return response.data
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Erro ao buscar histórico')
  }
}
