from models import ScreeningResult
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Instancia del LLM para validar respuestas del usuario
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def validate_answer(requirement: str, user_answer: str) -> bool:
    """
    Usa la IA para decidir si la respuesta del usuario cuenta como un SÍ o un NO.
    """
    prompt = ChatPromptTemplate.from_template(
        "Eres un evaluador estricto. Requisito buscado: '{req}'. "
        "Respuesta del candidato: '{ans}'. "
        "¿El candidato cumple el requisito basándose en su respuesta? "
        "Responde solo 'SI' o 'NO'."
    )
    chain = prompt | llm
    res = chain.invoke({"req": requirement, "ans": user_answer})
    return "SI" in res.content.upper()

def start_interview(initial_result: ScreeningResult) -> float:
    """
    Recorre los requisitos no encontrados, entrevista al candidato y recalcula la nota.
    """
    print("\n" + "="*50)
    print("🎤 [Fase 2] ENTREVISTA DE COMPLETADO DE PERFIL")
    print("="*50)
    
    missing_items = initial_result.not_found_requirements
    
    if not missing_items:
        print("✅ No hay requisitos faltantes. La entrevista no es necesaria.")
        return initial_result.score

    print(f"🤖 IA: Hola. He visto tu CV y necesito aclararte {len(missing_items)} puntos que no encontré.")
    
    new_matches = 0

    # Bucle de preguntas
    for req in missing_items:
        print(f"\n🤖 IA: ¿Tienes experiencia o conocimientos en: '{req}'?")
        respuesta = input("👤 Tú: ")
        
        # Validamos con IA si la respuesta es positiva
        if validate_answer(req, respuesta):
            print("   (✅ Requisito validado)")
            new_matches += 1
            # Movemos el requisito de 'not_found' a 'matching' (virtualmente)
            initial_result.matching_requirements.append(req)
        else:
            print("   (❌ Requisito no cumplido)")
    
    # --- CÁLCULO FINAL (Lógica matemática del PDF) ---
    # Total de requisitos originales
    total_reqs = initial_result.total_requirements_count
    
    # Total cumplidos = Los que ya tenía + los nuevos validados
    total_matches = len(initial_result.matching_requirements) # Ya incluye los nuevos porque hicimos append arriba
    
    # Regla de 3
    final_score = (total_matches / total_reqs) * 100
    
    return final_score