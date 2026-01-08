"""Conversación basada en terminal para recopilar información sobre requisitos faltantes.

Este módulo proporciona funciones para preguntar al candidato sobre requisitos que
no se encontraron en su CV. Actualiza el resultado de evaluación en consecuencia y
recalcula la puntuación final.

Nota que en una aplicación real podrías reemplazar estas funciones con una interfaz
de chat GUI o integrarlas en una aplicación web. Mantener la lógica separada aquí
facilita intercambiar el mecanismo de entrada/salida.
"""

from typing import List, Tuple

from evaluation import EvaluationResult


def follow_up_interview(
    evaluation: EvaluationResult, requirements: List[Tuple[str, bool]]
) -> EvaluationResult:
    """Interactively ask the candidate about missing requirements and update the result.

    Parameters
    ----------
    evaluation : EvaluationResult
        The initial evaluation result from the LLM.
    requirements : List[Tuple[str, bool]]
        The original list of requirements used during evaluation.  The order and
        text must match those provided to the LLM so that matches and mandatory
        checks work correctly.

    Returns
    -------
    EvaluationResult
        A new evaluation result reflecting the candidate’s answers and the
        puntuación/bandera de descarte actualizada.
    """

    # Copiar las listas iniciales
    cumplidos = list(evaluation.matching_requirements)
    no_cumplidos = list(evaluation.unmatching_requirements)
    no_encontrados = list(evaluation.not_found_requirements)

    # Preguntar al usuario sobre cada requisito no encontrado
    for req in list(no_encontrados):  # iterar sobre una copia ya que modificamos la lista
        print(f"\nEl requisito '{req}' no aparecía en tu CV.")
        while True:
            respuesta = input(
                f"¿Cumples con este requisito? Responde 's' para sí o 'n' para no: "
            ).strip().lower()
            if respuesta in ("s", "n"):
                break
            print("Respuesta no válida. Por favor, introduce 's' o 'n'.")
        if respuesta == "s":
            # Mover este requisito de no_encontrados a cumplidos
            no_encontrados.remove(req)
            cumplidos.append(req)
        else:
            # Dejarlo en no_encontrados; sin cambios
            pass

    # Recalcular la puntuación y bandera de descarte
    total = len(requirements)
    coincidencias = len(cumplidos)
    puntuacion_porcentaje = int(round((coincidencias / total) * 100)) if total else 0

    # Verificar si algún requisito obligatorio permanece no cumplido
    descartado = False
    if no_cumplidos:
        textos_obligatorios = {texto for texto, obligatorio in requirements if obligatorio}
        if any(req in textos_obligatorios for req in no_cumplidos):
            descartado = True
            puntuacion_porcentaje = 0
    # También verificar si algún requisito obligatorio permanece faltante después del seguimiento
    # Un requisito obligatorio faltante es uno que aparece en no_encontrados y está
    # marcado como obligatorio en la lista original. Si es así, descartar.
    textos_obligatorios = {texto for texto, obligatorio in requirements if obligatorio}
    if any(req in textos_obligatorios for req in no_encontrados):
        descartado = True
        puntuacion_porcentaje = 0

    # Retornar nuevo EvaluationResult
    return EvaluationResult(
        score=puntuacion_porcentaje,
        discarded=descartado,
        matching_requirements=cumplidos,
        unmatching_requirements=no_cumplidos,
        not_found_requirements=no_encontrados,
    )