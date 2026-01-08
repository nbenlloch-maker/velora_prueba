from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models import ScreeningResult
import os
from dotenv import load_dotenv

load_dotenv()

# Usamos GPT-4o o GPT-3.5-turbo si tienes poco saldo
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def analyze_cv(offer_text: str, cv_text: str) -> ScreeningResult:
    """
    Analiza la oferta y el CV, extrae requisitos y calcula la puntuación inicial.
    """
    print("🧠 [Fase 1] Analizando CV contra Oferta...")

    system_prompt = """
    Eres un reclutador experto de IA "Velora". Tu trabajo es cruzar una Oferta y un CV.
    
    INSTRUCCIONES CRÍTICAS:
    1. **Desglosa requisitos**: Si una línea dice "Valorable FastAPI y LangChain", son DOS requisitos distintos.
    2. **Clasificación**:
       - `matching_requirements`: El CV lo menciona claramente.
       - `unmatching_requirements`: El CV dice explícitamente que NO lo tiene o es incompatible (ej: Pide "Inglés C1" y CV dice "Inglés A2").
       - `not_found_requirements`: El CV no dice nada al respecto.
    3. **Reglas de Descarte**:
       - Si un requisito OBLIGATORIO está en `unmatching`, `discarded` es True y `score` es 0.
       - Si falta información (`not_found`), NO se descarta.
    4. **Cálculo de Score**:
       - (Número de Matching / Número Total de Requisitos desglosados) * 100.
    
    Devuelve estrictamente un JSON con el modelo solicitado.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "OFERTA:\n{offer}\n\nCURRICULUM:\n{cv}")
    ])

    # Obligamos a que la salida sea el modelo Pydantic
    structured_llm = llm.with_structured_output(ScreeningResult)
    chain = prompt | structured_llm

    result = chain.invoke({"offer": offer_text, "cv": cv_text})
    return result