# 🚀 Velora AI Recruiter: Mi experimento de Reclutamiento Inteligente

¡Hola! 👋 Bienvenido al repositorio de mi proyecto **Velora**.

Este proyecto nace de mi curiosidad personal. Aunque en el máster todavía no hemos profundizado en la integración compleja de LLMs (Modelos de Lenguaje) con código, quise adelantarme e investigar por mi cuenta cómo construir una herramienta que no solo "lea" texto, sino que **tome decisiones y entreviste candidatos**.

Lo que ves aquí es la **Iteración 2**, donde solucioné los problemas que encontré en mis primeras pruebas.

---

## 💡 ¿Por qué hice esto? (El Problema)

En mi primer intento, me di cuenta de que la IA funcionaba como un filtro de palabras clave : si el CV no decía explícitamente "Python", descartaba al candidato.

Pensé: *"Un reclutador humano no descarta; si tiene dudas... pregunta"*.
Así que mi objetivo fue replicar ese comportamiento humano usando código: **Si la IA no encuentra un dato, no asume que no existe, sino que le pregunta al usuario.**

---

## ⚙️ ¿Cómo funciona? (Lo que he construido)

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

## 🛠️ Tecnologías que he explorado

Como comentaba, muchas de estas cosas no las hemos dado aún en clase, así que he tenido que leer documentación y probar por mi cuenta:

* **Python:** Para unirlo todo.
* **LangChain:** Me ha servido para conectar el código con OpenAI/Deepseek de forma más fácil.
* **OpenAI (GPT-4o):** El modelo que uso para razonar.
* **Pydantic:** Para definir la estructura de los datos (esto me ha parecido súper útil para evitar errores).

---

## 📊 Ejemplo de funcionamiento

1.  **Entrada:** Subo una oferta que pide "Python y Docker".
2.  **Análisis:** Mi CV solo dice "Python".
3.  **Acción:** En lugar de ponerme un 50% de nota, el sistema detecta que falta "Docker".
4.  **Entrevista:** Me pregunta por Docker. Yo respondo: "Sí, lo uso para desplegar contenedores".
5.  **Resultado:** La IA valida mi respuesta y me recalcula la nota al 100%.

---

## 🚀 Cómo probarlo

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

---
