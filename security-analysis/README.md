# Análisis de seguridad — Control-PrecISO

## Informe único de entrega

| | |
|--|--|
| **Documento** | [`INFORME_FINAL.md`](INFORME_FINAL.md) |
| **PDF** | Abrir [`INFORME_FINAL_print.html`](INFORME_FINAL_print.html) → **Ctrl+P** |

El informe incluye en un solo documento:

1. **Parte I** — Escaneo inicial Semgrep y tabla de vulnerabilidades (SG-001…SG-011)  
2. **Parte II** — Plan de tratamiento  
3. **Parte III** — Re-escaneo final y cierre (100 % erradicadas)

## Evidencias

| Archivo | Uso |
|---------|-----|
| `informes-historicos/semgrep-report-linea-base.json` | 11 hallazgos (antes) |
| `semgrep-report.json` | 0 hallazgos (después) |

## Comandos

```powershell
.\security-analysis\run-security-scan.ps1
python security-analysis\_build_informe_print_html.py
```
