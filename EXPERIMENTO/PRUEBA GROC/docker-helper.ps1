# Script de utilidad para Resume Evaluator con Docker
# Uso: .\docker-helper.ps1 [comando]

param(
    [Parameter(Position=0)]
    [string]$Comando = "help",
    
    [Parameter(Position=1)]
    [string]$Trabajo = "",
    
    [Parameter(Position=2)]
    [string]$CV = ""
)

function Show-Help {
    Write-Host ""
    Write-Host "🐳 Resume Evaluator - Helper Docker" -ForegroundColor Cyan
    Write-Host "====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Comandos disponibles:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  build          " -NoNewline
    Write-Host "Construir la imagen Docker" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  test           " -NoNewline
    Write-Host "Evaluar con archivos de ejemplo" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  eval           " -NoNewline
    Write-Host "Evaluar tus archivos" -ForegroundColor Gray
    Write-Host "                 Uso: .\docker-helper.ps1 eval trabajo.txt cv.txt" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  clean          " -NoNewline
    Write-Host "Limpiar contenedores e imágenes" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  status         " -NoNewline
    Write-Host "Ver estado de Docker" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  logs           " -NoNewline
    Write-Host "Ver logs del contenedor" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  shell          " -NoNewline
    Write-Host "Abrir shell en el contenedor" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  .\docker-helper.ps1 build" -ForegroundColor Green
    Write-Host "  .\docker-helper.ps1 test" -ForegroundColor Green
    Write-Host "  .\docker-helper.ps1 eval mi_trabajo.txt mi_cv.txt" -ForegroundColor Green
    Write-Host ""
}

function Build-Image {
    Write-Host "🔨 Construyendo imagen Docker..." -ForegroundColor Cyan
    docker-compose build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Imagen construida exitosamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al construir la imagen" -ForegroundColor Red
    }
}

function Test-Example {
    Write-Host "🧪 Evaluando con archivos de ejemplo..." -ForegroundColor Cyan
    docker-compose run --rm resume-evaluator
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Evaluación completada" -ForegroundColor Green
    } else {
        Write-Host "❌ Error en la evaluación" -ForegroundColor Red
    }
}

function Eval-Custom {
    if (-not $Trabajo -or -not $CV) {
        Write-Host "❌ Debes especificar archivo de trabajo y CV" -ForegroundColor Red
        Write-Host "Uso: .\docker-helper.ps1 eval trabajo.txt cv.txt" -ForegroundColor Yellow
        return
    }
    
    # Verificar que los archivos existen en data/
    $trabajoPath = Join-Path "data" $Trabajo
    $cvPath = Join-Path "data" $CV
    
    if (-not (Test-Path $trabajoPath)) {
        Write-Host "❌ No se encuentra: $trabajoPath" -ForegroundColor Red
        Write-Host "Copia el archivo a la carpeta 'data/' primero" -ForegroundColor Yellow
        return
    }
    
    if (-not (Test-Path $cvPath)) {
        Write-Host "❌ No se encuentra: $cvPath" -ForegroundColor Red
        Write-Host "Copia el archivo a la carpeta 'data/' primero" -ForegroundColor Yellow
        return
    }
    
    Write-Host "📊 Evaluando: $Trabajo vs $CV" -ForegroundColor Cyan
    docker-compose run --rm resume-evaluator --jd "/data/$Trabajo" --cv "/data/$CV"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Evaluación completada" -ForegroundColor Green
    } else {
        Write-Host "❌ Error en la evaluación" -ForegroundColor Red
    }
}

function Clean-Docker {
    Write-Host "🧹 Limpiando contenedores e imágenes..." -ForegroundColor Cyan
    
    Write-Host "Deteniendo contenedores..." -ForegroundColor Gray
    docker-compose down
    
    Write-Host "Eliminando imagen..." -ForegroundColor Gray
    docker rmi resume-evaluator:latest -f
    
    Write-Host "Limpiando contenedores parados..." -ForegroundColor Gray
    docker container prune -f
    
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

function Show-Status {
    Write-Host "📊 Estado de Docker" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Versión de Docker:" -ForegroundColor Yellow
    docker --version
    Write-Host ""
    
    Write-Host "Imágenes:" -ForegroundColor Yellow
    docker images | Select-String "resume-evaluator"
    Write-Host ""
    
    Write-Host "Contenedores:" -ForegroundColor Yellow
    docker ps -a | Select-String "resume-evaluator"
    Write-Host ""
    
    Write-Host "Uso de disco:" -ForegroundColor Yellow
    docker system df
}

function Show-Logs {
    Write-Host "📋 Logs del contenedor" -ForegroundColor Cyan
    docker-compose logs
}

function Open-Shell {
    Write-Host "🐚 Abriendo shell en el contenedor..." -ForegroundColor Cyan
    docker-compose run --rm --entrypoint /bin/bash resume-evaluator
}

# Ejecutar comando
switch ($Comando.ToLower()) {
    "build" {
        Build-Image
    }
    "test" {
        Test-Example
    }
    "eval" {
        Eval-Custom
    }
    "clean" {
        Clean-Docker
    }
    "status" {
        Show-Status
    }
    "logs" {
        Show-Logs
    }
    "shell" {
        Open-Shell
    }
    default {
        Show-Help
    }
}
