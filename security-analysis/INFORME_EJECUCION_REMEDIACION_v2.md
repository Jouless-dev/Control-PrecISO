# INFORME DE EJECUCIÓN DEL PLAN DE REMEDIACIÓN

| | |
|---|---|
| **Proyecto** | Control-PrecISO |
| **Versión** | 2.0 |
| **Fecha** | 20 de mayo de 2026 |
| **Plan de referencia** | `PLAN_REMEDIACION.md` v1.0 |
| **Informe de vulnerabilidades** | v1.0 (línea base) → v2.0 (verificación) |

---

## 1. Resumen

Se ejecutó el **Plan de remediación v1.0** sobre el código en `Control-PrecISO-main/`, sin modificar configuración AWS ni el flujo de login de Cognito.

| Resultado | Detalle |
|-----------|---------|
| **Estado del plan** | Completado (Fases 1 a 4) |
| **Semgrep** | De **11** a **0** hallazgos |
| **Gitleaks** | **0** fugas (sin cambio) |
| **Archivos de código tocados** | 20+ HTML, `js/auth.js`, nuevo `js/utils.js` |

---

## 2. Objetivos cumplidos

| Criterio del plan (§7) | Cumplido |
|------------------------|----------|
| Semgrep 0 hallazgos SRI | Sí |
| Gitleaks 0 | Sí |
| Una sola `getAccessToken()` | Sí |
| 5 archivos sin `innerHTML` + `error.message` | Sí |
| `fetch` a API con token cuando hay sesión | Sí (`apiFetch`) |
| `escapeHtml` en prioridad 1 | Sí |
| Sin cambiar URLs ni Cognito | Sí |

---

## 3. Fases ejecutadas

### Fase 1 — Bajo riesgo

| ID | Acción realizada | Archivos principales |
|----|------------------|----------------------|
| V-014 | Eliminada definición duplicada de `getAccessToken()` | `js/auth.js` |
| V-007 | Añadido `integrity` y `crossorigin` a Bootstrap 5.3.8 CDN | 11 HTML + `index.html` ya lo tenía |
| V-005 | Errores con `showLoadError()` en lugar de `innerHTML` | `superadmin-reportes.html`, `superadmin-controles.html`, `superadmin-controles-proveedores.html`, `matriz-riesgos.html`, `admin-empresas.html` |

### Fase 2 — Utilidades y APIs

| ID | Acción realizada | Detalle |
|----|------------------|---------|
| V-006 | `authHeaders()`, `apiFetch()`, `handleUnauthorized()` | `js/auth.js` |
| V-006 | Sustitución `fetch` → `apiFetch` en URLs de API Gateway | 18 archivos HTML |
| V-006 | POST con `authHeaders({ 'Content-Type': 'application/json' })` | Múltiples formularios |
| V-004 | Creado `js/utils.js` con `escapeHtml` y `showLoadError` | Nuevo archivo |
| — | Inclusión de `config.js`, `auth.js`, `utils.js` donde faltaba | p. ej. vistas superadmin |

**Excepción:** llamadas a `cognito-idp` siguen usando `fetch` directo (sin token de API).

### Fase 3 — XSS en datos dinámicos

| Prioridad | Archivos | Medida |
|-----------|----------|--------|
| P1 | `gestion-proveedores.html`, `admin-empresas.html`, `reportes.html`, `gestion-controles.html`, `modificar-proveedor.html` | `escapeHtml` en campos de API |
| P2 | `implementacion.html`, `capacitacion.html`, `auditoria.html`, `auditoria-proveedor.html`, `todo-en-uno.html`, `superadmin-reportes.html`, `superadmin-controles.html` | Misma medida en tarjetas y listados |
| Unificación | `gestion-riesgos.html`, `matriz-riesgos.html`, `vulnerabilidades.html`, `superadmin-controles-proveedores.html` | Eliminada función `escapeHtml` local; uso de `utils.js` |

### Fase 4 — V-001 parcial

| Verificación | Resultado |
|--------------|-----------|
| Uso de `refresh_token` en el proyecto | Solo `setItem` / `removeItem` en `auth.js` |
| Acción | Dejó de guardarse en login; `logout()` sigue limpiando por higiene |
| **No aplicado** | Sacar `access_token` / `id_token` de `localStorage` |

---

## 4. Alcance no ejecutado (según plan)

| ID | Motivo |
|----|--------|
| V-003 | Riesgo de romper demo con `empresa_id = 8` |
| V-002 | Requiere validación en servidor, no solo front |
| V-008, V-009, V-010, V-011 | Cognito, CSP o rediseño — fuera de alcance v1.0 |
| V-001 completo | Requiere cookies HttpOnly o BFF |

---

## 5. Verificación posterior

| Herramienta | Comando / script | Resultado |
|-------------|------------------|-----------|
| Semgrep + Gitleaks | `run-security-scan.ps1` | 0 + 0 |
| Revisión manual | Controles §2 | Cumplidos |
| Prueba manual | Pendiente en entorno del equipo | Login, dashboard, proveedores, superadmin |

Evidencia numérica: `env-verificacion.txt`, `semgrep-report.json`, `VERIFICACION_REMEDIACION_v1.md`.

---

## 6. Artefactos de código nuevos o clave

```text
Control-PrecISO-main/js/utils.js     → escapeHtml, showLoadError
Control-PrecISO-main/js/auth.js      → apiFetch, authHeaders, getAccessToken única
```

---

## 7. Conclusión

El Plan de remediación v1.0 se **ejecutó según lo definido**. Se redujo de forma verificable la superficie detectada por Semgrep y se reforzó el cliente frente a XSS y llamadas sin token. Los riesgos residuales quedan documentados en el **Informe de vulnerabilidades v2.0**.

---

**Fin del informe de ejecución — versión 2.0**
