import datetime
import os
from typing import List, Dict, Optional
import google.genai as genai
import json
from models.schemas import Activity, Interest

class ActivitiesService:
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))

    def _generate_activities_with_gemini(self, date: str, city: str = None, interests: List[str] = None, count: int = 3) -> List[Dict]:
        """Gera atividades usando Gemini"""
        city = city
        interests_str = ", ".join(interests) if interests else "variados"
        
        valid_interests = ["art", "cooking", "comedy", "dancing", "fitness", "gardening", "hiking", "movies", "music", "photography", "reading", "sports", "technology", "theatre", "tennis", "writing"]

        prompt = f"""
        Gere {count} atividades turísticas para {city} na data {date}.
        Interesses: {interests_str}

        IMPORTANTE: Use apenas estes interesses válidos: {', '.join(valid_interests)}

        Retorne APENAS um JSON válido no formato:
        [
            {{
                "activity_id": "event-{date}-1",
                "name": "Nome da Atividade",
                "start_time": "{date} HH:MM",
                "end_time": "{date} HH:MM",
                "location": "Local específico em {city}",
                "description": "Descrição detalhada da atividade",
                "price": 25,
                "related_interests": ["interesse1", "interesse2"]
            }}
        ]
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-lite',
                contents=prompt
            )
            content = response.text.strip()
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            activities = json.loads(content)
            return activities if isinstance(activities, list) else [activities]
            
        except Exception as e:
            print(f"Erro ao gerar atividades: {e}")
            return self._get_default_activities(date, city)

    def _get_default_activities(self, date: str, city: str = None) -> List[Dict]:
        """Retorna atividades padrão quando não é possível gerar"""
        city = city or "Local"
        return [{
            "activity_id": f"default-{date}-1",
            "name": "Atividade não encontrada",
            "start_time": f"{date} 10:00",
            "end_time": f"{date} 12:00",
            "location": f"{city}",
            "description": "Não foi possível encontrar atividades para esta data e local.",
            "price": 0,
            "related_interests": []
        }]

    def get_activities_by_date(self, date: str, city: str = None, activity_ids: List[str] = None) -> List[Dict]:
        """Retorna atividades para uma data específica"""
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Formato de data inválido: {date}")

        return self._generate_activities_with_gemini(date, city)

    def get_activity_by_id(self, activity_id: str) -> Optional[Dict]:
        """Retorna uma atividade específica pelo ID"""
        if "event-" in activity_id:
            date_part = activity_id.split("-")[1:4]
            if len(date_part) == 3:
                date = "-".join(date_part)
                activities = self._generate_activities_with_gemini(date, count=1)
                if activities:
                    activities[0]["activity_id"] = activity_id
                    return activities[0]
        return None

    def get_activities_by_interests(self, interests: List[str], date: str = None) -> List[Dict]:
        """Retorna atividades que correspondem aos interesses especificados"""
        if date:
            return self._generate_activities_with_gemini(date, interests=interests)
        else:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            return self._generate_activities_with_gemini(tomorrow, interests=interests)

    def filter_activities_by_weather(self, activities: List[Dict], weather_condition: str) -> List[Dict]:
        """Filtra atividades baseado nas condições climáticas"""
        if weather_condition.lower() in ["thunderstorm", "rainy", "heavy rain"]:
            return [
                activity for activity in activities
                if "indoor" in activity.get("description", "").lower() or
                   "hall" in activity.get("location", "").lower() or
                   "center" in activity.get("location", "").lower()
            ]
        return activities

    def calculate_total_cost(self, activities: List[Dict]) -> int:
        """Calcula o custo total das atividades"""
        return sum(activity.get("price", 0) for activity in activities)
