# Análisis de seguridad (SAST — Semgrep)

Gestión de vulnerabilidades detectadas por **Semgrep** — ciclo completo con **cierre al 100 %**.

## Entregar al profesor

1. **Escaneo inicial** — `informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP.md`
2. **Plan** — `PLAN_REMEDIACION_print.html`
3. **Ejecución** — `INFORME_EJECUCION_REMEDIACION_v2_print.html`
4. **Cierre final** — `INFORME_VULNERABILIDADES_FINAL_print.html`

Índice: [`INDICE_INFORMES.md`](INDICE_INFORMES.md)

## Resultado

| | Línea base | Final |
|--|------------|-------|
| Hallazgos Semgrep | 11 | **0** |
| Estado | Abiertos | **Todos erradicados (SG-001…SG-011)** |

## Comandos

```powershell
.\security-analysis\run-security-scan.ps1
python security-analysis\_build_informe_print_html.py
.\serve-docker.ps1
```
