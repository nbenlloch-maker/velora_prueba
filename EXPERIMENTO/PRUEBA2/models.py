from pydantic import BaseModel, Field
from typing import List

class ScreeningResult(BaseModel):
    """
    Estructura de salida de la Fase 1.
    """
    score: float = Field(description="Puntuación de 0 a 100. (Coincidencias / Total * 100). Si discarded es True, esto es 0.")
    discarded: bool = Field(description="True si el candidato incumple explícitamente un requisito OBLIGATORIO.")
    matching_requirements: List[str] = Field(description="Lista de requisitos que SÍ aparecen en el CV.")
    unmatching_requirements: List[str] = Field(description="Lista de requisitos que el candidato explícitamente NO cumple.")
    not_found_requirements: List[str] = Field(description="Lista de requisitos que NO aparecen en el CV (ni sí ni no) y se deben preguntar.")
    
    # Campo auxiliar para saber cuántos eran en total y poder recalcular luego
    total_requirements_count: int = Field(description="Número total de requisitos identificados en la oferta (desglosando los compuestos).")