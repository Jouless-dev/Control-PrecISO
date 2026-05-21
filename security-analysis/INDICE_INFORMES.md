# Índice de informes — Control-PrecISO (SAST / Semgrep)

Ciclo de vulnerabilidades **solo con hallazgos Semgrep**, formato empresarial académico.

---

## Orden de entrega (PDF: Ctrl+P en cada `*_print.html`)

| # | Documento | Rol |
|---|-----------|-----|
| 1 | [`informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP.md`](informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP.md) | **Identificación** — 11 hallazgos (SG-001…SG-011) |
| 2 | [`PLAN_REMEDIACION.md`](PLAN_REMEDIACION.md) | **Plan de tratamiento** |
| 3 | [`INFORME_EJECUCION_REMEDIACION_v2.md`](INFORME_EJECUCION_REMEDIACION_v2.md) | **Ejecución y cierre** — 11/11 erradicados |
| 4 | **[`INFORME_VULNERABILIDADES_FINAL.md`](INFORME_VULNERABILIDADES_FINAL.md)** | **Acta de cierre** — 0 hallazgos abiertos |

---

## Impresión

| Documento | HTML |
|-----------|------|
| Escaneo inicial | Copiar desde MD o usar informe FINAL §3.1 |
| Plan | [`PLAN_REMEDIACION_print.html`](PLAN_REMEDIACION_print.html) |
| Ejecución | [`INFORME_EJECUCION_REMEDIACION_v2_print.html`](INFORME_EJECUCION_REMEDIACION_v2_print.html) |
| **Cierre final** | [`INFORME_VULNERABILIDADES_FINAL_print.html`](INFORME_VULNERABILIDADES_FINAL_print.html) |

---

## Evidencias

| Archivo | Contenido |
|---------|-----------|
| `informes-historicos/semgrep-report-linea-base.json` | 11 hallazgos (antes) |
| `semgrep-report.json` | 0 hallazgos (después) |
| `env-verificacion.txt` | Fecha y herramientas |

---

## Resumen del ciclo

| Etapa | Hallazgos Semgrep | Abiertos |
|-------|-------------------|----------|
| Línea base | 11 | 11 |
| Post-remediación | 0 | **0** |
| **Cierre** | — | **100 % erradicados** |
