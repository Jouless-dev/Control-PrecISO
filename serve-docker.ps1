# Levanta Control-PrecISO en Docker (nginx en http://localhost:8080)
# Requisito: Docker Desktop en ejecución
# Uso: .\serve-docker.ps1

$ErrorActionPreference = "Stop"
$repoRoot = $PSScriptRoot
Set-Location $repoRoot

$dockerBin = "${env:ProgramFiles}\Docker\Docker\resources\bin"
if (Test-Path $dockerBin) { $env:Path = "$dockerBin;$env:Path" }

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker no está instalado. Instala Docker Desktop."
}

Write-Host "=== Control-PrecISO — Docker ===" -ForegroundColor Cyan

docker info 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Iniciando Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -ErrorAction SilentlyContinue
    $ready = $false
    1..36 | ForEach-Object {
        Start-Sleep -Seconds 5
        docker info 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { $ready = $true; return }
    }
    if (-not $ready) {
        Write-Error "Docker Desktop no arrancó. Abre Docker Desktop manualmente y vuelve a ejecutar este script."
    }
}

docker compose up --build -d
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Listo: http://localhost:8080" -ForegroundColor Green
Write-Host "Detener: docker compose down" -ForegroundColor Gray
