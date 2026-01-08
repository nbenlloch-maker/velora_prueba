# 🐳 Guía de Uso con Docker

## 🎯 Ventajas de Usar Docker

- ✅ **No instalar Python** - Todo está en el contenedor
- ✅ **Sin conflictos** - Entorno aislado
- ✅ **Portátil** - Funciona igual en Windows, Mac, Linux
- ✅ **Reproducible** - Mismo entorno siempre
- ✅ **Limpio** - No ensucia tu sistema

---

## 📋 Requisitos Previos

1. **Docker Desktop** instalado
   - Windows: [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Verificar: `docker --version`

2. **API Key de Groq** configurada
   - Si no la tienes, ejecuta primero: `py setup_groq.py`
   - O crea el archivo `.env` manualmente

---

## 🚀 Método 1: Docker Compose (Recomendado)

### Construcción Inicial

```powershell
# Construir la imagen
docker-compose build
```

⏱️ Primera vez: 2-3 minutos  
⏱️ Siguientes: segundos (usa caché)

### Uso Básico

**1. Evaluar con archivos de ejemplo:**
```powershell
docker-compose run --rm resume-evaluator
```

**2. Evaluar tus propios archivos:**
```powershell
# Primero, copia tus archivos a la carpeta 'data'
# Luego ejecuta:
docker-compose run --rm resume-evaluator --jd /data/mi_trabajo.txt --cv /data/mi_cv.txt
```

**3. Modo interactivo:**
```powershell
docker-compose run --rm resume-evaluator --jd examples/job_description.txt --cv examples/cv.txt
```

### Comandos Útiles

```powershell
# Ver logs
docker-compose logs

# Limpiar todo
docker-compose down

# Reconstruir desde cero
docker-compose build --no-cache
```

---

## 🔨 Método 2: Docker CLI

### Construcción

```powershell
docker build -t resume-evaluator .
```

### Ejecución

**Con archivo .env:**
```powershell
docker run --rm `
  --env-file .env `
  -v ${PWD}/examples:/app/examples:ro `
  -v ${PWD}/data:/data:rw `
  -it resume-evaluator `
  --jd examples/job_description.txt --cv examples/cv.txt
```

**Con API key directa:**
```powershell
docker run --rm `
  -e GROQ_API_KEY="tu-api-key-aqui" `
  -v ${PWD}/examples:/app/examples:ro `
  -v ${PWD}/data:/data:rw `
  -it resume-evaluator `
  --jd examples/job_description.txt --cv examples/cv.txt
```

---

## 📁 Organización de Archivos

```
resume_evaluator/
├── Dockerfile              # Definición de la imagen
├── docker-compose.yml      # Configuración orquestada
├── .dockerignore          # Archivos excluidos
├── .env                   # Tu API key (NO versionar)
├── examples/              # Archivos de ejemplo (montado como volumen)
│   ├── job_description.txt
│   └── cv.txt
└── data/                  # TUS archivos (crear esta carpeta)
    ├── mi_trabajo.txt
    └── mi_cv.txt
```

### Crear Carpeta data

```powershell
# Si no existe, créala
New-Item -ItemType Directory -Force -Path data
```

---

## 🎓 Ejemplos de Uso

### Ejemplo 1: Evaluación Rápida

```powershell
# Con archivos de ejemplo
docker-compose run --rm resume-evaluator
```

Salida:
```
--- Evaluación automática inicial ---
{'puntuacion': 85, 'descartado': False, ...}
```

### Ejemplo 2: Tus Archivos

```powershell
# 1. Copia tus archivos
Copy-Item C:\Descargas\trabajo.txt data\trabajo.txt
Copy-Item C:\Descargas\cv.txt data\cv.txt

# 2. Evalúa
docker-compose run --rm resume-evaluator --jd /data/trabajo.txt --cv /data/cv.txt
```

### Ejemplo 3: Múltiples Evaluaciones

```powershell
# Crear alias para facilitar
function Evaluar-CV {
    param($trabajo, $cv)
    docker-compose run --rm resume-evaluator --jd "/data/$trabajo" --cv "/data/$cv"
}

# Usar
Evaluar-CV "trabajo1.txt" "candidato1.txt"
Evaluar-CV "trabajo1.txt" "candidato2.txt"
Evaluar-CV "trabajo2.txt" "candidato1.txt"
```

---

## 🔧 Solución de Problemas Docker

### Error: "Cannot connect to Docker daemon"

**Solución:**
```powershell
# Inicia Docker Desktop y espera que arranque completamente
# Verifica:
docker ps
```

### Error: "API key not found"

**Solución:**
```powershell
# Verifica que el archivo .env existe
Get-Content .env

# Debe contener:
# GROQ_API_KEY=gsk_...
```

### Error: "No such file or directory"

**Solución:**
```powershell
# Asegúrate de ejecutar desde la carpeta del proyecto
cd C:\Users\sescorue\Downloads\resume_evaluator\resume_evaluator

# Verifica que los archivos existan
ls examples/
ls data/
```

### Reconstruir Imagen Limpia

```powershell
# Eliminar imagen actual
docker rmi resume-evaluator

# Construir sin caché
docker-compose build --no-cache
```

---

## 🎯 Flujo de Trabajo Recomendado

### Setup Inicial (Una sola vez)

```powershell
# 1. Asegurar que tienes API key
py setup_groq.py

# 2. Crear carpeta data
New-Item -ItemType Directory -Force -Path data

# 3. Construir imagen
docker-compose build
```

### Uso Diario

```powershell
# 1. Copia archivos a 'data/'
Copy-Item ruta\trabajo.txt data\
Copy-Item ruta\cv.txt data\

# 2. Evalúa
docker-compose run --rm resume-evaluator --jd /data/trabajo.txt --cv /data/cv.txt

# 3. Revisa resultados
```

---

## 🔄 Comparación: Docker vs Local

| Aspecto | Docker | Local (Python) |
|---------|--------|----------------|
| Setup inicial | ⏱️ 5 min | ⏱️ 5 min |
| Instalación Python | ❌ No necesario | ✅ Requerido |
| Portabilidad | ✅ Funciona en todo | ⚠️ Depende del SO |
| Limpieza | ✅ Aislado | ⚠️ Instala paquetes |
| Velocidad | ⚡ Similar | ⚡ Similar |
| Uso de disco | 📦 ~500MB | 📦 ~100MB |

**Recomendación:**
- 🐳 **Usa Docker si:** No quieres instalar Python, necesitas portabilidad, trabajas en equipo
- 🐍 **Usa Python si:** Ya tienes Python, prefieres control directo, desarrollo activo

---

## 📊 Comandos Docker Útiles

```powershell
# Ver imágenes
docker images

# Ver contenedores corriendo
docker ps

# Ver todos los contenedores
docker ps -a

# Limpiar contenedores parados
docker container prune

# Limpiar imágenes sin usar
docker image prune

# Limpiar TODO (cuidado)
docker system prune -a

# Ver uso de disco
docker system df
```

---

## 🚀 Optimizaciones Avanzadas

### Crear Alias Permanente

```powershell
# Agregar a tu perfil de PowerShell
notepad $PROFILE

# Agregar estas líneas:
function Evaluar-CV {
    param($trabajo, $cv)
    docker-compose run --rm resume-evaluator --jd "/data/$trabajo" --cv "/data/$cv"
}

# Recargar perfil
. $PROFILE

# Ahora puedes usar:
Evaluar-CV "trabajo.txt" "cv.txt"
```

### Ejecutar en Background

```powershell
# Si necesitas procesar múltiples CVs
docker-compose up -d

# Ver logs
docker-compose logs -f
```

---

## ❓ FAQ Docker

**¿Necesito reiniciar Docker cada vez?**
No. Docker Desktop se mantiene corriendo en segundo plano.

**¿Cuánto espacio ocupa?**
~500MB la imagen + dependencias de Docker.

**¿Puedo usar mi API key sin archivo .env?**
Sí, pásala directamente: `-e GROQ_API_KEY="tu-key"`

**¿Los archivos se quedan en el contenedor?**
No. Los volúmenes mapean a tu disco local (`data/`).

**¿Funciona sin internet?**
No. Necesita internet para conectarse a Groq API.

**¿Es más lento que Python local?**
No. Performance es prácticamente idéntica.

---

## 🎓 Recursos Docker

- [Documentación Docker](https://docs.docker.com)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Docker Compose Docs](https://docs.docker.com/compose)

---

**¡Listo para usar Docker!** 🐳

```powershell
docker-compose build
docker-compose run --rm resume-evaluator
```
