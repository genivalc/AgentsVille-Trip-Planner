'use client'
import { useState } from 'react'
import ItineraryDisplay from './components/ItineraryDisplay'
import TravelForm from './components/TravelForm'

export default function Home() {
  const [itinerary, setItinerary] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="container py-4" style={{maxWidth: '1200px'}}>
      <h1 className="text-center mb-4 text-ice-white" style={{fontSize: '2.5rem', fontWeight: 'bold', color: '#f8f9fa'}}>
        🌍 AgentsVille Trip Planner
      </h1>
      
      {!itinerary ? (
        <TravelForm 
          onItineraryGenerated={setItinerary}
          loading={loading}
          setLoading={setLoading}
        />
      ) : (
        <ItineraryDisplay 
          itinerary={itinerary}
          onNewTrip={() => setItinerary(null)}
        />
      )}
    </div>
  )
}
