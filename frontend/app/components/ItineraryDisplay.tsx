'use client'
import { useState } from 'react'

interface ItineraryDisplayProps {
  itinerary: any
  onNewTrip: () => void
}

export default function ItineraryDisplay({ itinerary, onNewTrip }: ItineraryDisplayProps) {
  const { travel_plan, destination_images, weather_forecast, trip_id } = itinerary
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)

  const imagesList = destination_images?.images || []

  // Calcular custo total somando todas as atividades
  const calculateTotalCost = () => {
    let total = 0
    travel_plan.itinerary_days?.forEach((day: any) => {
      day.activity_recommendations?.forEach((rec: any) => {
        total += parseFloat(rec.activity.price) || 0
      })
    })
    return total.toFixed(2)
  }

  const totalCost = travel_plan.total_cost || calculateTotalCost()

  const getWeatherIcon = (condition: string) => {
    switch (condition) {
      case 'sunny': return '☀️'
      case 'rainy': return '🌧️'
      case 'cloudy': return '☁️'
      case 'partly cloudy': return '⛅'
      default: return '🌤️'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  return (
    <div className="card bg-custom-dark text-ice-white shadow" style={{backgroundColor: '#1a1a1a', border: '1px solid #333'}}>
      {/* Header com imagem de destaque */}
      <div className="position-relative" style={{height: '300px', background: 'linear-gradient(to right, #0d6efd, #6610f2)'}}>
        {destination_images?.featured_image && (
          <img 
            src={destination_images.featured_image.url}
            alt={destination_images.featured_image.description}
            className="w-100 h-100"
            style={{objectFit: 'cover'}}
          />
        )}
        <div className="position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-between p-4" style={{backgroundColor: 'rgba(0,0,0,0.4)'}}>
          <div>
            <h1 className="display-4 fw-bold text-white mb-2">
              🏖️ {travel_plan.city}
            </h1>
            <p className="text-white fs-5">Trip ID: {trip_id}</p>
          </div>
          <button
            onClick={onNewTrip}
            className="btn btn-light btn-lg"
          >
            Nova Viagem
          </button>
        </div>
      </div>

      <div className="card-body p-4">
        {/* Informações da viagem */}
        <div className="mb-4 p-4 rounded" style={{background: 'linear-gradient(to right, rgba(13, 110, 253, 0.2), rgba(102, 16, 242, 0.2))'}}>
          <div className="row">
            <div className="col-md-6">
              <p className="fs-5 mb-2">
                📅 <strong>Chegada:</strong> {formatDate(travel_plan.start_date)}
              </p>
              <p className="fs-5">
                📅 <strong>Partida:</strong> {formatDate(travel_plan.end_date)}
              </p>
            </div>
            <div className="col-md-6">
              <p className="fs-3 fw-bold text-success">
                💰 Custo Total: R$ {totalCost}
              </p>
            </div>
          </div>
        </div>

        {/* Galeria de imagens do destino */}
        {imagesList && imagesList.length > 0 ? (
          <div className="mb-4">
            <h3 className="h4 mb-3">📸 Galeria do Destino ({imagesList.length} fotos)</h3>
            <div className="row g-3">
              {imagesList.map((image: any, index: number) => (
                <div key={image.id || index} className="col-md-3 col-sm-6 col-6">
                  <div 
                    className="position-relative"
                    style={{cursor: 'pointer'}}
                    onClick={() => setSelectedImageIndex(index)}
                  >
                    <img 
                      src={image.thumb_url}
                      alt={image.description}
                      className="w-100 rounded"
                      style={{height: '100px', objectFit: 'cover'}}
                    />
                    <div className="position-absolute bottom-0 end-0 bg-dark bg-opacity-75 text-white px-2 py-1 rounded" style={{fontSize: '0.75rem'}}>
                      📷 {image.photographer}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="mb-4">
            <p className="text-muted">Nenhuma imagem disponível para este destino.</p>
          </div>
        )}

        {/* Previsão do tempo completa */}
        {weather_forecast && weather_forecast.length > 0 && (
          <div className="mb-4">
            <h3 className="h4 mb-3">🌤️ Previsão do Tempo</h3>
            <div className="row g-3">
              {weather_forecast.map((forecast: any, index: number) => (
                <div key={index} className="col-md-4">
                  <div className="card bg-primary text-white text-center p-3">
                    <p className="fw-bold">{formatDate(forecast.date)}</p>
                    <div className="fs-1 my-2">{getWeatherIcon(forecast.condition)}</div>
                    <p className="fs-4 fw-bold">{forecast.temperature}°{forecast.temperature_unit}</p>
                    <p className="text-capitalize">{forecast.condition}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Itinerário detalhado */}
        <div>
          <h3 className="h4 mb-4">📋 Itinerário Detalhado</h3>
          <div>
            {travel_plan.itinerary_days.map((day: any, index: number) => (
              <div key={index} className="border-start border-primary border-4 ps-4 pb-4 mb-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h4 className="h5 fw-bold">
                    📆 {formatDate(day.date)}
                  </h4>
                  <div className="d-flex align-items-center gap-2 bg-primary px-3 py-2 rounded-pill">
                    <span className="fs-4">{getWeatherIcon(day.weather.condition)}</span>
                    <span className="fw-bold">{day.weather.temperature}°{day.weather.temperature_unit}</span>
                  </div>
                </div>

                {day.activity_recommendations.length > 0 ? (
                  <div>
                    {day.activity_recommendations.map((rec: any, actIndex: number) => (
                      <div key={actIndex} className="card bg-secondary text-white mb-3 border-start border-success border-4">
                        <div className="card-body">
                          <div className="d-flex justify-content-between align-items-start mb-3">
                            <h5 className="card-title">{rec.activity.name}</h5>
                            <span className="badge bg-success fs-6">
                              R$ {rec.activity.price}
                            </span>
                          </div>
                          
                          <div className="row mb-3">
                            <div className="col-md-6">
                              <p className="mb-1">
                                📍 {rec.activity.location}
                              </p>
                            </div>
                            <div className="col-md-6">
                              <p className="mb-1">
                                ⏰ {new Date(rec.activity.start_time).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})} - 
                                {new Date(rec.activity.end_time).toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'})}
                              </p>
                            </div>
                          </div>
                          
                          <p className="card-text mb-3">{rec.activity.description}</p>
                          
                          <div className="d-flex flex-wrap gap-2 mb-3">
                            {rec.activity.related_interests.map((interest: string) => (
                              <span key={interest} className="badge bg-info">
                                {interest}
                              </span>
                            ))}
                          </div>
                          
                          {rec.reasons_for_recommendation.length > 0 && (
                            <div className="alert alert-success mb-0">
                              <small>
                                💡 <strong>Por que recomendamos:</strong> {rec.reasons_for_recommendation.join(', ')}
                              </small>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="alert alert-secondary text-center">
                    <p className="mb-0 fst-italic">Nenhuma atividade programada para este dia</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Créditos das imagens */}
        {destination_images?.featured_image && (
          <div className="mt-4 pt-4 border-top border-secondary">
            <p className="text-center text-white small">
              Imagem de destaque por{' '}
              <a 
                href={destination_images.featured_image.photographer_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-info"
              >
                {destination_images.featured_image.photographer}
              </a>
              {' '}via Unsplash 
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
