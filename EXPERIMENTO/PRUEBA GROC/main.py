"""Punto de entrada para la aplicación de evaluación de CV.

Este script lee una descripción de trabajo y un CV de candidato desde archivos de texto,
usa LangChain para evaluar el CV contra los requisitos, y luego realiza un diálogo de
seguimiento para recopilar información faltante. Finalmente, reporta las puntuaciones
inicial y final.

Uso::

    python main.py --jd ruta/a/descripcion_trabajo.txt --cv ruta/a/cv.txt

Configura tu API key de Groq (GRATIS) ejecutando: python setup_groq.py
O leyendo las instrucciones en: INSTRUCCIONES_GROQ.md
"""

import argparse
import os
import sys
from typing import List, Tuple
from pathlib import Path

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

from evaluation import evaluate_cv, EvaluationResult
from conversation import follow_up_interview


def parse_requirements(lines: List[str]) -> List[Tuple[str, bool]]:
    """Convierte líneas de requisitos en una lista de tuplas (texto, es_obligatorio).

    Este helper interpreta el contenido de la línea para decidir si un requisito es
    obligatorio. La heurística usada aquí marca un requisito como opcional si la
    línea contiene las palabras 'Valorable' o 'Deseable' (sin distinguir mayúsculas).
    Todo lo demás se trata como obligatorio.

    Parámetros
    ----------
    lines : List[str]
        Líneas crudas del archivo de descripción de trabajo.

    Retorna
    -------
    List[Tuple[str, bool]]
        Una lista donde cada entrada es una tupla del texto del requisito (sin
        marcadores de viñeta) y un booleano indicando si es obligatorio.
    """

    requisitos: List[Tuple[str, bool]] = []
    for line in lines:
        texto = line.strip().lstrip("-•*\u2022 ")
        if not texto:
            continue
        # Determinar opcionalidad basado en palabras clave
        minuscula = texto.lower()
        opcional = any(palabra in minuscula for palabra in ("valorable", "deseable", "opcional"))
        requisitos.append((texto, not opcional))
    return requisitos


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main(argv: List[str] | None = None) -> int:
    # Verificar que existe la API key de Groq
    if not os.getenv("GROQ_API_KEY"):
        print("=" * 70, file=sys.stderr)
        print("❌ ERROR: No se encontró la API key de Groq", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print(file=sys.stderr)
        print("Groq es COMPLETAMENTE GRATUITO - No necesitas tarjeta de crédito", file=sys.stderr)
        print(file=sys.stderr)
        print("Para configurar tu API key, tienes dos opciones:", file=sys.stderr)
        print(file=sys.stderr)
        print("OPCIÓN 1 (Recomendada): Ejecuta el asistente de configuración", file=sys.stderr)
        print("  py setup_groq.py", file=sys.stderr)
        print(file=sys.stderr)
        print("OPCIÓN 2: Configuración manual", file=sys.stderr)
        print("  1. Ve a: https://console.groq.com/keys", file=sys.stderr)
        print("  2. Crea una API key (gratis)", file=sys.stderr)
        print("  3. Copia .env.example a .env", file=sys.stderr)
        print("  4. Pega tu API key en el archivo .env", file=sys.stderr)
        print(file=sys.stderr)
        print("📖 Instrucciones detalladas: INSTRUCCIONES_GROQ.md", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        return 1
    
    parser = argparse.ArgumentParser(description="Evaluar un CV contra una descripción de trabajo.")
    parser.add_argument("--jd", required=True, help="Ruta al archivo de texto de descripción de trabajo")
    parser.add_argument("--cv", required=True, help="Ruta al archivo de texto del CV")
    args = parser.parse_args(argv)

    # Leer y parsear requisitos
    texto_jd = read_file(args.jd)
    lineas_jd = [line for line in texto_jd.splitlines() if line.strip()]
    requisitos = parse_requirements(lineas_jd)
    if not requisitos:
        print("No se encontraron requisitos en la descripción de trabajo.", file=sys.stderr)
        return 1

    texto_cv = read_file(args.cv)
    if not texto_cv.strip():
        print("El archivo CV está vacío.", file=sys.stderr)
        return 1

    # Evaluación inicial
    print("\n--- Evaluación automática inicial ---")
    resultado = evaluate_cv(requisitos, texto_cv)
    print(resultado.to_json())

    # Si el candidato no es descartado, comenzar preguntas de seguimiento
    if not resultado.discarded and resultado.not_found_requirements:
        print("\n--- Entrevista de seguimiento ---")
        resultado = follow_up_interview(resultado, requisitos)

    print("\n--- Resultado final ---")
    print(resultado.to_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())