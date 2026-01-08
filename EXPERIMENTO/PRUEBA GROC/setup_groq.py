"""
Script de configuración rápida para Resume Evaluator con Groq (GRATIS)

Este script te ayuda a configurar tu API key de Groq de forma interactiva.
"""

import os
from pathlib import Path


def main():
    print("=" * 70)
    print("🚀 CONFIGURACIÓN DE GROQ PARA RESUME EVALUATOR")
    print("=" * 70)
    print()
    print("Groq es COMPLETAMENTE GRATUITO - No necesitas tarjeta de crédito")
    print()
    
    # Verificar si ya existe un .env
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  Ya existe un archivo .env")
        respuesta = input("¿Quieres sobrescribirlo? (s/n): ").strip().lower()
        if respuesta != 's':
            print("\n✅ Configuración cancelada. Tu archivo .env actual se mantiene.")
            return
    
    print("\n" + "=" * 70)
    print("PASO 1: OBTENER TU API KEY DE GROQ")
    print("=" * 70)
    print()
    print("1. Abre tu navegador y ve a: https://console.groq.com")
    print("2. Crea una cuenta (gratis, con Google/GitHub/Email)")
    print("3. Ve a: https://console.groq.com/keys")
    print("4. Haz clic en 'Create API Key'")
    print("5. Copia la API key que te dan")
    print()
    
    # Solicitar la API key
    print("=" * 70)
    print("PASO 2: PEGA TU API KEY AQUÍ")
    print("=" * 70)
    print()
    api_key = input("Pega tu API key de Groq: ").strip()
    
    if not api_key:
        print("\n❌ No ingresaste ninguna API key. Configuración cancelada.")
        return
    
    if not api_key.startswith("gsk_"):
        print("\n⚠️  ADVERTENCIA: Las API keys de Groq normalmente comienzan con 'gsk_'")
        print(f"   Tu key comienza con: '{api_key[:10]}...'")
        respuesta = input("\n¿Quieres continuar de todas formas? (s/n): ").strip().lower()
        if respuesta != 's':
            print("\n✅ Configuración cancelada.")
            return
    
    # Crear el archivo .env
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"# Configuración de Groq - Generado automáticamente\n")
            f.write(f"GROQ_API_KEY={api_key}\n")
        
        print("\n" + "=" * 70)
        print("✅ ¡CONFIGURACIÓN EXITOSA!")
        print("=" * 70)
        print()
        print("Tu archivo .env ha sido creado correctamente.")
        print()
        print("🎉 ¡Ya puedes usar el programa!")
        print()
        print("Ejecuta:")
        print("  py main.py --jd examples/job_description.txt --cv examples/cv.txt")
        print()
        
    except Exception as e:
        print(f"\n❌ Error al crear el archivo .env: {e}")
        print("\nPuedes crear el archivo manualmente:")
        print("1. Crea un archivo llamado '.env' en esta carpeta")
        print(f"2. Agrega esta línea: GROQ_API_KEY={api_key}")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
