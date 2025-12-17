import datetime
import os
import requests
from typing import Dict, List, Optional
from models.schemas import Weather

class WeatherService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_weather_forecast(self, date: str, city: str) -> Dict:
        """Retorna a previsão do tempo para uma data e cidade específicas"""
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Formato de data inválido: {date}")

        if not self.api_key:
            return self._get_mock_weather(date, city)
        
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "pt_br"
            }
            
            response = requests.get(
                f"{self.base_url}/forecast",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                
                for forecast in data.get("list", []):
                    forecast_date = datetime.datetime.fromtimestamp(forecast["dt"]).date()
                    if forecast_date == target_date:
                        return {
                            "date": date,
                            "city": city,
                            "temperature": round(forecast["main"]["temp"]),
                            "temperature_unit": "celsius",
                            "condition": forecast["weather"][0]["main"].lower(),
                            "description": forecast["weather"][0]["description"]
                        }
        except Exception as e:
            print(f"Erro ao buscar clima: {e}")
        
        return self._get_mock_weather(date, city)

    def get_weather_range(self, start_date: str, end_date: str, city: str) -> List[Dict]:
        """Retorna previsão do tempo para um período"""
        import pandas as pd
        
        weather_data = []
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            weather = self.get_weather_forecast(date_str, city)
            weather_data.append(weather)
        
        return weather_data

    def is_outdoor_friendly(self, condition: str) -> bool:
        """Verifica se as condições climáticas são favoráveis para atividades ao ar livre"""
        unfriendly_conditions = ["thunderstorm", "rain", "drizzle", "snow"]
        return condition.lower() not in unfriendly_conditions
    
    def _get_mock_weather(self, date: str, city: str) -> Dict:
        """Retorna dados mockados quando a API não está disponível"""
        return {
            "date": date,
            "city": city,
            "temperature": 25,
            "temperature_unit": "celsius",
            "condition": "partly cloudy",
            "description": f"Previsão do tempo para {city} em {date}"
        }
