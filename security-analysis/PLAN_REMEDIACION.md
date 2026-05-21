# PLAN DE TRATAMIENTO DE VULNERABILIDADES (SAST)

| Campo | Valor |
|-------|-------|
| **Proyecto** | Control-PrecISO |
| **Documento base** | `informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP.md` |
| **Herramienta origen** | Semgrep OSS 1.163.0 |
| **Hallazgos a tratar** | SG-001 a SG-011 (11) |
| **Fecha del plan** | Mayo 2026 |
| **Estado** | **Ejecutado y cerrado** |

---

## 1. Objetivo

**Erradicar el 100 %** de los hallazgos reportados por Semgrep en la línea base, mediante la implementación de **Subresource Integrity (SRI)** en todos los archivos HTML afectados, y **verificar** el cierre con un re-escaneo que reporte **0 hallazgos**.

| Métrica | Línea base | Objetivo |
|---------|------------|----------|
| Hallazgos Semgrep | 11 | **0** |
| Hallazgos abiertos | 11 | **0** |
| Tasa de cierre | 0 % | **100 %** |

---

## 2. Alcance

| Incluido | Excluido |
|----------|----------|
| Los 11 archivos HTML listados en el informe de escaneo | Hallazgos no detectados por Semgrep en la línea base |
| Atributos `integrity` y `crossorigin` en Bootstrap 5.3.8 CDN | Cambios en AWS Cognito o API Gateway |
| Re-ejecución de `run-security-scan.ps1` | Nuevas reglas o herramientas fuera del alcance académico |

---

## 3. Estrategia de remediación

**Tratamiento único replicable:** copiar el patrón de enlace Bootstrap ya correcto en `index.html` hacia el resto de páginas con la misma dependencia CDN.

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous">
```

---

## 4. Plan de acción por hallazgo

| ID | Archivo | Acción | Responsable | Estado planificado |
|----|---------|--------|-------------|-------------------|
| SG-001 | `admin-empresas.html` | Añadir SRI + `crossorigin` | Desarrollo | Cerrar |
| SG-002 | `admin-login.html` | Idem | Desarrollo | Cerrar |
| SG-003 | `confirmar.html` | Idem | Desarrollo | Cerrar |
| SG-004 | `dashboard.html` | Idem | Desarrollo | Cerrar |
| SG-005 | `documentos.html` | Idem | Desarrollo | Cerrar |
| SG-006 | `gestion-riesgos.html` | Idem | Desarrollo | Cerrar |
| SG-007 | `login.html` | Idem | Desarrollo | Cerrar |
| SG-008 | `matriz-riesgos.html` | Idem | Desarrollo | Cerrar |
| SG-009 | `registro.html` | Idem | Desarrollo | Cerrar |
| SG-010 | `superadmin-dashboard.html` | Idem | Desarrollo | Cerrar |
| SG-011 | `vulnerabilidades.html` | Idem | Desarrollo | Cerrar |

---

## 5. Fases y cronograma

| Fase | Actividad | Criterio de salida |
|------|-----------|-------------------|
| **1** | Aplicar SRI en los 11 HTML | Código actualizado en repositorio |
| **2** | Prueba funcional (carga de estilos Bootstrap) | Páginas renderizan correctamente |
| **3** | Re-escaneo Semgrep | **0 hallazgos** |
| **4** | Informe de ejecución y cierre | 11/11 **ERRADICADOS** |

---

## 6. Verificación y criterios de aceptación

| Criterio | Método | Resultado esperado |
|----------|--------|-------------------|
| CA-1 | `semgrep scan` (mismas reglas que línea base) | 0 findings |
| CA-2 | Registro SG-001…SG-011 | Estado **ERRADICADO** |
| CA-3 | Evidencia archivada | `semgrep-report.json` actualizado |

---

## 7. Riesgos residuales del plan

Tras la ejecución completa de este plan, **no quedan hallazgos Semgrep abiertos** del alcance del escaneo inicial. Cualquier hallazgo futuro requerirá un **nuevo ciclo** de escaneo (nueva línea base).

---

**Fin del plan de tratamiento**
