# Script PowerShell para iniciar el proyecto Glifos Mayas

Write-Host "🚀 Iniciando Diccionario de Glifos Mayas..." -ForegroundColor Cyan
Write-Host ""

# Verificar que Docker esté corriendo
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker no está corriendo"
    }
} catch {
    Write-Host "❌ Error: Docker no está corriendo" -ForegroundColor Red
    Write-Host "Por favor, inicia Docker Desktop y vuelve a ejecutar este script" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "✅ Docker está corriendo" -ForegroundColor Green
Write-Host ""

# Verificar archivo .env
if (-not (Test-Path .env)) {
    Write-Host "⚠️  No se encontró archivo .env" -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Write-Host "Copiando .env.example a .env..." -ForegroundColor Yellow
        Copy-Item .env.example .env
        Write-Host "⚠️  Por favor, configura las variables en .env antes de continuar" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

Write-Host "✅ Archivo .env encontrado" -ForegroundColor Green
Write-Host ""

# Detener contenedores previos si existen
Write-Host "🛑 Deteniendo contenedores previos..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null

Write-Host ""
Write-Host "🏗️  Construyendo y levantando servicios..." -ForegroundColor Cyan
docker-compose up -d --build

Write-Host ""
Write-Host "⏳ Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "✅ ¡Servicios iniciados!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Aplicación disponible en:" -ForegroundColor Cyan
Write-Host "   🌐 http://localhost:81" -ForegroundColor White
Write-Host ""
Write-Host "🔧 phpMyAdmin disponible en:" -ForegroundColor Cyan
Write-Host "   🌐 http://localhost:82" -ForegroundColor White
Write-Host ""
Write-Host "📊 Ver logs en tiempo real:" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f app" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Para detener los servicios:" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
