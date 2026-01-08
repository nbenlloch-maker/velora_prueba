"""Plantillas de prompts para evaluar CVs contra requisitos de trabajo.

Este módulo define las plantillas y funciones auxiliares usadas para instruir al
modelo de lenguaje grande. Mantener los prompts en un archivo separado facilita
iterar sobre la redacción sin tocar la lógica de negocio.
"""

from langchain_core.prompts import ChatPromptTemplate


def build_evaluation_prompt() -> ChatPromptTemplate:
    """Return a chat prompt that asks the model to classify job requirements.

    The prompt expects the following input variables:

    - `requirements`: A newline separated list of job requirements.  Each line
      should be prefixed by either "MANDATORY:" or "OPTIONAL:" to indicate
      whether it is a must‑have.
    - `cv`: The full text of the candidate’s CV.

    The model is instructed to analyse the CV and categorise each requirement
    into one of three lists: `matching_requirements`, `unmatching_requirements`
    and `not_found_requirements`.  The output must be valid JSON following a
    predefined schema.  See ``evaluation.py`` for the schema definition.
    """
    return ChatPromptTemplate.from_messages([
        ("system", 
            "You are an expert human resources assistant.  "
            "Your task is to evaluate a candidate's CV against a job description.\n"
            "You are provided with a set of job requirements.  Each requirement is on its own line "
            "and begins with either 'MANDATORY:' for must‑have qualifications or 'OPTIONAL:' for nice‑to‑have qualifications.\n"
            "You are also provided with the candidate's CV.\n\n"
            "For each requirement do the following:\n"
            "- If the CV clearly satisfies the requirement, add the full requirement text to `matching_requirements`.\n"
            "- If the CV mentions the requirement but does NOT meet the stated level (e.g. fewer years of experience than required), add it to `unmatching_requirements`.\n"
            "- If the requirement is not mentioned at all in the CV, add it to `not_found_requirements`.\n\n"
            "Return your answer strictly as JSON matching the given schema.  "
            "Do not include any explanation or additional keys."
        ),
        ("human",
            "Requisitos del trabajo:\n"
            "{requirements}\n\n"
            "CV del Candidato:\n"
            "{cv}\n\n"
            "Ahora evalúa el CV contra los requisitos y produce un objeto JSON con "
            "tres listas: `matching_requirements`, `unmatching_requirements` y `not_found_requirements`."
        )
    ])