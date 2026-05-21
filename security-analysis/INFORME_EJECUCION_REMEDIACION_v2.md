# INFORME DE EJECUCIÓN Y CIERRE DE REMEDIACIÓN

| Campo | Valor |
|-------|-------|
| **Proyecto** | Control-PrecISO |
| **Plan de referencia** | `PLAN_REMEDIACION.md` |
| **Hallazgos tratados** | SG-001 a SG-011 (Semgrep) |
| **Fecha de ejecución** | Mayo 2026 |
| **Resultado** | **11/11 hallazgos erradicados** |

---

## 1. Resumen ejecutivo

Se ejecutó el plan de tratamiento derivado del **escaneo SAST Semgrep**. Se aplicó la corrección de **Subresource Integrity (SRI)** en los once archivos HTML reportados y se validó el cierre con **re-escaneo: 0 hallazgos**.

| Indicador | Antes | Después |
|-----------|-------|---------|
| Hallazgos Semgrep | 11 | **0** |
| Hallazgos abiertos | 11 | **0** |
| Estado del tratamiento | Pendiente | **Cerrado al 100 %** |

---

## 2. Acciones realizadas

### 2.1 Remediación técnica (Fase 1)

En cada archivo SG-001…SG-011 se actualizó el `<link>` de Bootstrap 5.3.8 (jsDelivr) incorporando:

- Atributo `integrity` (hash SHA-384)
- Atributo `crossorigin="anonymous"`

**Referencia de implementación:** mismo patrón que `index.html` (archivo sin hallazgo en línea base).

### 2.2 Verificación (Fases 2–3)

| Actividad | Resultado |
|-----------|-----------|
| Prueba visual de pantallas (login, dashboard, gestión) | Estilos Bootstrap cargan correctamente |
| `.\security-analysis\run-security-scan.ps1` | Semgrep: **0 hallazgos** |
| Gitleaks (complemento) | **0 fugas** |

### 2.3 Despliegue local (complemento del proyecto)

Se documentó despliegue con **Docker + nginx** (`docker-compose.yml`, `serve-docker.ps1`) para servir el front-end en `http://localhost:8080`. No corresponde a un hallazgo Semgrep; es entorno de prueba reproducible.

---

## 3. Matriz de cierre de hallazgos

| ID | Archivo | Acción aplicada | Re-escaneo | **Estado final** |
|----|---------|-----------------|------------|------------------|
| SG-001 | `admin-empresas.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-002 | `admin-login.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-003 | `confirmar.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-004 | `dashboard.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-005 | `documentos.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-006 | `gestion-riesgos.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-007 | `login.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-008 | `matriz-riesgos.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-009 | `registro.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-010 | `superadmin-dashboard.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |
| SG-011 | `vulnerabilidades.html` | SRI Bootstrap | Sin coincidencia | **ERRADICADO** |

---

## 4. Evidencias

| Artefacto | Ubicación |
|-----------|-----------|
| Escaneo línea base (11 hallazgos) | `informes-historicos/semgrep-report-linea-base.json` |
| Escaneo post-remediación (0) | `semgrep-report.json` |
| Entorno y fecha | `env-verificacion.txt` |

---

## 5. Conclusión

El plan de tratamiento se **ejecutó en su totalidad**. Los **11 hallazgos** identificados por Semgrep en la línea base quedan **erradicados** y **cerrados**, con evidencia de re-escaneo en **cero coincidencias**. No permanece ningún hallazgo abierto del alcance del ejercicio SAST.

---

**Fin del informe de ejecución**
