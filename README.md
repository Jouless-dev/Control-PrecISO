# Control-PrecISO

Aplicación web para gestión SGSI (ISO 27001) y análisis de seguridad del front-end.

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| [`Control-PrecISO-main/`](Control-PrecISO-main/) | Aplicación HTML/JS/CSS (Cognito + API Gateway) |
| [`security-analysis/`](security-analysis/) | Informe final SAST (Semgrep) + evidencias JSON |

## Informe de seguridad (entrega)

Un solo documento con escaneo inicial, plan de tratamiento y cierre:

**[`security-analysis/INFORME_FINAL_print.html`](security-analysis/INFORME_FINAL_print.html)** → Ctrl+P para PDF

- Parte I: 11 vulnerabilidades Semgrep (SG-001…SG-011)  
- Parte II: Plan de tratamiento (SRI)  
- Parte III: Re-escaneo **0 hallazgos** — **100 % erradicadas**

## Docker (despliegue local)

```powershell
.\serve-docker.ps1
```

→ http://localhost:8080

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
