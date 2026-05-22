# INFORME FINAL DE ANÁLISIS Y TRATAMIENTO DE VULNERABILIDADES

| | |
|---|---|
| **Proyecto** | Control-PrecISO (aplicación web SGSI / ISO 27001) |
| **Herramienta** | Semgrep OSS 1.163.0 |
| **Reglas** | `auto` + `p/owasp-top-ten` |
| **Alcance** | Código fuente en `Control-PrecISO-main/` rastreado por Git |
| **Fecha** | Mayo 2026 |
| **Veredicto** | **11/11 vulnerabilidades erradicadas — 0 hallazgos abiertos** |

---

# PARTE I — ESCANEO INICIAL (LÍNEA BASE)

## 1.1 Objetivo y metodología

Se realizó un **análisis estático de seguridad (SAST)** con Semgrep, siguiendo un flujo de gestión de vulnerabilidades de tipo empresarial:

1. **Identificación** — escaneo inicial y registro de hallazgos  
2. **Plan de tratamiento** — acciones correctivas por hallazgo  
3. **Verificación** — re-escaneo y cierre  

**Comando ejecutado:**

```text
semgrep scan --config auto --config p/owasp-top-ten
```

**Evidencia línea base:** `informes-historicos/semgrep-report-linea-base.json`

## 1.2 Resumen del escaneo inicial

| Indicador | Resultado |
|-----------|-----------|
| Hallazgos totales | **11** |
| Tipos de regla distintos | **1** (`html.security.audit.missing-integrity`) |
| Severidad (Semgrep) | **Media** (11 ocurrencias) |
| Archivos analizados | 36 |
| Estado al cierre de esta fase | **11 vulnerabilidades abiertas** |

## 1.3 Descripción del hallazgo

Todas las vulnerabilidades detectadas corresponden a la **ausencia de Subresource Integrity (SRI)** en hojas de estilo Bootstrap cargadas desde CDN (jsDelivr). Sin el atributo `integrity`, el navegador no verifica que el archivo descargado coincida con el hash esperado; un CDN comprometido podría inyectar contenido malicioso.

**Referencia:** buenas prácticas OWASP — integridad de recursos de terceros en aplicaciones web.

## 1.4 Tabla de vulnerabilidades (escaneo inicial)

| ID | Regla Semgrep | Severidad | Archivo | Descripción | Estado inicial |
|----|---------------|-----------|---------|-------------|----------------|
| **SG-001** | `html.security.audit.missing-integrity` | Media | `admin-empresas.html` | `<link>` Bootstrap CDN sin `integrity` | Abierto |
| **SG-002** | `html.security.audit.missing-integrity` | Media | `admin-login.html` | Idem | Abierto |
| **SG-003** | `html.security.audit.missing-integrity` | Media | `confirmar.html` | Idem | Abierto |
| **SG-004** | `html.security.audit.missing-integrity` | Media | `dashboard.html` | Idem | Abierto |
| **SG-005** | `html.security.audit.missing-integrity` | Media | `documentos.html` | Idem | Abierto |
| **SG-006** | `html.security.audit.missing-integrity` | Media | `gestion-riesgos.html` | Idem | Abierto |
| **SG-007** | `html.security.audit.missing-integrity` | Media | `login.html` | Idem | Abierto |
| **SG-008** | `html.security.audit.missing-integrity` | Media | `matriz-riesgos.html` | Idem | Abierto |
| **SG-009** | `html.security.audit.missing-integrity` | Media | `registro.html` | Idem | Abierto |
| **SG-010** | `html.security.audit.missing-integrity` | Media | `superadmin-dashboard.html` | Idem | Abierto |
| **SG-011** | `html.security.audit.missing-integrity` | Media | `vulnerabilidades.html` | Idem | Abierto |

**Nota:** `index.html` ya incluía SRI correctamente y **no** fue reportado por Semgrep.

## 1.5 Resumen por severidad (línea base)

| Severidad | Cantidad |
|-----------|----------|
| Media | 11 |
| Alta | 0 |
| Baja | 0 |
| **Total** | **11** |

---

# PARTE II — PLAN DE TRATAMIENTO

## 2.1 Objetivo del plan

**Erradicar el 100 %** de los hallazgos SG-001 a SG-011 mediante la implementación de **Subresource Integrity (SRI)** y validar el cierre con re-escaneo Semgrep en **0 hallazgos**.

| Métrica | Línea base | Objetivo |
|---------|------------|----------|
| Hallazgos Semgrep | 11 | **0** |
| Vulnerabilidades abiertas | 11 | **0** |

## 2.2 Estrategia de remediación

Aplicar en los 11 archivos HTML el mismo patrón de enlace Bootstrap ya correcto en `index.html`:

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous">
```

## 2.3 Plan de acción por vulnerabilidad

| ID | Archivo | Acción correctiva | Control de seguridad |
|----|---------|-------------------|----------------------|
| SG-001 | `admin-empresas.html` | Añadir `integrity` y `crossorigin="anonymous"` | SRI |
| SG-002 | `admin-login.html` | Idem | SRI |
| SG-003 | `confirmar.html` | Idem | SRI |
| SG-004 | `dashboard.html` | Idem | SRI |
| SG-005 | `documentos.html` | Idem | SRI |
| SG-006 | `gestion-riesgos.html` | Idem | SRI |
| SG-007 | `login.html` | Idem | SRI |
| SG-008 | `matriz-riesgos.html` | Idem | SRI |
| SG-009 | `registro.html` | Idem | SRI |
| SG-010 | `superadmin-dashboard.html` | Idem | SRI |
| SG-011 | `vulnerabilidades.html` | Idem | SRI |

## 2.4 Fases de ejecución

| Fase | Actividad | Criterio de salida |
|------|-----------|-------------------|
| 1 | Modificar los 11 HTML en el repositorio | Código actualizado |
| 2 | Prueba funcional (carga de estilos Bootstrap) | Interfaz correcta |
| 3 | Re-escaneo con Semgrep (mismas reglas) | **0 hallazgos** |
| 4 | Documentar cierre en Parte III | 11/11 **ERRADICADAS** |

---

# PARTE III — RE-ESCANEO FINAL Y CIERRE

## 3.1 Ejecución de la remediación

Se aplicó el plan de la Parte II en el código de `Control-PrecISO-main/`. En cada archivo SG-001…SG-011 se actualizó el enlace CDN de Bootstrap 5.3.8 con atributos `integrity` (SHA-384) y `crossorigin="anonymous"`.

## 3.2 Re-escaneo de verificación

| Parámetro | Valor |
|-----------|-------|
| Herramienta | Semgrep 1.163.0 |
| Reglas | `auto` + `p/owasp-top-ten` |
| Archivos analizados | 42 |
| Reglas ejecutadas | 260 |
| **Hallazgos** | **0** |
| Fecha (última corrida) | Ver `env-verificacion.txt` |

**Evidencia:** `semgrep-report.json`

## 3.3 Tabla de cierre de vulnerabilidades

| ID | Archivo | Escaneo inicial | Re-escaneo final | **Estado** |
|----|---------|-----------------|------------------|------------|
| SG-001 | `admin-empresas.html` | Detectado | No detectado | **ERRADICADA** |
| SG-002 | `admin-login.html` | Detectado | No detectado | **ERRADICADA** |
| SG-003 | `confirmar.html` | Detectado | No detectado | **ERRADICADA** |
| SG-004 | `dashboard.html` | Detectado | No detectado | **ERRADICADA** |
| SG-005 | `documentos.html` | Detectado | No detectado | **ERRADICADA** |
| SG-006 | `gestion-riesgos.html` | Detectado | No detectado | **ERRADICADA** |
| SG-007 | `login.html` | Detectado | No detectado | **ERRADICADA** |
| SG-008 | `matriz-riesgos.html` | Detectado | No detectado | **ERRADICADA** |
| SG-009 | `registro.html` | Detectado | No detectado | **ERRADICADA** |
| SG-010 | `superadmin-dashboard.html` | Detectado | No detectado | **ERRADICADA** |
| SG-011 | `vulnerabilidades.html` | Detectado | No detectado | **ERRADICADA** |

## 3.4 Resumen de cierre

| Concepto | Línea base | Final |
|----------|------------|-------|
| Hallazgos Semgrep | 11 | **0** |
| Vulnerabilidades abiertas | 11 | **0** |
| Vulnerabilidades erradicadas | 0 | **11** |
| **Tasa de cierre** | 0 % | **100 %** |

## 3.5 Conclusión formal

1. El escaneo inicial Semgrep identificó **11 vulnerabilidades** (SG-001 a SG-011), todas relacionadas con la ausencia de SRI en recursos Bootstrap CDN.  
2. Se ejecutó el **plan de tratamiento** aplicando SRI en los once archivos afectados.  
3. El **re-escaneo final** reportó **cero hallazgos**, confirmando que **todas las vulnerabilidades del alcance fueron erradicadas**.  
4. **No permanece ninguna vulnerabilidad abierta** detectada por Semgrep en el ejercicio.

---

## Evidencias adjuntas

| Archivo | Contenido |
|---------|-----------|
| `informes-historicos/semgrep-report-linea-base.json` | Escaneo inicial (11 hallazgos) |
| `semgrep-report.json` | Re-escaneo final (0 hallazgos) |
| `env-verificacion.txt` | Herramientas y fechas |

---

**Fin del informe final**
