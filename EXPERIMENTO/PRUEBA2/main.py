import os
import sys
from screener import analyze_cv
from interviewer import start_interview

# Intentamos cargar variables de entorno (útil si usas OpenAI, opcional en Local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def print_header(text: str):
    """Utilidad para imprimir cabeceras visuales y limpias."""
    print("\n" + "═" * 70)
    print(f" {text}")
    print("═" * 70)

def print_kpi(label: str, value: str, icon: str = "•"):
    """Imprime una línea de dato clave (KPI) alineada."""
    print(f" {icon} {label:<25}: {value}")

def main():
    print_header("🚀 VELORA AI RECRUITER - SISTEMA DE RECUPERACIÓN DE TALENTO")
    print(" ℹ️  Objetivo: Detectar candidatos válidos ocultos por CVs incompletos.")

    # --- DATOS DEL CASO DE USO (Según Especificación Oficial) ---
    # Estos datos están diseñados para probar la lógica:
    # 4 Requisitos Totales -> Cumple 2 (50%) -> Entrevista -> Cumple 1 más -> Final (75%)
    
    oferta = """
    Requisitos:
    - Experiencia mínima de 3 años en Python (Obligatorio)
    - Formación mínima requerida: Ingeniería/Grado en informática o Master en IA (Obligatorio)
    - Valorable conocimientos en FastAPI y LangChain
    """

    cv_candidato = """
    Experiencia:
    Desarrollador de IA Generativa - EMPRESA A (Abril 2023 - Actualidad)
    Encargado de desarrollar sistemas de IA generativa en Python, diseñando prompts.
    
    Formación:
    Ingeniería Informática (2017 - 2021)
    """

    # --- FASE 1: ANÁLISIS ATS (SCREENING) ---
    print("\n⏳ [Sistema] Analizando perfil del candidato...")
    
    try:
        # Llamada al cerebro (screener.py)
        eval_1 = analyze_cv(oferta, cv_candidato)
        
        print_header("📊 REPORTE DE FASE 1 (ANÁLISIS ESTÁTICO)")
        
        estado = "❌ DESCARTADO" if eval_1.discarded else "✅ APTO PARA REVISIÓN"
        
        print_kpi("Score Inicial", f"{eval_1.score:.1f}%", "📉")
        print_kpi("Estado Automático", estado)
        print_kpi("Requisitos Totales", str(eval_1.total_requirements_count))
        print_kpi("Cumplidos (CV)", f"{len(eval_1.matching_requirements)}")
        
        if eval_1.not_found_requirements:
            print(f"\n ⚠️  ALERT: Se detectaron {len(eval_1.not_found_requirements)} lagunas de información:")
            for req in eval_1.not_found_requirements:
                print(f"    - {req}")
        
        if eval_1.discarded:
            print("\n❌ EL CANDIDATO NO CUMPLE REQUISITOS MÍNIMOS. FIN DEL PROCESO.")
            return

    except Exception as e:
        print(f"\n❌ Error crítico en el motor de IA: {e}")
        return

    # --- FASE 2: AGENTE DE ENTREVISTA (INTERVIEWER) ---
    # Solo se activa si hay dudas (requisitos 'not_found')
    if eval_1.not_found_requirements:
        print_header("🎤 FASE 2: INTERVENCIÓN DEL AGENTE (VELORA)")
        print(" 🤖 El agente iniciará una validación técnica para recuperar información.\n")
        
        # Llamada al entrevistador (interviewer.py)
        nota_final = start_interview(eval_1)
        
        # --- RESUMEN FINAL PARA DIRECCIÓN ---
        print_header("📈 INFORME DE IMPACTO Y ROI")
        
        print_kpi("Score Original (ATS)", f"{eval_1.score:.1f}%", "🔴")
        print_kpi("Score Final (Velora)", f"{nota_final:.1f}%", "🟢")
        
        mejora = nota_final - eval_1.score
        if mejora > 0:
            print(f"\n ✅ ÉXITO: El sistema ha recuperado un +{mejora:.1f}% de valor en el candidato.")
            print("    Recomendación: 📞 CONTACTAR PARA ENTREVISTA HUMANA.")
        else:
            print("\n ⏹️  RESULTADO: El candidato no poseía los conocimientos ocultos.")
            
    else:
        print("\n✅ El perfil ya estaba completo al 100%. No fue necesaria intervención.")

if __name__ == "__main__":
    main()