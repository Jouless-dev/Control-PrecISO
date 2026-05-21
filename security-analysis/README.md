# Análisis de seguridad — Control-PrecISO

Ciclo **identificar → planificar → remediar → verificar → desplegar** (SGSI / ISO 27001).

## Empieza aquí

**[`INDICE_INFORMES.md`](INDICE_INFORMES.md)** — orden de lectura y respuesta a *“¿por qué Semgrep pasó de 11 a 0?”*

## Informe para entregar (FINAL)

| | |
|--|--|
| **Markdown** | [`INFORME_VULNERABILIDADES_FINAL.md`](INFORME_VULNERABILIDADES_FINAL.md) |
| **PDF** | Abrir [`INFORME_VULNERABILIDADES_FINAL_print.html`](INFORME_VULNERABILIDADES_FINAL_print.html) → Ctrl+P |

El informe FINAL explica que los **11 avisos Semgrep eran el mismo problema (V-007) en 11 HTML**, no 11 vulnerabilidades distintas, y relaciona **cada control** con su hallazgo.

## Orden lógico de documentos

```
v1.0 (histórico)  →  PLAN  →  EJECUCIÓN  →  VERIFICACIÓN  →  INFORME FINAL + Docker
```

| # | Archivo |
|---|---------|
| 1 | `informes-historicos/INFORME_VULNERABILIDADES_v1.0.md` |
| 2 | `PLAN_REMEDIACION.md` |
| 3 | `INFORME_EJECUCION_REMEDIACION_v2.md` |
| 4 | `VERIFICACION_REMEDIACION_v1.md` |
| 5 | **`INFORME_VULNERABILIDADES_FINAL.md`** |

## Evidencias

| Archivo | Contenido |
|---------|-----------|
| `semgrep-report.json` | 0 hallazgos (corrida final; incluye Dockerfile) |
| `gitleaks-report.json` | 0 fugas |
| `env-verificacion.txt` | Herramientas y fecha |

## Despliegue local (Docker)

En la raíz del repo: `serve-docker.ps1` → **http://localhost:8080**  
Guía: [`../DOCKER_SETUP.md`](../DOCKER_SETUP.md)

## Comandos

```powershell
.\security-analysis\run-security-scan.ps1
python security-analysis\_build_informe_print_html.py
```
