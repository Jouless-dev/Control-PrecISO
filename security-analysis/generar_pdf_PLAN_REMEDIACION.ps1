# Regenerar PLAN_REMEDIACION.pdf desde el HTML (Windows + Microsoft Edge)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$html = Join-Path $here "PLAN_REMEDIACION_print.html"
$pdf  = Join-Path $here "PLAN_REMEDIACION.pdf"
$edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe" }
if (-not (Test-Path $edge)) { throw "No se encontró Microsoft Edge." }
if (-not (Test-Path $html)) { throw "No existe $html. Ejecute antes: python _build_informe_print_html.py" }
$uri = ([System.Uri](Resolve-Path $html)).AbsoluteUri
if (Test-Path $pdf) { Remove-Item $pdf -Force }
& $edge --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$pdf" $uri
Start-Sleep -Seconds 3
if (-not (Test-Path $pdf)) { throw "No se generó el PDF." }
Write-Host "Listo:" $pdf
