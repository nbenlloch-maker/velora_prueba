import sys
# Importamos las funciones REALES de los otros archivos
from screener import analyze_cv
from interviewer import start_interview
from models import ScreeningResult

# ==========================================
# DATOS DE ENTRADA (TEXTOS REALES)
# ==========================================
# En un caso real, aquí harías: with open('cv.txt') as f: cv_text = f.read()

OFERTA_TEXTO = """
Buscamos un Python Backend Developer.
Requisitos Obligatorios:
- Experiencia mínima de 3 años en Python.
- Ingeniería en Informática o similar.
Requisitos Deseables:
- Conocimientos en FastAPI.
- Experiencia con LangChain o LLMs.
- Nivel de inglés B2.
"""

CV_TEXTO = """
Hola, soy Juan.
Tengo 4 años de experiencia programando en Python creando scripts de automatización.
Soy Graduado en Ingeniería Informática por la Universidad Politécnica.
Tengo un nivel de inglés medio-alto.
He trabajado un poco con Flask y Django.
"""

# ==========================================
# FLUJO PRINCIPAL
# ==========================================

def main():
    print("\n--- 🚀 VELORA AI RECRUITER (LIVE MODE) ---")
    
    # --- FASE 1: ANÁLISIS (SCREENER) ---
    print("\n📄 Leyendo documentos...")
    try:
        # Llamada real al modelo en screener.py
        resultado_analisis = analyze_cv(OFERTA_TEXTO, CV_TEXTO)
    except Exception as e:
        print(f"❌ Error fatal conectando con la IA: {e}")
        print("Asegúrate de que GPT4All/LM Studio está corriendo en el puerto 4891.")
        return

    # Mostrar resultado preliminar
    print(f"\n📊 Resultado Fase 1 (Análisis CV):")
    print(f"   Score Inicial: {resultado_analisis.score}%")
    print(f"   Encontrados:   {resultado_analisis.matching_requirements}")
    print(f"   No encontrados (Dudas): {resultado_analisis.not_found_requirements}")
    
    # Criterio de descarte inmediato
    if resultado_analisis.discarded:
        print("\n❌ EL CANDIDATO HA SIDO DESCARTADO POR REQUISITOS OBLIGATORIOS.")
        print(f"   Faltan: {resultado_analisis.unmatching_requirements}")
        return

    # Si el score ya es 100 o no hay dudas, terminamos
    if not resultado_analisis.not_found_requirements:
        print("\n✅ El candidato cumple todo lo visible. No se requiere entrevista.")
        return

    # --- FASE 2: ENTREVISTA (INTERVIEWER) ---
    # Pasamos el objeto resultado a la entrevista para intentar mejorarlo
    input("\nPresiona ENTER para comenzar la entrevista con la IA...")
    
    score_final = start_interview(resultado_analisis)
    
    # --- RESULTADO FINAL ---
    print("\n" + "="*50)
    print("📈 INFORME FINAL TRAS ENTREVISTA")
    print("="*50)
    print(f"Score Original: {resultado_analisis.score}%")
    print(f"Score Final:    {score_final}%")
    
    if score_final > 70:
        print("✅ CONCLUSIÓN: El candidato pasa a la siguiente fase humana.")
    else:
        print("⚠️ CONCLUSIÓN: El score es bajo incluso tras la entrevista.")

if __name__ == "__main__":
    main()