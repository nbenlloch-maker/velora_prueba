
# 🚀 Velora AI Recruiter (Local DeepSeek Edition)

Este proyecto es un sistema de reclutamiento inteligente que utiliza **IA Generativa Local** (sin subir datos a la nube) para evaluar candidatos. A diferencia de los sistemas tradicionales, este modelo utiliza técnicas de **Chain of Thought (Cadena de Pensamiento)** para "razonar" internamente antes de emitir una puntuación, logrando una precisión superior.

El sistema consta de dos fases:
1.  **Screener (Fase 1):** Analiza la Oferta vs. el CV, extrae requisitos y calcula un score inicial basándose en evidencias encontradas.
2.  **Interviewer (Fase 2):** Si faltan requisitos (y no son excluyentes), entrevista al candidato interactivamente para validar sus conocimientos.

---

## 📋 Requisitos Previos

1.  **Python 3.10+** instalado.
2.  **GPT4All** (o LM Studio) instalado para correr el modelo localmente.
3.  Modelo recomendado: **DeepSeek-R1-Distill-Qwen-14B** (o cualquier modelo con buena capacidad de razonamiento).

---

## ⚙️ Configuración del "Cerebro" (GPT4All)

⚠️ **CRÍTICO:** Para que el sistema funcione y no corte la respuesta a mitad de pensamiento, debes configurar GPT4All así antes de ejecutar nada:

1.  Abre **GPT4All**.
2.  Ve a **Settings** -> **Application** (o Server).
3.  Activa la casilla **Enable API Server**.
4.  Puerto: **4891** (Si usas otro, actualízalo en `screener.py` y `interviewer.py`).
5.  **AJUSTE VITAL:** En **Generation Settings** (los ajustes del modelo cargado):
    * **Max Tokens:** Súbelo a **4096** o **8192**. (Por defecto viene muy bajo y cortará el JSON final).
    * **Context Length:** Al menos **4096**.

---

## 🛠️ Instalación y Ejecución

Sigue estos pasos en tu terminal dentro de la carpeta del proyecto:

### 1. Preparar el entorno virtual
Es recomendable usar un entorno virtual para no conflictos con otras librerías.

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno (Mac/Linux)
source venv/bin/activate

# Activar entorno (Windows)
# venv\Scripts\activate

2. Instalar dependencias
Instala las librerías necesarias para conectar Python con la IA local.

pip install langchain langchain-openai pydantic python-dotenv

3 Ejecutar

Resultados esperados

--- 🚀 VELORA AI RECRUITER (LIVE MODE) ---

📄 Leyendo documentos...
🧠 [Fase 1] Iniciando inferencia con DeepSeek 14B (Chain of Thought)...

⏳ [DEBUG] Enviando petición a DeepSeek (puede tardar por el pensamiento)...

----- 

📥 [DEBUG] Respuesta recibida. ¿Usó Chain of Thought? ✅ SÍ

🔍 [DEBUG] Buscando JSON dentro del texto recibido...

📊 Resultado Fase 1 (Análisis CV):
   Score Inicial: 60.0%  <-- (Ojo: Puede variar entre 60 y 75)
   Encontrados:   ['Experiencia mínima de 3 años en Python', 'Ingeniería en Informática']
   No encontrados (Dudas): ['Conocimientos en FastAPI', 'Experiencia con LangChain o LLMs']

----

Presiona ENTER para comenzar la entrevista con la IA...

==================================================
🎤 [Fase 2] ENTREVISTA DE COMPLETADO DE PERFIL (IA LOCAL)
==================================================
🤖 Velora (DeepSeek): Hola. He analizado tu CV y tengo 2 dudas.

🤖 Pregunta: ¿Tienes experiencia o conocimientos en: 'Conocimientos en FastAPI'?
👤 Tú: (Aquí escribes tu respuesta, ej: "Sí, lo usé en un proyecto...")

----

==================================================
📈 INFORME FINAL TRAS ENTREVISTA
==================================================
Score Original: 60.0%
Score Final:    80.0%  <-- (Si respondiste bien a una de las dos preguntas)
✅ CONCLUSIÓN: El candidato pasa a la siguiente fase humana.