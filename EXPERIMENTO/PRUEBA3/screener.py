import json
import re
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models import ScreeningResult
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN DE INFERENCIA LOCAL ---
# Usamos os.getenv para permitir la inyección de la URL desde Docker
llm = ChatOpenAI(
    base_url=os.getenv("LLM_URL", "http://localhost:4891/v1"),
    api_key="sk-no-key-required",
    model="DeepSeek-R1-Distill-Qwen-14B",
    temperature=0.1,
    streaming=False,
    max_tokens=8192,  # Espacio suficiente para pensar
    timeout=600
)

def extract_json_from_text(text: str) -> dict:
    """Extrae JSON válido ignorando el bloque <think>."""
    print("\n🔍 [DEBUG] Buscando JSON dentro del texto recibido...")
    
    # 1. Limpieza de etiquetas de pensamiento
    if "</think>" in text:
        clean_text = text.split("</think>")[-1]
    else:
        clean_text = text
        
    # 2. Búsqueda con Regex (encuentra lo que esté entre { y })
    match = re.search(r"\{.*\}", clean_text, re.DOTALL)
    
    if match:
        json_str = match.group(0)
    else:
        # Intento de rescate en texto crudo
        match_raw = re.search(r"\{.*\}", text, re.DOTALL)
        if match_raw:
            json_str = match_raw.group(0)
        else:
            print("   ❌ ERROR: No se encontraron las llaves del JSON.")
            print(f"   (Final del texto: ...{text[-200:]})")
            raise ValueError("La respuesta de la IA no contiene un objeto JSON {}")

    try:
        # 3. Limpiezas comunes de formato
        fixed_str = json_str.replace("'", '"')
        fixed_str = fixed_str.replace("True", "true").replace("False", "false")
        # Eliminar comas finales (trailing commas)
        fixed_str = re.sub(r",\s*([\]}])", r"\1", fixed_str)
        return json.loads(fixed_str)
    except Exception as e:
        raise ValueError(f"JSON malformado: {e}")

def analyze_cv(offer_text: str, cv_text: str) -> ScreeningResult:
    print(f"🧠 [Fase 1] Iniciando inferencia con DeepSeek 14B (Chain of Thought)...")

    # Prompt con Chain of Thought y Dobles Llaves {{ }}
    system_prompt = """
    Eres un reclutador experto (Velora AI). Tu tarea es cruzar una OFERTA con un CV.
    
    PASOS DE RAZONAMIENTO (Chain of Thought):
    1. Lee la oferta y extrae la lista de requisitos.
    2. Busca evidencia en el CV para cada requisito.
    3. Clasifica cada uno como "matching" (cumple), "unmatching" (no cumple explícitamente) o "not_found" (no se menciona).
    4. Calcula mentalmente un SCORE de 0 a 100 basado en el % de requisitos cumplidos.
    
    SALIDA FINAL OBLIGATORIA (JSON):
    Genera ÚNICAMENTE este objeto JSON al final. No añadas texto fuera del JSON (salvo tu pensamiento interno en <think>).
    
    {{
        "score": 0.0,
        "discarded": false,
        "matching_requirements": ["Python 3 años", "Ingeniería"],
        "unmatching_requirements": [],
        "not_found_requirements": ["LangChain"],
        "total_requirements_count": 0
    }}
    
    Nota: "discarded" es true SOLO si falta un requisito marcado como "Obligatorio" o "Excluyente".
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "ESTA ES LA OFERTA:\n{offer}\n\nESTE ES EL CV:\n{cv}")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        print("\n⏳ [DEBUG] Enviando petición a DeepSeek...")
        raw_response = chain.invoke({"offer": offer_text, "cv": cv_text})
        
        has_thought = "<think>" in raw_response
        print(f"📥 [DEBUG] Respuesta recibida. ¿Usó Chain of Thought? {'✅ SÍ' if has_thought else '❌ NO'}")
        
        json_data = extract_json_from_text(raw_response)
        return ScreeningResult(**json_data)
        
    except Exception as e:
        print(f"⚠️ [CRASH] Error final en analyze_cv: {e}")
        raise e