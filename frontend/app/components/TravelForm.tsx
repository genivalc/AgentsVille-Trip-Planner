'use client'
import { useState } from 'react'
import { generateItinerary } from '../services/api'

interface TravelFormProps {
  onItineraryGenerated: (itinerary: any) => void
  loading: boolean
  setLoading: (loading: boolean) => void
}

export default function TravelForm({ onItineraryGenerated, loading, setLoading }: TravelFormProps) {
  const [formData, setFormData] = useState({
    travelers: [{ name: '', age: '', interests: [] }],
    destination: '',
    date_of_arrival: '',
    date_of_departure: '',
    budget: ''
  })

  const interestsMap: { [key: string]: string } = {
    'arte': 'art',
    'culinária': 'cooking',
    'dança': 'dancing',
    'fitness': 'fitness',
    'trilha': 'hiking',
    'música': 'music',
    'fotografia': 'photography',
    'leitura': 'reading',
    'esportes': 'sports',
    'tecnologia': 'technology'
  }

  const interests = Object.keys(interestsMap)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const processedData = {
        ...formData,
        travelers: formData.travelers.map(t => ({
          ...t,
          age: parseInt(t.age),
          interests: t.interests.map(i => interestsMap[i] || i)
        })),
        budget: parseInt(formData.budget)
      }
      
      const result = await generateItinerary(processedData)
      onItineraryGenerated(result)
    } catch (error) {
      alert('Erro ao gerar itinerário: ' + error)
    } finally {
      setLoading(false)
    }
  }

  const updateTraveler = (index: number, field: string, value: any) => {
    const newTravelers = [...formData.travelers]
    newTravelers[index] = { ...newTravelers[index], [field]: value }
    setFormData({ ...formData, travelers: newTravelers })
  }

  const toggleInterest = (travelerIndex: number, interest: string) => {
    const traveler = formData.travelers[travelerIndex]
    const newInterests = traveler.interests.includes(interest)
      ? traveler.interests.filter(i => i !== interest)
      : [...traveler.interests, interest]
    
    updateTraveler(travelerIndex, 'interests', newInterests)
  }

  return (
    <form onSubmit={handleSubmit} className="card bg-custom-dark text-ice-white p-4 shadow" style={{backgroundColor: '#1a1a1a', border: '1px solid #333'}}>
      <h2 className="h3 mb-4">Planeje sua Viagem</h2>
      
      {/* Viajantes */}
      <div className="mb-4">
        <h3 className="h5 mb-3">Viajantes</h3>
        {formData.travelers.map((traveler, index) => (
          <div key={index} className="border border-secondary rounded p-3 mb-3">
            <div className="row g-3 mb-3">
              <div className="col-md-6">
                <input
                  type="text"
                  placeholder="Nome"
                  value={traveler.name}
                  onChange={(e) => updateTraveler(index, 'name', e.target.value)}
                  className="form-control"
                  required
                />
              </div>
              <div className="col-md-6">
                <input
                  type="number"
                  placeholder="Idade"
                  value={traveler.age}
                  onChange={(e) => updateTraveler(index, 'age', e.target.value)}
                  className="form-control"
                  required
                />
              </div>
            </div>
            
            <div>
              <p className="fw-bold mb-2">Interesses:</p>
              <div className="row g-2">
                {interests.map(interest => (
                  <div key={interest} className="col-md-4">
                    <div className="form-check">
                      <input
                        type="checkbox"
                        checked={traveler.interests.includes(interest)}
                        onChange={() => toggleInterest(index, interest)}
                        className="form-check-input"
                        id={`interest-${index}-${interest}`}
                      />
                      <label className="form-check-label text-white" htmlFor={`interest-${index}-${interest}`}>
                        {interest}
                      </label>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Destino e Datas */}
      <div className="row g-3 mb-4">
        <div className="col-md-4">
          <input
            type="text"
            placeholder="Destino"
            value={formData.destination}
            onChange={(e) => setFormData({...formData, destination: e.target.value})}
            className="form-control"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            type="date"
            value={formData.date_of_arrival}
            onChange={(e) => setFormData({...formData, date_of_arrival: e.target.value})}
            className="form-control"
            required
          />
        </div>
        <div className="col-md-4">
          <input
            type="date"
            value={formData.date_of_departure}
            onChange={(e) => setFormData({...formData, date_of_departure: e.target.value})}
            className="form-control"
            required
          />
        </div>
      </div>

      {/* Orçamento */}
      <div className="mb-4">
        <input
          type="number"
          placeholder="Orçamento (R$)"
          value={formData.budget}
          onChange={(e) => setFormData({...formData, budget: e.target.value})}
          className="form-control"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="btn btn-primary w-100 py-2"
      >
        {loading ? 'Gerando Itinerário...' : 'Gerar Itinerário'}
      </button>
    </form>
  )
}
