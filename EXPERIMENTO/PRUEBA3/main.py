import sys
import os
from screener import analyze_cv
from interviewer import start_interview

# Textos de ejemplo (Simulando lectura de archivos)
JD_TEXT = """
Buscamos un Python Developer.
Requisitos:
- Experiencia mínima de 3 años en Python (OBLIGATORIO)
- Ingeniería informática o similar (OBLIGATORIO)
- Conocimientos en FastAPI (OPCIONAL)
- Conocimientos en LangChain (OPCIONAL)
"""

CV_TEXT = """
Hola, soy Juan. Soy Ingeniero Informático.
Llevo 4 años programando en Python haciendo scripts de automatización.
No menciono nada más.
"""

def main():
    # Comprobación de API KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: Necesitas configurar la variable de entorno OPENAI_API_KEY")
        return

    print("🚀 SISTEMA DE SELECCIÓN IA v2.0 (OpenAI Enhanced)")
    print("-" * 50)
    
    # FASE 1
    print("\n📄 Analizando CV vs Oferta...")
    try:
        result_phase_1 = analyze_cv(JD_TEXT, CV_TEXT)
    except Exception as e:
        print(f"Error en el análisis: {e}")
        return

    print("\n📊 RESULTADO FASE 1:")
    print(result_phase_1.model_dump_json(indent=2))
    
    if result_phase_1.discarded:
        print("\n❌ EL CANDIDATO HA SIDO DESCARTADO POR REQUISITOS OBLIGATORIOS.")
        sys.exit(0)

    # FASE 2
    if result_phase_1.not_found_requirements:
        result_final = start_interview(result_phase_1)
        
        print("\n" + "="*50)
        print("🏆 INFORME FINAL")
        print("="*50)
        print(f"Score Inicial: {result_phase_1.score}%")
        print(f"Score Final:   {result_final.score}%")
        print(result_final.model_dump_json(indent=2))
    else:
        print("\n✅ El CV está completo. No se requiere entrevista.")

if __name__ == "__main__":
    main()