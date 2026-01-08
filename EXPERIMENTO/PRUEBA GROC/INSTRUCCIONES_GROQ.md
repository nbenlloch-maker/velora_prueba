# 🚀 Instrucciones para Usar Groq (GRATIS)

## ¿Por qué Groq?

✅ **Completamente GRATUITO** - No requiere tarjeta de crédito
✅ **Sin instalación** - Todo en la nube
✅ **Muy rápido** - Hasta 10x más rápido que OpenAI
✅ **Límite generoso** - 14,400 requests por día (suficiente para miles de CVs)
✅ **Modelos potentes** - Usa Llama 3.3 70B, uno de los mejores modelos open source

## Paso 1: Crear Cuenta en Groq

1. Ve a: https://console.groq.com
2. Haz clic en **"Sign Up"** o **"Sign In"**
3. Puedes registrarte con:
   - Google
   - GitHub
   - Email

⏱️ **Tiempo estimado: 1 minuto**

## Paso 2: Obtener tu API Key

1. Una vez dentro, ve a: https://console.groq.com/keys
2. Haz clic en **"Create API Key"**
3. Dale un nombre (ejemplo: "Resume Evaluator")
4. Haz clic en **"Submit"**
5. **COPIA la API key** (solo se muestra una vez)

⚠️ **IMPORTANTE**: Guarda tu API key en un lugar seguro. No la compartas con nadie.

## Paso 3: Configurar el Proyecto

### Opción A: Usando archivo .env (Recomendado)

1. Copia el archivo `.env.example` y renómbralo a `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Abre el archivo `.env` con un editor de texto

3. Reemplaza `tu-api-key-aqui` con tu API key real:
   ```
   GROQ_API_KEY=gsk_tu_api_key_real_aqui
   ```

4. Guarda el archivo

### Opción B: Variable de Entorno (Temporal)

En PowerShell, ejecuta:
```powershell
$env:GROQ_API_KEY = "gsk_tu_api_key_aqui"
```

⚠️ Esta opción solo funciona para la sesión actual de PowerShell.

## Paso 4: Ejecutar el Programa

```powershell
py main.py --jd examples/job_description.txt --cv examples/cv.txt
```

## 🎉 ¡Listo!

El programa ahora usará Groq de forma completamente gratuita para evaluar CVs.

## Modelos Disponibles en Groq

El proyecto usa `llama-3.3-70b-versatile` por defecto, pero puedes cambiar el modelo editando `evaluation.py` o pasando `model_kwargs`.

Otros modelos disponibles:
- `llama-3.3-70b-versatile` (Recomendado - muy inteligente)
- `llama-3.1-70b-versatile` (Alternativa estable)
- `llama-3.1-8b-instant` (Más rápido, menos preciso)
- `mixtral-8x7b-32768` (Bueno para textos largos)

## Solución de Problemas

### Error: "Invalid API Key"
- Verifica que copiaste la API key completa
- Asegúrate de que no hay espacios antes o después
- Revisa que el archivo `.env` esté en la carpeta correcta

### Error: "Rate limit exceeded"
- Espera unos minutos e intenta de nuevo
- El límite gratuito es muy generoso (14,400 requests/día)

### ¿Necesitas ayuda?
- Documentación oficial: https://console.groq.com/docs
- Discord de Groq: https://groq.com/discord

---

**💡 Consejo**: Groq es mucho más rápido que OpenAI y es gratis. ¡Disfrútalo!
