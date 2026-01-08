# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY . .

# Crear directorio para archivos de entrada del usuario
RUN mkdir -p /data

# Variables de entorno (se sobrescriben con docker run -e o docker-compose)
ENV GROQ_API_KEY=""

# Punto de entrada por defecto
ENTRYPOINT ["python", "main.py"]

# Argumentos por defecto (se pueden sobrescribir)
CMD ["--help"]
