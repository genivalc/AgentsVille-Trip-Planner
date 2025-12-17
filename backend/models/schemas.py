from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import datetime

class Interest(str, Enum):
    ART = "art"
    COOKING = "cooking"
    COMEDY = "comedy"
    DANCING = "dancing"
    FITNESS = "fitness"
    GARDENING = "gardening"
    HIKING = "hiking"
    MOVIES = "movies"
    MUSIC = "music"
    PHOTOGRAPHY = "photography"
    READING = "reading"
    SPORTS = "sports"
    TECHNOLOGY = "technology"
    THEATRE = "theatre"
    TENNIS = "tennis"
    WRITING = "writing"

class Traveler(BaseModel):
    name: str
    age: int
    interests: List[Interest]

class VacationInfo(BaseModel):
    travelers: List[Traveler]
    destination: str
    date_of_arrival: datetime.date
    date_of_departure: datetime.date
    budget: int

class Weather(BaseModel):
    temperature: float
    temperature_unit: str
    condition: str
    description: Optional[str] = None

class Activity(BaseModel):
    activity_id: str
    name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    location: str
    description: str
    price: int
    related_interests: List[Interest]

class ActivityRecommendation(BaseModel):
    activity: Activity
    reasons_for_recommendation: List[str]

class ItineraryDay(BaseModel):
    date: datetime.date
    weather: Weather
    activity_recommendations: List[ActivityRecommendation]

class TravelPlan(BaseModel):
    city: str
    start_date: datetime.date
    end_date: datetime.date
    total_cost: int
    itinerary_days: List[ItineraryDay]

class TripHistory(BaseModel):
    id: str
    vacation_info: VacationInfo
    travel_plan: TravelPlan
    created_at: datetime.datetime
    modifications: List[dict] = []
