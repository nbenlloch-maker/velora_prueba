from screener import analyze_cv
from interviewer import start_interview
from dotenv import load_dotenv
import os

# Cargar claves
load_dotenv()

def main():
    print("--- 🚀 VELORA AI RECRUITER (FULL SYSTEM) ---")

    # DATOS DE EJEMPLO DEL PDF [cite: 22-33]
    oferta = """
    Requisitos:
    - Experiencia mínima de 3 años en Python (Obligatorio)
    - Formación mínima requerida: Ingeniería/Grado en informática o Master en IA (Obligatorio)
    - Valorable conocimientos en FastAPI y LangChain (Opcional)
    """

    cv_candidato = """
    Experiencia:
    Desarrollador de IA Generativa - EMPRESA A (Abril 2023 - Actualidad)
    Encargado de desarrollar sistemas de IA generativa en Python.
    
    Formación:
    Ingeniería Informática (2017 - 2021)
    """

    # --- FASE 1: SCREENING ---
    try:
        eval_1 = analyze_cv(oferta, cv_candidato)
        
        print("\n📊 RESULTADO FASE 1:")
        print(f"   Score Inicial: {eval_1.score}%")
        print(f"   Requisitos encontrados: {eval_1.matching_requirements}")
        print(f"   No encontrados (a preguntar): {eval_1.not_found_requirements}")
        print(f"   Total Requisitos detectados: {eval_1.total_requirements_count}")

        if eval_1.discarded:
            print("\n❌ EL CANDIDATO HA SIDO DESCARTADO (Falta requisito obligatorio).")
            return

    except Exception as e:
        print(f"Error en Fase 1: {e}")
        return

    # --- FASE 2: ENTREVISTA ---
    # Solo pasamos a fase 2 si hay cosas que preguntar
    if eval_1.not_found_requirements:
        nota_final = start_interview(eval_1)
        
        print("\n" + "="*50)
        print(f"🎯 PUNTUACIÓN FINAL RECALCULADA: {nota_final}%")
        print("="*50)
    else:
        print("Finalizado sin entrevista.")

if __name__ == "__main__":
    main()