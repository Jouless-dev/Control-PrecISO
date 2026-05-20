# Análisis de seguridad — Control-PrecISO

Documentación del ciclo **identificar → remediar → verificar** (SGSI / ISO 27001).

## Entrega académica (orden recomendado)

| # | Documento | Formato imprimible (PDF) |
|---|-----------|--------------------------|
| 1 | Línea base — Informe v1.0 | `informes-historicos/INFORME_VULNERABILIDADES_v1.0.md` |
| 2 | Plan de remediación v1.0 | `PLAN_REMEDIACION_print.html` |
| 3 | Ejecución del plan | `INFORME_EJECUCION_REMEDIACION_v2_print.html` |
| 4 | **Informe final v2.0** (post-remediación) | `INFORME_VULNERABILIDADES_print.html` |

Abrir cada `*_print.html` en el navegador → **Ctrl+P** → *Guardar como PDF*.

## Documentos actuales

| Archivo | Versión | Descripción |
|---------|---------|-------------|
| `INFORME_VULNERABILIDADES.md` | **2.0** | Estado de vulnerabilidades tras mitigar |
| `INFORME_EJECUCION_REMEDIACION_v2.md` | 2.0 | Qué se aplicó del plan (fases 1–4) |
| `PLAN_REMEDIACION.md` | 1.0 (ejecutado) | Medidas en código; sin cambios AWS |
| `VERIFICACION_REMEDIACION_v1.md` | — | Resumen técnico Semgrep/Gitleaks |
| `informes-historicos/INFORME_VULNERABILIDADES_v1.0.md` | 1.0 | Informe inicial (referencia) |

## Evidencias de herramientas

| Archivo | Contenido |
|---------|-----------|
| `semgrep-report.json` / `.txt` | SAST (0 hallazgos tras remediación) |
| `gitleaks-report.json` | Secretos en Git (0 fugas) |
| `env-verificacion.txt` | Versiones de herramientas y resumen |

## Código de la aplicación

Mitigaciones en `../Control-PrecISO-main/`:

- `js/auth.js` — `apiFetch`, `authHeaders`, sin guardar `refresh_token`
- `js/utils.js` — `escapeHtml`, `showLoadError`
- HTML — SRI en Bootstrap, llamadas API con token

## Regenerar informes HTML

Desde la raíz del repositorio:

```powershell
python security-analysis\_build_informe_print_html.py
```

Genera: `INFORME_VULNERABILIDADES_print.html`, `PLAN_REMEDIACION_print.html`, `INFORME_EJECUCION_REMEDIACION_v2_print.html`.

## Re-ejecutar análisis

```powershell
.\security-analysis\run-security-scan.ps1
```

Requiere: Git, Python, Semgrep, Gitleaks (y Java si se usa Dependency-Check en el futuro).

## Scripts internos (mantenimiento)

| Script | Uso |
|--------|-----|
| `_build_informe_print_html.py` | Markdown → HTML formal |
| `_apply_api_fetch.py` | Migración masiva `fetch` → `apiFetch` (ya aplicada) |
| `_inject_scripts.py` | Inyección de `auth.js` / `utils.js` (ya aplicada) |

No son necesarios para la entrega; se conservan como referencia del proceso.
