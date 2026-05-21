# Control-PrecISO

Aplicación web para gestión SGSI (ISO 27001) y análisis de seguridad del front-end.

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| [`Control-PrecISO-main/`](Control-PrecISO-main/) | Aplicación HTML/JS/CSS (Cognito + API Gateway) |
| [`security-analysis/`](security-analysis/) | Informes, plan de remediación, evidencias y HTML para entrega |

## Documentación de seguridad (entrega SAST)

Índice: **[`security-analysis/INDICE_INFORMES.md`](security-analysis/INDICE_INFORMES.md)**

| # | Documento (PDF: Ctrl+P) |
|---|-------------------------|
| 1 | [`INFORME_ESCANEO_INICIAL_SEMGREP_print.html`](security-analysis/informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP_print.html) — 11 hallazgos |
| 2 | [`PLAN_REMEDIACION_print.html`](security-analysis/PLAN_REMEDIACION_print.html) |
| 3 | [`INFORME_EJECUCION_REMEDIACION_v2_print.html`](security-analysis/INFORME_EJECUCION_REMEDIACION_v2_print.html) |
| 4 | [`INFORME_VULNERABILIDADES_FINAL_print.html`](security-analysis/INFORME_VULNERABILIDADES_FINAL_print.html) — **cierre: 0 abiertos** |

## Resumen

- **Semgrep línea base:** 11 hallazgos (CDN sin SRI) → **tratados y erradicados** → re-escaneo **0**.
- **Docker:** despliegue local en puerto 8080 (`serve-docker.ps1`).

## Despliegue local con Docker

Requisito: **Docker Desktop** en ejecución (usa WSL2 + Ubuntu).

```powershell
.\serve-docker.ps1
```

Abrir: **http://localhost:8080** — Detener: `docker compose down`

Login y APIs siguen en **AWS** (Cognito + API Gateway).

Si Docker no arranca, ver [`DOCKER_SETUP.md`](DOCKER_SETUP.md).

## Herramientas

```powershell
# Análisis estático
.\security-analysis\run-security-scan.ps1

# Regenerar HTML imprimibles
python security-analysis\_build_informe_print_html.py
```

## Requisitos de desarrollo

- Navegador moderno para probar la app
- Cuenta/configuración AWS (Cognito, APIs) según `Control-PrecISO-main/js/config.js`
- Para análisis: Git, Python 3.12+, Semgrep, Gitleaks (ver `security-analysis/env-verificacion.txt`)
