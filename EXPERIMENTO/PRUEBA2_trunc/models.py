from pydantic import BaseModel, Field
from typing import List

class ScreeningResult(BaseModel):
    score: float = Field(description="Puntuación de 0 a 100.")
    discarded: bool = Field(description="True si incumple un requisito obligatorio explícito.")
    matching_requirements: List[str] = Field(description="Requisitos encontrados en el CV.")
    unmatching_requirements: List[str] = Field(description="Requisitos que explícitamente NO cumple.")
    not_found_requirements: List[str] = Field(description="Requisitos no mencionados (dudas).")
    total_requirements_count: int = Field(description="Total de requisitos de la oferta.")
    