# interviewer.py
from models import ScreeningResult
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Usamos la misma instancia de IA local
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)

def validate_answer(requirement: str, user_answer: str) -> bool:
    """
    Sub-agente que actúa como juez técnico. 
    Decide si la respuesta del usuario es válida (SI/NO).
    """
    prompt = ChatPromptTemplate.from_template(
        "Eres un evaluador técnico estricto. \n"
        "Requisito buscado: '{req}'. \n"
        "Respuesta del candidato: '{ans}'. \n"
        "¿La respuesta demuestra que cumple el requisito? \n"
        "Responde SOLO con la palabra 'SI' o la palabra 'NO'. Sin explicaciones."
    )
    chain = prompt | llm
    res = chain.invoke({"req": requirement, "ans": user_answer})
    
    # Limpiamos la respuesta (quitamos espacios o puntos extra) y buscamos el SI
    return "SI" in res.content.strip().upper()

def start_interview(initial_result: ScreeningResult) -> float:
    """
    Bucle principal de la entrevista. Pregunta por lo que falta y recalcula la nota.
    """
    print("\n" + "="*50)
    print("🗣️  [Fase 2] ENTREVISTA INTERACTIVA")
    print("="*50)
    
    missing_items = initial_result.not_found_requirements
    
    # Si no falta nada, devolvemos la nota original
    if not missing_items:
        return initial_result.score

    print(f"🤖 IA: Hola. He visto tu CV, pero necesito aclararte {len(missing_items)} puntos.")
    
    # Iteramos por cada requisito que estaba en 'not_found'
    for req in missing_items:
        print(f"\n🔹 Requisito no encontrado: '{req}'")
        respuesta = input(f"🤖 IA: ¿Tienes experiencia en esto? \n👤 Tú: ")
        
        # Llamamos al Juez (función de arriba)
        if validate_answer(req, respuesta):
            print("   ✅ (Respuesta Validada: Suma puntos)")
            # Movemos el requisito a la lista de cumplidos
            initial_result.matching_requirements.append(req)
        else:
            print("   ❌ (Respuesta No válida)")

    # --- LÓGICA MATEMÁTICA DE RECÁLCULO ---
    # Total de requisitos originales (extraídos en fase 1)
    total_reqs = initial_result.total_requirements_count
    
    # Total cumplidos ahora = Los del CV + Los validados en entrevista
    total_matches_final = len(initial_result.matching_requirements)
    
    # Evitamos división por cero
    if total_reqs > 0:
        final_score = (total_matches_final / total_reqs) * 100
    else:
        final_score = 0

    return final_score