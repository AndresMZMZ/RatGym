#!/bin/bash
# Script para iniciar el Notification Service

echo "🚀 Iniciando Notification Service..."

# Verificar que RabbitMQ esté corriendo
echo "📡 Verificando conexión a RabbitMQ..."

# Crear directorio de datos si no existe
mkdir -p data

# Iniciar el servicio
echo "✅ Iniciando servidor en puerto 3006..."
uvicorn src.main:app --host 0.0.0.0 --port 3006 --reload
