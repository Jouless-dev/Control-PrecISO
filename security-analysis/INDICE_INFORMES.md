# Índice de informes — Control-PrecISO

Guía única para entender **qué documento leer y en qué orden**.

---

## Para la entrega (recomendado)

| # | Documento | Para qué sirve |
|---|-----------|----------------|
| 1 | [`informes-historicos/INFORME_VULNERABILIDADES_v1.0.md`](informes-historicos/INFORME_VULNERABILIDADES_v1.0.md) | **Antes** — qué vulnerabilidades había |
| 2 | [`PLAN_REMEDIACION.md`](PLAN_REMEDIACION.md) | **Plan** — qué se iba a corregir |
| 3 | [`INFORME_EJECUCION_REMEDIACION_v2.md`](INFORME_EJECUCION_REMEDIACION_v2.md) | **Hecho** — qué se implementó |
| 4 | **[`INFORME_VULNERABILIDADES_FINAL.md`](INFORME_VULNERABILIDADES_FINAL.md)** | **Cierre** — por qué Semgrep 11→0, matriz controles, Docker |
| 5 | [`../DOCKER_SETUP.md`](../DOCKER_SETUP.md) | **Despliegue** — cómo correr en Docker |

**PDF:** abrir `INFORME_VULNERABILIDADES_FINAL_print.html` → Ctrl+P.

---

## Pregunta frecuente: ¿Por qué 11 vulnerabilidades pasaron a 0?

**Respuesta corta:** No pasaron 11 vulnerabilidades distintas a cero.

- **Semgrep (11 → 0):** el mismo problema (**CDN sin SRI**, V-007) en **11 archivos HTML**. Un control (añadir `integrity`) cerró los 11 avisos automáticos.
- **Informe manual (13 IDs):** solo **4 cerrados**, **3 mitigados**, el resto **abierto o parcial**. Detalle en el informe FINAL, sección 2.

---

## Todos los archivos

| Archivo | Versión | Estado |
|---------|---------|--------|
| `INFORME_VULNERABILIDADES_FINAL.md` | **FINAL** | **Vigente — entregar este** |
| `INFORME_VULNERABILIDADES.md` | — | Redirige al FINAL |
| `informes-historicos/INFORME_VULNERABILIDADES_v1.0.md` | 1.0 | Histórico |
| `informes-historicos/INFORME_VULNERABILIDADES_v2.0.md` | 2.0 | Histórico |
| `PLAN_REMEDIACION.md` | 1.0 | Ejecutado |
| `INFORME_EJECUCION_REMEDIACION_v2.md` | 2.0 | Ejecutado |
| `VERIFICACION_REMEDIACION_v1.md` | 1.0 | Evidencia Semgrep/Gitleaks |
| `semgrep-report.json` | — | Evidencia SAST |
| `gitleaks-report.json` | — | Evidencia secretos |

---

## Herramientas

```powershell
.\security-analysis\run-security-scan.ps1
python security-analysis\_build_informe_print_html.py
.\serve-docker.ps1
```
