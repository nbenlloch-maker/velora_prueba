# models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ScreeningResult(BaseModel):
    """
    Esta clase define la estructura estricta (JSON) que la IA debe devolver.
    Actúa como un "molde" para asegurar que siempre tengamos los datos necesarios.
    """
    
    # La puntuación calculada matemáticamente (Matches / Total * 100)
    score: float = Field(description="Puntuación de 0 a 100.")
    
    # Flag de seguridad: Si falta un requisito obligatorio, esto es True y se descarta.
    discarded: bool = Field(description="True si incumple requisitos obligatorios.")
    
    # Listas para clasificar cada requisito encontrado en la oferta
    matching_requirements: List[str] = Field(description="Lista de requisitos que SÍ cumple.")
    unmatching_requirements: List[str] = Field(description="Lista de requisitos que explícitamente NO cumple.")
    not_found_requirements: List[str] = Field(description="Lista de requisitos que NO aparecen en el CV (duda).")
    
    # Dato clave para hacer la regla de tres matemática después
    total_requirements_count: int = Field(description="Número total de requisitos desglosados.")
    
    # Campo nuevo para la integración con WhatsApp (puede estar vacío si el CV no tiene teléfono)
    phone: Optional[str] = Field(description="Número de teléfono extraído del CV. Null si no existe.")
    email: Optional[str] = Field(description="Correo electrónico extraído del CV. Null si no existe.")