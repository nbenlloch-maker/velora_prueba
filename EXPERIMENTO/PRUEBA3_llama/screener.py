# screener.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from models import ScreeningResult
import os
from dotenv import load_dotenv

# Cargamos variables de entorno (por si usáramos claves privadas, buena práctica)
load_dotenv()

# --- CONFIGURACIÓN DEL MODELO ---
# Usamos 'deepseek-r1:8b' porque razona muy bien. 
# Temperature=0 hace que sea "aburrido" pero preciso (no se inventa datos).
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)

def analyze_cv(offer_text: str, cv_text: str) -> ScreeningResult:
    """
    Función principal de la Fase 1: Cruza la Oferta con el CV.
    """
    print("🧠 [Fase 1] IA Analizando documentos y desglosando requisitos...")

    # --- EL PROMPT (LAS INSTRUCCIONES AL CEREBRO) ---
    system_prompt = """
    Eres un sistema experto ATS (Applicant Tracking System).
    
    TU MISIÓN:
    1. Analizar la OFERTA y el CV.
    2. Extraer el número de teléfono del candidato si existe.
    
    REGLAS CRÍTICAS DE DESGLOSE (OBLIGATORIO):
    - Si una línea dice "Python y Java", SON DOS REQUISITOS SEPARADOS.
    - Debes separar por "y", "e", ",".
    
    REGLAS DE CLASIFICACIÓN:
    - matching: El CV lo tiene.
    - unmatching: El CV dice que NO lo tiene (o es incompatible).
    - not_found: El CV no dice nada (IMPORTANTE: Ante la duda, usa esta categoría).
    
    REGLAS DE DESCARTE:
    - discarded = True SOLO si falta un requisito marcado como 'Obligatorio'/'Mínimo' en la oferta.
    
    Salida: Únicamente el JSON estricto.
    """

    # Preparamos la plantilla de conversación
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "OFERTA:\n{offer}\n\nCURRICULUM:\n{cv}")
    ])

    # Obligamos al modelo a usar la estructura de 'models.py'
    structured_llm = llm.with_structured_output(ScreeningResult)
    
    # Creamos la cadena (Chain) y la ejecutamos
    chain = prompt | structured_llm
    result = chain.invoke({"offer": offer_text, "cv": cv_text})
    
    return result