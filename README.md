

¡Hola! 👋 Bienvenido al repositorio de mi proyecto **Velora**.

Este proyecto nace de mi curiosidad personal. Aunque en el máster todavía no hemos profundizado en la integración compleja de LLMs (Modelos de Lenguaje) con código y la IA generativa, por qué no adelantarme e investigar por mi cuenta cómo construir una herramienta que no solo "lea" texto, sino que **tome decisiones y entreviste candidatos**.

La verdad es que me lo he pasado genial haciéndolo. La idea que tenía al entrar al máster era justo esta: poder vincular mi formación base de Relaciones Laborales y Recursos Humanos con la IA, así que ha sido la excusa perfecta y me encantaría poder seguir aprendiendo de estos modelos y tecnologías.

---

## 🧠 Evolución del Proyecto: La elección del Modelo

Para lograr que esto funcionara, pasé por **tres fases de experimentación con distintos modelos**, enfrentándome a barreras técnicas y económicas:

1.  **Intento 1: OpenAI (GPT-4)** 
    * Fue mi primera opción por ser el estándar.
    * **Problema:** Me encontré con barreras de entrada (requerimiento de tarjetas de crédito y *tiers* de pago para la API) que dificultaban el desarrollo fluido para un proyecto de estudiantes. No me dejaba continuar sin configurar la facturación.

2.  **Intento 2: DeepSeek** 
    * Probé este modelo buscando una alternativa potente y más accesible.
    * **Resultado:** Aunque prometedor, la integración no fue tan inmediata para el flujo de conversación que yo necesitaba en este prototipo específico.

3.  **Intento 3: Groq** 
    * Finalmente, opté por **Groq**.
    * **Resultado:** Es la que me ha funcionado a la perfección. Ofrece una velocidad de inferencia increíble (necesaria para que la entrevista no se sienta lenta) y su integración ha sido la más estable y sin problemas de bloqueos por pago durante las pruebas.
    
De todas formas, adjunto los 3 modelos para que se les eche un ojo yse vea el procedimiento a seguir por ver si iba bien encaminado o no.
---

## ⚙️ ¿Cómo funciona? (Arquitectura)

He dividido el código en piezas pequeñas para mantener la modularidad. Así fluye la lógica:

### 1. El Cerebro (`screener.py` y `models.py`)
Investigando, descubrí que pedirle texto libre a un LLM es un caos para programar posteriormente.
* **Lo que aprendí:** Usé una librería llamada `Pydantic` para obligar a la IA a devolverme los datos ordenados (en formato JSON estricto).
* **La lógica:** Ahora la IA clasifica los requisitos en tres tipos:
    * ✅ **Matching:** Lo tienes.
    * ❌ **Unmatching:** Dices explícitamente que no lo tienes.
    * ❓ **Not Found:** No aparece en el CV (aquí está la clave del proyecto).

### 2. El Entrevistador (`interviewer.py`)
Si la IA detecta requisitos "Not Found", no te baja la nota inmediatamente.
* Se inicia un chat automático.
* La IA pregunta: *"Oye, no vi FastAPI en tu CV, ¿sabes usarlo?"*.
* **El Juez:** Lo más interesante es que no busco un "Sí" o un "No" simple. He programado una segunda llamada a la IA que lee tu respuesta y evalúa semánticamente si realmente sabes del tema.

---

## 🛠 Tecnologías que he explorado

Como comentaba, muchas de estas cosas no las hemos dado aún en clase, así que he tenido que leer documentación y probar por mi cuenta:

* **Python:** El lenguaje base.
* **LangChain:** Para orquestar la conexión entre mi código y los modelos de IA.
* **Groq API:** El motor de inteligencia elegido por su velocidad y fiabilidad.
* **Pydantic:** Para definir la estructura de datos y validación (crucial para evitar errores de parseo).

---

## 📝 Ejemplo de funcionamiento

1.  **Entrada:** Subo una oferta que pide "Python y Docker".
2.  **Análisis:** Mi CV solo dice "Python".
3.  **Acción:** En lugar de ponerme un 50% de nota, el sistema detecta que falta "Docker" (Not Found).
4.  **Entrevista:** Me pregunta por Docker. Yo respondo: "Sí, lo uso para desplegar contenedores".
5.  **Resultado:** La IA valida mi respuesta y me recalcula la nota al 100%.

---


<img width="464" height="198" alt="Captura Terminal Velora" src="https://github.com/user-attachments/assets/31788f33-9b94-4af3-b61e-2e6f2d9f6d18" />

---

## 📋 Ejercicio propuesto (Base del proyecto)

Este proyecto soluciona el siguiente enunciado técnico:

**Especificaciones:**
El sistema debe recibir los requisitos de la oferta (mínimos/obligatorios o deseables/opcionales) y el CV del candidato. Debe identificar qué requisitos se cumplen.

* **Puntuación:** Todos los requisitos puntúan igual sobre 100%.
* **Regla de Oro:** Si falla un requisito obligatorio, la puntuación es 0% (Descartado).
* **Dudas:** Si un requisito no aparece, cuenta como no cumplido pero no descarta.

**Ejemplo de Oferta:**
* Experiencia mínima de 3 años en Python (Obligatorio)
* Valorable certificación de DevOps en AWS (Opcional)

**Flujo:**
1.  **Fase 1:** Devolver puntuación inicial, listas de requisitos cumplidos/no cumplidos/no encontrados y flag de descartado.
2.  **Fase 2:** Si no está descartado, iniciar conversación preguntando por los requisitos "no encontrados".
3.  **Recálculo:** Si el candidato responde positivamente (ej: confirma experiencia en FastAPI), recalcular la nota final (ej: subir de 50% a 75%).

```