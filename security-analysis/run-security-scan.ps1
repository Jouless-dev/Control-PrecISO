# Ejecuta Semgrep + Gitleaks y actualiza env-verificacion.txt
# Uso (desde la raíz del repo): .\security-analysis\run-security-scan.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$outDir = $PSScriptRoot
Set-Location $repoRoot

function Get-CmdVersion($label, $scriptBlock) {
    try {
        $v = & $scriptBlock 2>&1 | Out-String
        return "$label`: $($v.Trim())"
    } catch {
        return "$label`: NO INSTALADO - $($_.Exception.Message)"
    }
}

# Certificados SSL para Python/Semgrep (redes con proxy o antivirus)
try {
    $certPath = python -c "import certifi; print(certifi.where())" 2>$null
    if ($certPath) {
        $env:SSL_CERT_FILE = $certPath.Trim()
        $env:REQUESTS_CA_BUNDLE = $certPath.Trim()
    }
} catch { }

Write-Host "=== Verificacion de herramientas ===" -ForegroundColor Cyan
$lines = @(
    "=== Verificacion entorno ($(Get-Date -Format 'yyyy-MM-dd HH:mm')) ===",
    (Get-CmdVersion "Git" { git --version }),
    (Get-CmdVersion "Python" { python --version }),
    (Get-CmdVersion "pip" { python -m pip --version }),
    (Get-CmdVersion "Semgrep" { semgrep --version }),
    (Get-CmdVersion "Gitleaks" { gitleaks version }),
    (Get-CmdVersion "Java" { java -version })
)
$lines | Set-Content -Encoding UTF8 (Join-Path $outDir "env-verificacion.txt")
$lines | ForEach-Object { Write-Host $_ }

if (-not (Test-Path (Join-Path $repoRoot ".git"))) {
    Write-Warning "No hay carpeta .git. Inicializa el repo antes de escanear (Semgrep usa archivos rastreados por Git)."
    exit 1
}

Write-Host "`n=== Gitleaks ===" -ForegroundColor Cyan
gitleaks detect --source $repoRoot `
    --report-path (Join-Path $outDir "gitleaks-report.json") `
    --report-format json
Write-Host "Reporte: security-analysis/gitleaks-report.json"

Write-Host "`n=== Semgrep ===" -ForegroundColor Cyan
$semgrepJson = Join-Path $outDir "semgrep-report.json"
$semgrepTxt = Join-Path $outDir "semgrep-report.txt"
$localRules = Join-Path $outDir "semgrep-rules"

$semgrepOk = $false
$semgrepMode = ""

# 1) Intentar reglas en línea (auto + OWASP) — requiere semgrep.dev
Write-Host "Intento 1: reglas en linea (auto + owasp-top-ten)..." -ForegroundColor Gray
try {
    semgrep scan --config auto --config p/owasp-top-ten `
        --exclude security-analysis `
        --exclude dependency-check-tool `
        --json -o $semgrepJson 2>&1 | Tee-Object -FilePath $semgrepTxt
    if ($LASTEXITCODE -eq 0) {
        $semgrepOk = $true
        $semgrepMode = "online (auto + p/owasp-top-ten)"
    }
} catch {
    Write-Host "Fallo conexion SSL o red a semgrep.dev." -ForegroundColor Yellow
}

# 2) Reglas locales (sin internet) — misma regla SRI del informe
if (-not $semgrepOk) {
    Write-Host "Intento 2: reglas locales (missing-integrity, sin internet)..." -ForegroundColor Yellow
    semgrep scan --config $localRules `
        --exclude security-analysis `
        --exclude dependency-check-tool `
        --json -o $semgrepJson 2>&1 | Tee-Object -FilePath $semgrepTxt
    if ($LASTEXITCODE -eq 0) {
        $semgrepOk = $true
        $semgrepMode = "local (semgrep-rules/missing-integrity.yaml)"
    }
}

if (-not $semgrepOk) {
    Write-Host "Semgrep no completo. Revisa semgrep-report.txt" -ForegroundColor Red
    exit 1
}

# Resumen de hallazgos
$count = 0
try {
    $report = Get-Content $semgrepJson -Raw | ConvertFrom-Json
    $count = @($report.results).Count
} catch { }

Add-Content -Encoding UTF8 (Join-Path $outDir "env-verificacion.txt") @"

=== Ultimo escaneo Semgrep ===
Modo: $semgrepMode
Hallazgos: $count
Reporte: security-analysis/semgrep-report.json
"@

Write-Host ""
if ($count -eq 0) {
    Write-Host "RESULTADO: 0 hallazgos (vulnerabilidades del escaneo: ninguna detectada)" -ForegroundColor Green
} else {
    Write-Host "RESULTADO: $count hallazgo(s) — revisa semgrep-report.json" -ForegroundColor Red
}

Write-Host "`nListo." -ForegroundColor Green
