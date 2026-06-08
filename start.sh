#!/bin/bash

# Script para iniciar el proyecto Glifos Mayas

echo "🚀 Iniciando Diccionario de Glifos Mayas..."
echo ""

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo"
    echo "Por favor, inicia Docker Desktop y vuelve a ejecutar este script"
    exit 1
fi

echo "✅ Docker está corriendo"
echo ""

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "⚠️  No se encontró archivo .env"
    echo "Copiando .env.example a .env..."
    cp .env.example .env
    echo "⚠️  Por favor, configura las variables en .env antes de continuar"
    exit 1
fi

echo "✅ Archivo .env encontrado"
echo ""

# Detener contenedores previos si existen
echo "🛑 Deteniendo contenedores previos..."
docker-compose down

echo ""
echo "🏗️  Construyendo y levantando servicios..."
docker-compose up -d --build

echo ""
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

echo ""
echo "✅ ¡Servicios iniciados!"
echo ""
echo "📱 Aplicación disponible en:"
echo "   🌐 http://localhost:81"
echo ""
echo "🔧 phpMyAdmin disponible en:"
echo "   🌐 http://localhost:82"
echo ""
echo "📊 Ver logs en tiempo real:"
echo "   docker-compose logs -f app"
echo ""
echo "🛑 Para detener los servicios:"
echo "   docker-compose down"
echo ""
