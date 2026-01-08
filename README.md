#  Velora: Experimento de Reclutamiento Inteligente

¡Hola! 👋 Bienvenido al repositorio de mi proyecto **Velora**.

Este proyecto nace de mi curiosidad personal. Aunque en el máster todavía no hemos profundizado en la integración compleja de LLMs (Modelos de Lenguaje) con código, quise adelantarme e investigar por mi cuenta cómo construir una herramienta que no solo "lea" texto, sino que **tome decisiones y entreviste candidatos**.

---

##  ¿Por qué hice esto? (El Problema)

En mi primer intento, me di cuenta de que la IA funcionaba como un filtro de palabras clave : si el CV no decía explícitamente "Python", descartaba al candidato.

Pensé: *"Un reclutador humano no descarta; si tiene dudas... pregunta"*.
Así que mi objetivo fue replicar ese comportamiento humano usando código: **Si la IA no encuentra un dato, no asume que no existe, sino que le pregunta al usuario.**

---

##  ¿Cómo funciona? (Lo que he construido)

He dividido el código en piezas pequeñas para no liarme (modularidad). Así es como fluye la lógica:

### 1. El Cerebro (`screener.py` y `models.py`)
Investigando, descubrí que pedirle texto libre a ChatGPT es un caos para programar.
* **Lo que aprendí:** Usé una librería llamada `Pydantic` para obligar a la IA a devolverme los datos ordenados (en formato JSON estricto).
* **La lógica:** Ahora la IA clasifica los requisitos en tres tipos:
    * ✅ **Matching:** Lo tienes.
    * ❌ **Unmatching:** Dices explícitamente que no lo tienes.
    * ❓ **Not Found:** No aparece en el CV (aquí está la clave).

### 2. El Entrevistador (`interviewer.py`)
Si la IA detecta requisitos "Not Found", no te baja la nota.
* Se inicia un chat automático.
* La IA te pregunta: *"Oye, no vi FastAPI en tu CV, ¿sabes usarlo?"*.
* **El Juez:** Lo más interesante es que no busco un "Sí" o un "No" simple. He programado una segunda llamada a la IA que lee tu respuesta y evalúa si realmente sabes del tema o no.

---

##  Tecnologías que he explorado

Como comentaba, muchas de estas cosas no las hemos dado aún en clase, así que he tenido que leer documentación y probar por mi cuenta:

* **Python:** Para unirlo todo.
* **LangChain:** Me ha servido para conectar el código con OpenAI/Deepseek de forma más fácil.
* **OpenAI (GPT-4o):** El modelo que uso para razonar.
* **Pydantic:** Para definir la estructura de los datos (esto me ha parecido súper útil para evitar errores).

---

##  Ejemplo de funcionamiento

1.  **Entrada:** Subo una oferta que pide "Python y Docker".
2.  **Análisis:** Mi CV solo dice "Python".
3.  **Acción:** En lugar de ponerme un 50% de nota, el sistema detecta que falta "Docker".
4.  **Entrevista:** Me pregunta por Docker. Yo respondo: "Sí, lo uso para desplegar contenedores".
5.  **Resultado:** La IA valida mi respuesta y me recalcula la nota al 100%.

---

##  Cómo probarlo

He creado un archivo `main.py` para que sea fácil de ejecutar:

1.  Instalar lo necesario:
    ```bash
    pip install -r requirements.txt
    ```
2.  Poner la clave de OpenAI en un archivo `.env`.
3.  Ejecutar:
    ```bash
    python main.py
    ```
<img width="464" height="198" alt="Captura Terminal  Velora" src="https://github.com/user-attachments/assets/31788f33-9b94-4af3-b61e-2e6f2d9f6d18" />

---
## Ejercicio propuesto:

Especificaciones
Este sistema recibirá el sistema recibirá los requisitos de la oferta (cada requisito puede ser
mínimos/obligatorios o deseables/opcionales) y el CV completo del candidato (ambos en texto,
puede ser leyendo un .txt o como se prefiera).
El sistema debe identificar cuáles de los requisitos de la oferta cumple el CV aportado. Todos
los requisitos puntúan lo mismo sobre un total de 100% (por simplificar la prueba), es decir si se
piden 5 requisitos y se cumplen 4, se obtiene un 80%. Pero si uno de los requisitos obligatorios
(indicado en la oferta), no se cumple, la puntuación debe ser 0%, ya que el candidato está
descartado. Si un requisito de la oferta no aparece en el CV, cuenta como no cumplido pero no
descarta nunca.
Ejemplo de una oferta con requisito de experiencia obligatorio y certificación en AWS opcional:

- Experiencia mínima de 3 años en Python
- Valorable certificación de DevOps en AWS
Este primer paso del sistema, deberá devolver la puntuación del CV sobre la oferta, un listado
de los requisito que ha complicado y de los que no ha cumplido, un flag indicando si ha sido descartado por un requisito obligatorio o no y una lista de “requisitos” de la oferta no encontrados en el CV.
El segundo paso del sistema es tomar esta salida, y si el candidato no ha sido descartado debe
establecer una conversación con el candidato para preguntar sobre los requisitos no
encontrados en la oferta. El sistema debe recopilar la información faltante y cuando la tenga,
volver a evaluar al candidato con el fin de actualizar la puntuación con las respuesta obtenidas.
Ejemplo completo:
Requisitos de la oferta:
- Experiencia mínima de 3 años en Python
- Formación mínima requerida: Ingeniería/Grado en informática o Master en IA
- Valorable conocimientos en FastAPI y LangChain
CV (versión resumida para el ejemplo):
Experiencia:
Desarrollador de IA Generativa - EMPRESA A (Abril 2023 - Actualidad)
Encargado de desarrollar sistemas de IA generativa en Python, diseñando prompts eficientes y
sistemas escalables
Data Science / LLM - EMPRESA B (Enero 2022 - Abril 2023)
Analista de datos para el entrenamiento de modelos LLM. Entre mis funciones reentrenamiento
y validación con prompt diseñados para validar su correcto funcionamiento

Con esta información el sistema debe iniciar una conversación (puede ser directamente en la
terminal, o con alguna interfaz UI sencilla generada con el software que desee).
En esa conversación un asistente/agente debe saludar al candidato y preguntar por los
requisitos no encontrados. En este ejemplo debe preguntar si tiene experiencia en FastAPI y
después si tiene experiencia en LangChain.
Supongamos que el candidato contesta que sí tiene experiencia en FastAPI pero no en
LangChain. El sistema debe recalcular la puntuación con esta nueva información y responder
que la puntuación final es de 75% (los 2 requisitos detectados en el CV + 1 en la conversación,
son 3 sobre 4)
