# Control-PrecISO

Aplicación web para gestión SGSI (ISO 27001) y análisis de seguridad del front-end.

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| [`Control-PrecISO-main/`](Control-PrecISO-main/) | Aplicación HTML/JS/CSS (Cognito + API Gateway) |
| [`security-analysis/`](security-analysis/) | Informes, plan de remediación, evidencias y HTML para entrega |

## Documentación de seguridad (entrega)

Índice completo: **[`security-analysis/README.md`](security-analysis/README.md)**

| Para presentar | Abrir en el navegador |
|----------------|------------------------|
| **Informe final** (entregar) | [`INFORME_VULNERABILIDADES_FINAL_print.html`](security-analysis/INFORME_VULNERABILIDADES_FINAL_print.html) |
| Índice de informes | [`security-analysis/INDICE_INFORMES.md`](security-analysis/INDICE_INFORMES.md) |
| Ejecución del plan | [`INFORME_EJECUCION_REMEDIACION_v2_print.html`](security-analysis/INFORME_EJECUCION_REMEDIACION_v2_print.html) |
| Plan de remediación | [`PLAN_REMEDIACION_print.html`](security-analysis/PLAN_REMEDIACION_print.html) |
| Informe inicial v1.0 | [`informes-historicos/INFORME_VULNERABILIDADES_v1.0.md`](security-analysis/informes-historicos/INFORME_VULNERABILIDADES_v1.0.md) |

**PDF:** en cada HTML → `Ctrl+P` → *Guardar como PDF*.

## Resumen del trabajo realizado

1. **Análisis v1.0** — Semgrep (11 SRI), revisión manual (V-001…V-014).
2. **Plan y remediación** — SRI, `apiFetch`, `escapeHtml`, errores seguros, sin `refresh_token` en login.
3. **Verificación FINAL** — Semgrep **0** (11 avisos eran solo V-007/SRI en 11 HTML); informe FINAL con matriz control–vulnerabilidad.
4. **Docker** — despliegue local nginx en puerto 8080.

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
