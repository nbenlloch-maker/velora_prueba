import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from models import ScreeningResult
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURACIÓN DE INFERENCIA LOCAL ---
llm = ChatOpenAI(
    base_url="http://localhost:4891/v1",
    api_key="sk-no-key-required",
    model="DeepSeek-R1-Distill-Qwen-14B",
    temperature=0.1,
    streaming=False
    # NOTA: Sin max_tokens aquí. Usamos la configuración de tu App GPT4All.
)

def extract_json_from_text(text: str) -> dict:
    print("\n🔍 [DEBUG] Buscando JSON dentro del texto recibido...")
    
    start_index = text.find('{')
    end_index = text.rfind('}')

    if start_index == -1 or end_index == -1:
        print("   ❌ ERROR: No se encontraron las llaves del JSON.")
        print(f"   (Texto recibido: {text[:200]}...)")
        raise ValueError("La respuesta de la IA no contiene un objeto JSON {}")

    json_str = text[start_index : end_index + 1]
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"   ❌ [DEBUG] JSON malformado. Intentando corrección rápida...")
        try:
            fixed_str = json_str.replace("'", '"')
            return json.loads(fixed_str)
        except:
            raise ValueError(f"Texto extraído no es JSON válido: {e}")

def analyze_cv(offer_text: str, cv_text: str) -> ScreeningResult:
    print(f"🧠 [Fase 1] Iniciando inferencia con DeepSeek 14B (Local)...")

    system_prompt = """
    Analiza la OFERTA y el CV. Genera ÚNICAMENTE un JSON válido.
    
    ESTRUCTURA OBLIGATORIA:
    {{
        "score": 0.0,
        "discarded": false,
        "matching_requirements": ["req1", "req2"],
        "unmatching_requirements": ["req3"],
        "not_found_requirements": ["req4"],
        "total_requirements_count": 0
    }}

    REGLAS:
    1. Si necesitas pensar, usa etiquetas <think>...</think>.
    2. DESPUÉS de pensar, escribe SOLO el JSON.
    """
    

    prompt = ChatPromptTemplate.from_messages([
        ("system", "hola"),
        ("user", "hola")
    ])

    chain = prompt | llm | StrOutputParser()

    try:
        print("\n⏳ [DEBUG] Enviando petición a GPT4All (Confiando en Settings de la App)...")
        
        raw_response = chain.invoke({"offer": offer_text, "cv": cv_text})
        
        # Logs mínimos para verificar
        print(f"📥 [DEBUG] Respuesta recibida ({len(raw_response)} caracteres).")

        json_data = extract_json_from_text(raw_response)
        return ScreeningResult(**json_data)
        
    except Exception as e:
        print(f"⚠️ [CRASH] Error final en analyze_cv: {e}")
        raise e