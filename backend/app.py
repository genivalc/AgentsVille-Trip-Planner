import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import uuid
from datetime import datetime
from typing import Dict, List

from models.schemas import VacationInfo, TravelPlan, TripHistory
from services.ai_service import AIService
from services.weather_service import WeatherService
from services.activities_service import ActivitiesService
from services.image_service import ImageService
from utils.validators import TripValidator

load_dotenv()

app = Flask(__name__)
CORS(app)

# Inicializar serviços
ai_service = AIService(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
weather_service = WeatherService()
activities_service = ActivitiesService()
image_service = ImageService()

trip_history: Dict[str, TripHistory] = {}

@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de verificação da API"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route("/api/generate-itinerary", methods=["POST"])
def generate_itinerary():
    """Gera um novo itinerário de viagem"""
    try:
        # Validar dados de entrada
        data = request.get_json()
        vacation_info = VacationInfo.model_validate(data)
        
        # Validar informações da viagem
        validation_errors = TripValidator.validate_vacation_info(vacation_info)
        if validation_errors:
            return jsonify({"error": "Dados inválidos", "details": validation_errors}), 400
        
        # Obter dados de clima
        weather_data = weather_service.get_weather_range(
            start_date=vacation_info.date_of_arrival.strftime("%Y-%m-%d"),
            end_date=vacation_info.date_of_departure.strftime("%Y-%m-%d"),
            city=vacation_info.destination
        )
        
        # Obter atividades disponíveis
        all_interests = []
        for traveler in vacation_info.travelers:
            all_interests.extend([interest.value for interest in traveler.interests])
        
        activities_data = []
        import pandas as pd
        date_range = pd.date_range(
            start=vacation_info.date_of_arrival,
            end=vacation_info.date_of_departure,
            freq='D'
        )
        
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            daily_activities = activities_service.get_activities_by_interests(
                interests=all_interests,
                date=date_str
            )
            activities_data.extend(daily_activities)
        
        # Gerar itinerário(LLM)
        travel_plan = ai_service.generate_itinerary(
            vacation_info=vacation_info,
            weather_data=weather_data,
            activities_data=activities_data
        )
        
        # Validar plano gerado
        plan_validation_errors = TripValidator.validate_travel_plan(vacation_info, travel_plan)
        if plan_validation_errors:
            return jsonify({
                "warning": "Plano gerado com problemas",
                "validation_errors": plan_validation_errors,
                "travel_plan": travel_plan.model_dump()
            }), 200
        
        # Salvar no histórico
        trip_id = str(uuid.uuid4())
        trip_history[trip_id] = TripHistory(
            id=trip_id,
            vacation_info=vacation_info,
            travel_plan=travel_plan,
            created_at=datetime.now()
        )
        
        # Obter imagens do destino
        destination_images = image_service.get_destination_gallery(vacation_info.destination)
        
        return jsonify({
            "trip_id": trip_id,
            "travel_plan": travel_plan.model_dump(),
            "destination_images": destination_images,
            "weather_forecast": weather_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/modify-itinerary/<trip_id>", methods=["POST"])
def modify_itinerary(trip_id: str):
    """Modifica um itinerário existente"""
    try:
        if trip_id not in trip_history:
            return jsonify({"error": "Viagem não encontrada"}), 404
        
        data = request.get_json()
        modification_request = data.get("modification_request", "")
        
        if not modification_request:
            return jsonify({"error": "Solicitação de modificação é obrigatória"}), 400
        
        current_trip = trip_history[trip_id]
        
        # Modificar itinerário usando IA
        modified_plan = ai_service.modify_itinerary(
            current_plan=current_trip.travel_plan,
            modification_request=modification_request
        )
        
        # Atualizar histórico
        current_trip.travel_plan = modified_plan
        current_trip.modifications.append({
            "timestamp": datetime.now().isoformat(),
            "request": modification_request,
            "type": "user_modification"
        })
        
        return jsonify({
            "trip_id": trip_id,
            "travel_plan": modified_plan.model_dump(),
            "modification_applied": modification_request
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/trip-history", methods=["GET"])
def get_trip_history():
    """Retorna o histórico de viagens"""
    history_list = []
    for trip in trip_history.values():
        history_list.append({
            "id": trip.id,
            "destination": trip.vacation_info.destination,
            "travelers": [t.name for t in trip.vacation_info.travelers],
            "dates": f"{trip.vacation_info.date_of_arrival} to {trip.vacation_info.date_of_departure}",
            "total_cost": trip.travel_plan.total_cost,
            "created_at": trip.created_at.isoformat(),
            "modifications_count": len(trip.modifications)
        })
    
    return jsonify({"trips": history_list})

@app.route("/api/trip/<trip_id>", methods=["GET"])
def get_trip_details(trip_id: str):
    """Retorna detalhes de uma viagem específica"""
    if trip_id not in trip_history:
        return jsonify({"error": "Viagem não encontrada"}), 404
    
    trip = trip_history[trip_id]
    return jsonify({
        "trip": trip.model_dump(),
        "destination_images": image_service.get_destination_gallery(trip.vacation_info.destination)
    })

@app.route("/api/weather/<city>/<date>", methods=["GET"])
def get_weather(city: str, date: str):
    """Retorna informações do clima para uma cidade e data"""
    try:
        weather = weather_service.get_weather_forecast(date, city)
        return jsonify(weather)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/activities", methods=["GET"])
def get_activities():
    """Retorna atividades disponíveis"""
    date = request.args.get("date")
    city = request.args.get("city")
    interests = request.args.getlist("interests")
    
    if interests:
        activities = activities_service.get_activities_by_interests(interests, date)
    elif date:
        activities = activities_service.get_activities_by_date(date, city)
    else:
        return jsonify({"error": "Parâmetros insuficientes"}), 400
    
    return jsonify({"activities": activities})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
