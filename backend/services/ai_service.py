import json
from openai import OpenAI
from typing import Optional
from models.schemas import VacationInfo, TravelPlan

class AIService:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = "gpt-3.5-turbo"

    def generate_itinerary(self, vacation_info: VacationInfo, weather_data: list, activities_data: list) -> TravelPlan:
        system_prompt = f"""
        Você é um Agente Especialista em Planejamento de Itinerários.

        ## Tarefa
        Crie um itinerário de viagem personalizado considerando:
        1. Interesses dos viajantes
        2. Condições climáticas (evite atividades ao ar livre durante chuva)
        3. Orçamento disponível (não exceda o limite)
        4. Pelo menos uma atividade por dia
        5. Compatibilidade entre atividades e clima

        ## Formato de Saída
        Responda usando duas seções (ANÁLISE E SAÍDA FINAL) no seguinte formato:

        ANÁLISE:
        - Análise passo a passo das preferências dos viajantes
        - Considerações sobre o clima para cada dia
        - Seleção de atividades baseada nos interesses
        - Cálculo e verificação do orçamento

        SAÍDA FINAL:

        ```json
        {TravelPlan.model_json_schema()}
        ```

        ## Contexto
        Dados do clima: {json.dumps(weather_data, indent=2)}
        Atividades disponíveis: {json.dumps(activities_data, indent=2)}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": vacation_info.model_dump_json(indent=2)}
                ],
                temperature=0.7
            )

            content = response.choices[0].message.content
            
            # Extrair JSON da resposta
            json_text = content.strip()
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()

            travel_plan = TravelPlan.model_validate_json(json_text)
            return travel_plan

        except Exception as e:
            raise Exception(f"Erro ao gerar itinerário: {str(e)}")

    def modify_itinerary(self, current_plan: TravelPlan, modification_request: str) -> TravelPlan:
        """Modifica um itinerário existente baseado em uma solicitação"""
        system_prompt = """
        Você é um especialista em modificação de itinerários de viagem.
        Modifique o itinerário existente baseado na solicitação do usuário.
        Mantenha a estrutura JSON original e faça apenas as alterações necessárias.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Itinerário atual: {current_plan.model_dump_json()}\n\nModificação solicitada: {modification_request}"}
                ],
                temperature=0.7
            )

            content = response.choices[0].message.content
            
            # Extrair JSON da resposta
            json_text = content.strip()
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()

            modified_plan = TravelPlan.model_validate_json(json_text)
            return modified_plan

        except Exception as e:
            raise Exception(f"Erro ao modificar itinerário: {str(e)}")
