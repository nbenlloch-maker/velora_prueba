from pydantic import BaseModel, Field
from typing import List, Optional

class ScreeningResult(BaseModel):
    score: float = Field(description="Puntuación calculada de 0 a 100.")
    discarded: bool = Field(description="Indica si el candidato está descartado por incumplir obligatorios.")
    matching_requirements: List[str] = Field(description="Lista de requisitos encontrados en el CV.")
    unmatching_requirements: List[str] = Field(description="Lista de requisitos que NO cumple explícitamente.")
    not_found_requirements: List[str] = Field(description="Lista de requisitos que NO se mencionan en el CV.")
    # Campo interno para ayudar al cálculo posterior, no se mostrará en el JSON final si no queremos
    total_requirements_count: int = Field(description="Número total de requisitos extraídos.")