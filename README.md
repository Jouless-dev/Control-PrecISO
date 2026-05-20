# Control-PrecISO

Repositorio de trabajo para **análisis de vulnerabilidades**, informes y **remediación** del front-end (HTML/JS) de Control-PrecISO.

**Repositorio:** https://github.com/Jouless-dev/Control-PrecISO

## Contenido

| Carpeta | Descripción |
|---------|-------------|
| `Control-PrecISO-main/` | Código de la aplicación web (SGSI / ISO 27001) |
| `security-analysis/` | Informes, plan de remediación, reportes Semgrep/Gitleaks |

## Para el equipo (integrar en su repo)

1. Clonar este repositorio o descargar ZIP desde GitHub.
2. Revisar `security-analysis/INFORME_VULNERABILIDADES.md` y `PLAN_REMEDIACION.md`.
3. Aplicar los cambios de mitigación en su rama (o copiar archivos modificados de `Control-PrecISO-main/`).
4. Volver a ejecutar las herramientas en su entorno si lo requiere el curso.

## Análisis de seguridad (local)

```powershell
# Desde la raíz del repositorio
.\security-analysis\run-security-scan.ps1
```

Guía detallada: `security-analysis/GUIA_EQUIPO_SEGURIDAD.md`  
Requisitos: Git, Python 3.12+, Semgrep, Gitleaks (ver `security-analysis/env-verificacion.txt`).
