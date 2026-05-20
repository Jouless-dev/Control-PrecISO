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
    Write-Warning "No hay carpeta .git. Ejecuta: git init (o clona el repo del equipo antes de escanear con Semgrep)."
    exit 1
}

Write-Host "`n=== Gitleaks ===" -ForegroundColor Cyan
gitleaks detect --source $repoRoot `
    --report-path (Join-Path $outDir "gitleaks-report.json") `
    --report-format json
Write-Host "Reporte: security-analysis/gitleaks-report.json"

Write-Host "`n=== Semgrep (puede tardar varios minutos) ===" -ForegroundColor Cyan
$semgrepJson = Join-Path $outDir "semgrep-report.json"
$semgrepTxt = Join-Path $outDir "semgrep-report.txt"

semgrep scan --config auto --config p/owasp-top-ten `
    --exclude security-analysis `
    --exclude dependency-check-tool `
    --json -o $semgrepJson | Tee-Object -FilePath $semgrepTxt

Write-Host "`nListo. Revisa:" -ForegroundColor Green
Write-Host "  - security-analysis/semgrep-report.json"
Write-Host "  - security-analysis/semgrep-report.txt"
Write-Host "  - security-analysis/gitleaks-report.json"
