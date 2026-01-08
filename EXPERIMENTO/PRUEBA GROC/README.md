# 🎯 Sistema de Evaluación y Puntuación de CVs con IA

Sistema automático para evaluar CVs contra descripciones de trabajo usando **Inteligencia Artificial** - **100% GRATUITO** y en español.

Ver archivo INICIO_RAPIDO.md para comenzar en 3 pasos.
Ver archivo INSTRUCCIONES_GROQ.md para configuración detallada.
**🐳 Ver archivo DOCKER.md para usar con Docker (sin instalar Python).**

## ✨ Instalación Rápida

### Opción A: Python Local

#### Paso 1: Instalar Dependencias
```powershell
py -m pip install -r requirements.txt
```

#### Paso 2: Configurar Groq (Gratis)
```powershell
py setup_groq.py
```
Sigue las instrucciones. No requiere tarjeta de crédito.

#### Paso 3: Ejecutar
```powershell
py main.py --jd examples/job_description.txt --cv examples/cv.txt
```

### Opción B: Docker 🐳 (Sin instalar Python)

#### Paso 1: Construir
```powershell
docker-compose build
```

#### Paso 2: Ejecutar
```powershell
docker-compose run --rm resume-evaluator
```

**Ver DOCKER.md para guía completa.**

¡Listo! 🎉

---

## 📚 Documentación Completa

Para la guía completa de instalación con todos los detalles, consulta estos archivos:

- **INICIO_RAPIDO.md** - Guía de inicio en 3 pasos
- **INSTRUCCIONES_GROQ.md** - Tutorial completo de configuración de Groq
- **DOCKER.md** - 🐳 Guía completa para usar con Docker
- **RESUMEN_CAMBIOS.md** - Lista detallada de características

---

## 🔍 Guía de Instalación Paso a Paso

### 📌 Requisitos Previos

1. **Python 3.8+** instalado
2. **Internet** activo
3. **5 minutos** de tu tiempo

### 🚀 Instalación Detallada

#### 1. Verificar Python

```powershell
py --version
# Debe mostrar Python 3.8 o superior
```

#### 2. Descargar el Proyecto

Si tienes Git:
```powershell
git clone <url-del-repo>
cd resume_evaluator
```

Si descargaste ZIP:
- Extrae el archivo
- Abre PowerShell en esa carpeta

#### 3. Instalar Dependencias

```powershell
py -m pip install -r requirements.txt
```

Esto instalará:
- langchain - Framework para LLMs
- langchain-groq - API de Groq (gratuita)
- pydantic - Validación de datos
- python-dotenv - Variables de entorno

⏱️ Tiempo: 1-2 minutos

#### 4. Configurar API de Groq (100% GRATIS)

**Opción A - Asistente Automático (Recomendado):**
```powershell
py setup_groq.py
```

El asistente te guiará para:
1. Crear cuenta en Groq (gratis, sin tarjeta)
2. Obtener tu API key
3. Configurar el archivo .env automáticamente

**Opción B - Manual:**

1. Ve a https://console.groq.com
2. Regístrate gratis (Google/GitHub/Email)
3. Ve a https://console.groq.com/keys
4. Crea una API key
5. Copia .env.example a .env
6. Pega tu API key en .env

⏱️ Tiempo: 3-5 minutos

#### 5. Verificar Instalación

```powershell
py main.py --jd examples/job_description.txt --cv examples/cv.txt
```

Si ves esto, ¡funciona! ✅
```
--- Evaluación automática inicial ---
{'puntuacion': XX, 'descartado': False, ...}
```

---

## 📖 Uso del Sistema

### Comando Básico

```powershell
py main.py --jd <archivo_requisitos> --cv <archivo_cv>
```

### Ejemplos de Uso

**1. Evaluar con archivos de ejemplo:**
```powershell
py main.py --jd examples/job_description.txt --cv examples/cv.txt
```

**2. Evaluar tus propios archivos:**
```powershell
py main.py --jd mi_oferta.txt --cv candidato1.txt
```

### Crear Archivos de Entrada

**Archivo de Requisitos (job_description.txt):**
```
Experiencia mínima de 3 años en Python
Formación mínima requerida: Ingeniería en Informática
Valorable conocimientos en FastAPI
Deseable experiencia con Docker
```

- Palabras clave "Valorable" o "Deseable" = **Opcional**
- Todo lo demás = **Obligatorio**

**Archivo de CV (cv.txt):**
```
EXPERIENCIA PROFESIONAL
Software Engineer - Tech Corp (2020-2024)
- Desarrollo backend con Python y Django
- Implementación de APIs RESTful

EDUCACIÓN
Ingeniería en Informática - Universidad XYZ

HABILIDADES
Python, Django, PostgreSQL, Git
```

---

## 📁 Estructura del Proyecto

```
resume_evaluator/
├── main.py              # Programa principal
├── evaluation.py        # Motor de IA
├── conversation.py      # Entrevista interactiva
├── prompts.py          # Prompts en español
├── setup_groq.py       # Asistente configuración
├── requirements.txt    # Dependencias
├── .env               # Tu API key (crear)
├── .env.example       # Plantilla
├── README.md          # Esta guía
├── INSTRUCCIONES_GROQ.md
├── INICIO_RAPIDO.md
├── RESUMEN_CAMBIOS.md
└── examples/
    ├── job_description.txt
    └── cv.txt
```

---

## 🔑 Acerca de Groq

### ¿Por qué Groq?

| Característica | Groq | OpenAI |
|---------------|------|--------|
| Precio | ✅ Gratis | ❌ Pago |
| Tarjeta crédito | ❌ No | ✅ Sí |
| Velocidad | ⚡ 10x | 🐌 1x |
| Límite diario | ✅ 14,400 | 💰 Por pago |

### Características

- 🆓 **100% Gratuito** - Sin trampas
- 🚀 **Súper Rápido** - Optimizado en hardware
- 🤖 **Llama 3.3 70B** - Modelo de última generación
- 📊 **14,400 requests/día** - Más que suficiente
- 🔒 **Seguro** - Políticas de privacidad estrictas

---

## 🔧 Solución de Problemas

### Error: "No se encontró la API key"

```powershell
# Solución rápida
py setup_groq.py
```

### Error: "Invalid API Key"

1. Verifica que empiece con gsk_
2. Sin espacios antes/después
3. Genera una nueva en console.groq.com/keys

### Error: "ModuleNotFoundError"

```powershell
py -m pip install -r requirements.txt
```

### Error: "FileNotFoundError"

- Verifica la ruta del archivo
- Usa los ejemplos primero
- Rutas relativas desde donde ejecutas

---

## ❓ Preguntas Frecuentes

**¿Es realmente gratis?**
Sí, 100%. Sin tarjeta, sin costos ocultos.

**¿Necesito instalar algo más?**
No. Solo Python y las dependencias.

**¿Funciona offline?**
No. Requiere internet para la API de Groq.

**¿Puedo usar otro LLM?**
Sí. Edita evaluation.py para cambiar el proveedor.

**¿Los CVs se guardan?**
Se envían a Groq para análisis. Lee su política de privacidad.

**¿Cuántos CVs puedo evaluar?**
14,400 por día (gratis).

---

## 💡 Mejores Prácticas

### Requisitos Claros

✅ Bueno: "3 años de experiencia en Python"
❌ Malo: "experiencia programando"

### CVs Estructurados

- Secciones claras
- Tecnologías específicas
- Años de experiencia

### Pruebas

1. Usa los ejemplos primero
2. Crea tus propios archivos
3. Ajusta prompts si necesario

---

## 🎯 Próximos Pasos

1. ✅ Instala el sistema (5 minutos)
2. ✅ Prueba con los ejemplos
3. ✅ Crea tus propios archivos
4. ✅ Personaliza según tus necesidades

---

## 📞 Recursos

- [Documentación Groq](https://console.groq.com/docs)
- [LangChain Docs](https://python.langchain.com)
- [Discord Groq](https://groq.com/discord)

---

**¡Listo para empezar!** 🚀

```powershell
py setup_groq.py
```
