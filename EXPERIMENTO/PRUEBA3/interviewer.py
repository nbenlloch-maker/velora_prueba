import os
from models import ScreeningResult
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURACIÓN DEL MODELO LOCAL ---
# Usamos la variable de entorno para Docker
llm = ChatOpenAI(
    base_url=os.getenv("LLM_URL", "http://localhost:4891/v1"),
    api_key="sk-no-key-required",
    model="DeepSeek-R1-Distill-Qwen-14B", 
    temperature=0.3,
    streaming=False
)

def validate_answer(requirement: str, user_answer: str) -> bool:
    """Usa la IA para validar si la respuesta cuenta como experiencia real."""
    prompt = ChatPromptTemplate.from_template(
        "Eres un evaluador técnico estricto. \n"
        "Requisito buscado: '{req}'. \n"
        "Respuesta del candidato: '{ans}'. \n\n"
        "Analiza si el candidato realmente tiene la experiencia requerida.\n"
        "Responde SOLO con la palabra 'SI' si cumple, o 'NO' si no cumple o es ambiguo."
    )
    
    chain = prompt | llm
    
    try:
        res = chain.invoke({"req": requirement, "ans": user_answer})
        content = res.content
        # Limpieza de <think> por si acaso
        if "<think>" in content:
            content = content.split("</think>")[-1]
            
        return "SI" in content.strip().upper()
    except Exception as e:
        print(f"(Error validando: {e}) -> Asumimos NO")
        return False

def start_interview(initial_result: ScreeningResult) -> float:
    print("\n" + "="*50)
    print("🎤 [Fase 2] ENTREVISTA DE COMPLETADO DE PERFIL (IA LOCAL)")
    print("="*50)
    
    missing_items = initial_result.not_found_requirements
    
    if not missing_items:
        print("✅ No hay requisitos faltantes. Entrevista no necesaria.")
        return initial_result.score

    print(f"🤖 Velora (DeepSeek): Hola. He analizado tu CV y tengo {len(missing_items)} dudas.")
    
    new_matches = 0

    for req in missing_items:
        print(f"\n🤖 Pregunta: ¿Tienes experiencia o conocimientos en: '{req}'?")
        respuesta = input("👤 Tú: ")
        
        print("   (Analizando respuesta con IA local...)")
        es_valido = validate_answer(req, respuesta)
        
        if es_valido:
            print("   ✅ Respuesta aceptada.")
            new_matches += 1
            initial_result.matching_requirements.append(req)
        else:
            print("   ❌ Respuesta no válida o insuficiente.")
    
    # Cálculo final
    total_reqs = initial_result.total_requirements_count
    total_matches = len(initial_result.matching_requirements) 
    
    if total_reqs == 0: return 0.0

    final_score = (total_matches / total_reqs) * 100
    return round(final_score, 2)