# Script para iniciar el Notification Service en Windows

Write-Host "🚀 Iniciando Notification Service..." -ForegroundColor Green

# Verificar que RabbitMQ esté corriendo
Write-Host "📡 Verificando conexión a RabbitMQ..." -ForegroundColor Yellow

# Crear directorio de datos si no existe
if (!(Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host "✅ Directorio 'data' creado" -ForegroundColor Green
}

# Iniciar el servicio
Write-Host "✅ Iniciando servidor en puerto 3006..." -ForegroundColor Green
uvicorn src.main:app --host 0.0.0.0 --port 3006 --reload
