# 🐳 Inicio Rápido con Docker

## ⚡ 3 Pasos - 5 Minutos

### Paso 1: Configurar API Key

```powershell
# Ejecutar el asistente
py setup_groq.py
```

Esto creará tu archivo `.env` con la API key de Groq.

### Paso 2: Construir

```powershell
docker-compose build
```

⏱️ Primera vez: 2-3 minutos

### Paso 3: Ejecutar

```powershell
docker-compose run --rm resume-evaluator
```

¡Eso es todo! 🎉

---

## 🎯 Usar con tus Archivos

### 1. Copiar archivos a `data/`

```powershell
Copy-Item C:\ruta\trabajo.txt data\
Copy-Item C:\ruta\cv.txt data\
```

### 2. Evaluar

```powershell
docker-compose run --rm resume-evaluator --jd /data/trabajo.txt --cv /data/cv.txt
```

---

## 🛠️ Helper Script (Opcional)

Para hacerlo aún más fácil:

```powershell
# Construir
.\docker-helper.ps1 build

# Probar con ejemplos
.\docker-helper.ps1 test

# Evaluar tus archivos (deben estar en data/)
.\docker-helper.ps1 eval trabajo.txt cv.txt

# Ver estado
.\docker-helper.ps1 status

# Limpiar todo
.\docker-helper.ps1 clean
```

---

## 📚 Más Información

Ver **DOCKER.md** para la guía completa con:
- Solución de problemas
- Comandos avanzados
- Optimizaciones
- FAQ

---

## ❓ Problemas Comunes

### "Cannot connect to Docker daemon"

**Solución:** Asegúrate de que Docker Desktop está corriendo.

### "No se encontró la API key"

**Solución:**
```powershell
# Verificar que existe el archivo .env
Get-Content .env

# Si no existe o está vacío:
py setup_groq.py
```

### "Image not found"

**Solución:**
```powershell
docker-compose build
```

---

**¡Listo para usar Docker!** 🚀

```powershell
docker-compose build && docker-compose run --rm resume-evaluator
```
