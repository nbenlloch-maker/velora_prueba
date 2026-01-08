"""Lógica principal para evaluar CVs contra requisitos de trabajo usando LangChain.

Este módulo define las estructuras de datos y funciones necesarias para llamar a un
modelo de lenguaje grande (LLM) a través de LangChain. El punto de entrada principal es
la función `evaluate_cv` que acepta una lista de requisitos, un texto de CV y un
modelo de chat LangChain opcional. Retorna el resultado estructurado del LLM así como
una puntuación calculada y bandera de descarte.

Las reglas de puntuación son:

1. Cada requisito contribuye equitativamente a la puntuación final. Si hay ``n``
   requisitos y ``m`` son cumplidos, la puntuación cruda es ``m / n``.
2. Si algún requisito obligatorio está en ``unmatching_requirements`` el candidato
   es considerado descartado y la puntuación es cero.
3. Los requisitos que están ``not_found`` no causan descarte pero aún cuentan como
   no cumplidos para propósitos de puntuación.

El valor de retorno incluye la salida estructurada del LLM como un diccionario,
la puntuación calculada en porcentaje (0–100) y una bandera booleana ``discarded``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from prompts import build_evaluation_prompt


class RequirementsResult(BaseModel):
    """Modelo Pydantic usado para definir la salida estructurada retornada por el LLM."""

    matching_requirements: List[str] = Field(
        description="Texto completo de requisitos que fueron claramente satisfechos por el CV."
    )
    unmatching_requirements: List[str] = Field(
        description=(
            "Texto completo de requisitos que se mencionan en el CV pero no "
            "cumplen con el nivel requerido."
        )
    )
    not_found_requirements: List[str] = Field(
        description="Texto completo de requisitos que no se mencionan en absoluto en el CV."
    )


@dataclass
class EvaluationResult:
    """Resultado agregado incluyendo la salida del LLM, puntuación y bandera de descarte."""

    score: int
    discarded: bool
    matching_requirements: List[str]
    unmatching_requirements: List[str]
    not_found_requirements: List[str]

    def to_json(self) -> Dict:
        return {
            "puntuacion": self.score,
            "descartado": self.discarded,
            "requisitos_cumplidos": self.matching_requirements,
            "requisitos_no_cumplidos": self.unmatching_requirements,
            "requisitos_no_encontrados": self.not_found_requirements,
        }


def evaluate_cv(
    requirements: List[Tuple[str, bool]],
    cv_text: str,
    llm: Optional[ChatGroq] = None,
    model_kwargs: Optional[dict] = None,
) -> EvaluationResult:
    """Evaluar un CV contra una lista de requisitos usando un LLM.

    Parámetros
    ----------
    requirements : List[Tuple[str, bool]]
        Una lista de tuplas ``(texto_requisito, es_obligatorio)``.
    cv_text : str
        El texto completo del CV del candidato.
    llm : Optional[ChatGroq]
        Un modelo de chat LangChain instanciado. Si es ``None`` se creará un modelo
        ``ChatGroq`` predeterminado usando cualquier ``model_kwargs`` adicional.
    model_kwargs : Optional[dict]
        Argumentos clave extra pasados al constructor del modelo cuando ``llm`` es
        ``None``. Útil para configurar temperatura, nombre de modelo, etc.

    Retorna
    -------
    EvaluationResult
        Un dataclass conteniendo la puntuación, bandera de descarte y listas de requisitos.
    """

    # Construir el modelo de chat si no se proporciona
    if llm is None:
        kwargs = model_kwargs or {}
        # Por defecto usar llama-3.3-70b-versatile (gratuito y potente)
        llm = ChatGroq(
            model=kwargs.get("model", "llama-3.3-70b-versatile"),
            temperature=kwargs.get("temperature", 0),
            **{k: v for k, v in kwargs.items() if k not in ["model", "temperature"]}
        )

    # Construir el prompt
    prompt_template = build_evaluation_prompt()

    # Preparar la cadena de requisitos con prefijos obligatorio/opcional
    lineas_req = []
    for texto, es_obligatorio in requirements:
        prefijo = "OBLIGATORIO" if es_obligatorio else "OPCIONAL"
        lineas_req.append(f"{prefijo}: {texto}")
    requisitos_str = "\n".join(lineas_req)

    # Crear cadena de salida estructurada usando el método with_structured_output
    structured_llm = llm.with_structured_output(RequirementsResult)
    
    # Crear la cadena con el prompt
    chain = prompt_template | structured_llm

    # Invocar la cadena
    structured: RequirementsResult = chain.invoke({"requirements": requisitos_str, "cv": cv_text})

    # Calcular puntuación
    total_requisitos = len(requirements)
    cumplidos = len(structured.matching_requirements)
    fraccion_puntuacion = cumplidos / total_requisitos if total_requisitos else 0.0
    puntuacion_porcentaje = int(round(fraccion_puntuacion * 100))

    # Determinar descarte: si algún requisito obligatorio está en no_cumplidos
    descartado = False
    if structured.unmatching_requirements:
        # Construir un conjunto de textos de requisitos obligatorios para comparación
        textos_obligatorios = {texto for texto, obligatorio in requirements if obligatorio}
        # Si algún requisito no cumplido aparece en el conjunto obligatorio, descartar
        if any(req in textos_obligatorios for req in structured.unmatching_requirements):
            descartado = True
            puntuacion_porcentaje = 0

    return EvaluationResult(
        score=puntuacion_porcentaje,
        discarded=descartado,
        matching_requirements=structured.matching_requirements,
        unmatching_requirements=structured.unmatching_requirements,
        not_found_requirements=structured.not_found_requirements,
    )