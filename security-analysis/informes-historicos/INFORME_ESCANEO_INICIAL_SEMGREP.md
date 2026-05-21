# INFORME DE ESCANEO DE VULNERABILIDADES (LÍNEA BASE)

| Campo | Valor |
|-------|-------|
| **Proyecto** | Control-PrecISO |
| **Tipo de documento** | Informe de resultados SAST — línea base |
| **Herramienta** | Semgrep OSS 1.163.0 |
| **Fecha del escaneo** | Mayo 2026 |
| **Alcance** | Código fuente en `Control-PrecISO-main/` rastreado por Git |
| **Reglas** | `auto` + `p/owasp-top-ten` |

---

## 1. Resumen ejecutivo

Se ejecutó un **análisis estático de seguridad (SAST)** con Semgrep sobre el front-end del proyecto. El escaneo identificó **11 hallazgos de seguridad**, todos de la **misma categoría**: ausencia de **Subresource Integrity (SRI)** en recursos Bootstrap cargados desde CDN.

| Indicador | Valor |
|-----------|-------|
| Hallazgos totales | **11** |
| Críticos / Altos / Medios (Semgrep) | Según severidad de regla: **Media** |
| Hallazgos distintos (tipos de regla) | **1** (repetido en 11 archivos) |
| Estado al cierre de este informe | **Abierto** — pendiente de plan de remediación |

---

## 2. Metodología (enfoque empresarial)

| Fase | Actividad |
|------|-----------|
| **Preparación** | Inventario de repositorio; exclusión de `security-analysis/` y herramientas auxiliares |
| **Ejecución** | `semgrep scan --config auto --config p/owasp-top-ten` |
| **Análisis** | Clasificación por ID interno (SG-xxx), archivo y regla Semgrep |
| **Reporte** | Registro de hallazgos y trazabilidad hacia plan de tratamiento |
| **Verificación posterior** | Re-escaneo tras remediación (informe de cierre) |

**Complemento:** Gitleaks 8.30.1 — **0 secretos** detectados (no constituye hallazgo de vulnerabilidad en este registro).

---

## 3. Registro de hallazgos (Semgrep)

| ID | Regla Semgrep | Severidad | Archivo | Descripción |
|----|---------------|-----------|---------|-------------|
| **SG-001** | `html.security.audit.missing-integrity` | Media | `admin-empresas.html` | Etiqueta `<link>` a CDN sin atributo `integrity` |
| **SG-002** | `html.security.audit.missing-integrity` | Media | `admin-login.html` | Idem |
| **SG-003** | `html.security.audit.missing-integrity` | Media | `confirmar.html` | Idem |
| **SG-004** | `html.security.audit.missing-integrity` | Media | `dashboard.html` | Idem |
| **SG-005** | `html.security.audit.missing-integrity` | Media | `documentos.html` | Idem |
| **SG-006** | `html.security.audit.missing-integrity` | Media | `gestion-riesgos.html` | Idem |
| **SG-007** | `html.security.audit.missing-integrity` | Media | `login.html` | Idem |
| **SG-008** | `html.security.audit.missing-integrity` | Media | `matriz-riesgos.html` | Idem |
| **SG-009** | `html.security.audit.missing-integrity` | Media | `registro.html` | Idem |
| **SG-010** | `html.security.audit.missing-integrity` | Media | `superadmin-dashboard.html` | Idem |
| **SG-011** | `html.security.audit.missing-integrity` | Media | `vulnerabilidades.html` | Idem |

**Referencia OWASP:** integridad de recursos de terceros (supply chain del cliente web).  
**Riesgo:** si el CDN se compromete, podría servirse CSS/JS alterado al navegador del usuario.

**Nota:** `index.html` ya incluía SRI y **no** generó hallazgo.

---

## 4. Resumen por severidad

| Severidad | Cantidad |
|-----------|----------|
| Media | 11 |
| Alta | 0 |
| Baja | 0 |
| **Total** | **11** |

---

## 5. Conclusión de la línea base

El proyecto presenta **11 hallazgos abiertos** detectados automáticamente, unificables en un **único tratamiento técnico** (implementar SRI en enlaces Bootstrap). Se recomienda ejecutar el **Plan de remediación** y validar con **re-escaneo Semgrep** hasta obtener **0 hallazgos**.

**Evidencia:** `informes-historicos/semgrep-report-linea-base.json` (export del escaneo inicial).

---

**Fin del informe de escaneo inicial**
