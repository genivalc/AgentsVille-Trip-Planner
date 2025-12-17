from typing import List
from datetime import date, datetime
from models.schemas import  VacationInfo, TravelPlan, Interest

class TripValidator:
    @staticmethod
    def validate_vacation_info(vacation_info: VacationInfo) -> List[str]:
        """Valida as informações da viagem e retorna lista de erros"""
        errors = []
        
        # Validar datas
        if vacation_info.date_of_arrival >= vacation_info.date_of_departure:
            errors.append("Data de chegada deve ser anterior à data de partida")
        
        if vacation_info.date_of_arrival < date.today():
            errors.append("Data de chegada não pode ser no passado")
        
        # Validar orçamento
        if vacation_info.budget <= 0:
            errors.append("Orçamento deve ser maior que zero")
        
        # Validar viajantes
        if not vacation_info.travelers:
            errors.append("Deve haver pelo menos um viajante")
        
        for traveler in vacation_info.travelers:
            if traveler.age < 0 or traveler.age > 120:
                errors.append(f"Idade inválida para {traveler.name}")
            
            if not traveler.interests:
                errors.append(f"{traveler.name} deve ter pelo menos um interesse")
        
        return errors

    @staticmethod
    def validate_travel_plan(vacation_info: VacationInfo, travel_plan: TravelPlan) -> List[str]:
        """Valida o plano de viagem gerado"""
        errors = []
        
        # Validar datas
        if travel_plan.start_date != vacation_info.date_of_arrival:
            errors.append("Data de início do plano não coincide com data de chegada")
        
        if travel_plan.end_date != vacation_info.date_of_departure:
            errors.append("Data de fim do plano não coincide com data de partida")
        
        # Validar orçamento
        if travel_plan.total_cost > vacation_info.budget:
            errors.append(f"Custo total ({travel_plan.total_cost}) excede o orçamento ({vacation_info.budget})")
        
        # Validar se há atividades para os interesses dos viajantes
        all_traveler_interests = set()
        for traveler in vacation_info.travelers:
            all_traveler_interests.update(traveler.interests)
        
        covered_interests = set()
        for day in travel_plan.itinerary_days:
            for recommendation in day.activity_recommendations:
                covered_interests.update(recommendation.activity.related_interests)
        
        uncovered_interests = all_traveler_interests - covered_interests
        if uncovered_interests:
            errors.append(f"Interesses não atendidos: {list(uncovered_interests)}")
        
        return errors

    @staticmethod
    def validate_budget_distribution(travel_plan: TravelPlan, max_daily_budget: int = None) -> List[str]:
        """Valida a distribuição do orçamento ao longo dos dias"""
        errors = []
        
        daily_costs = []
        for day in travel_plan.itinerary_days:
            daily_cost = sum(
                rec.activity.price for rec in day.activity_recommendations
            )
            daily_costs.append(daily_cost)
        
        if max_daily_budget:
            for i, cost in enumerate(daily_costs):
                if cost > max_daily_budget:
                    errors.append(f"Custo do dia {i+1} ({cost}) excede limite diário ({max_daily_budget})")
        
        # Verificar se o custo total calculado bate com o informado
        calculated_total = sum(daily_costs)
        if calculated_total != travel_plan.total_cost:
            errors.append(f"Custo total informado ({travel_plan.total_cost}) não bate com calculado ({calculated_total})")
        
        return errors
