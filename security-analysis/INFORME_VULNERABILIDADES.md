# INFORME DE ANÁLISIS DE VULNERABILIDADES

| | |
|---|---|
| **Proyecto** | Control-PrecISO (aplicación web SGSI / ISO 27001) |
| **Versión del informe** | 2.0 (post-remediación) |
| **Fecha** | 20 de mayo de 2026 |
| **Documento anterior** | Informe v1.0 (estado inicial) |
| **Plan aplicado** | `PLAN_REMEDIACION.md` v1.0 |
| **Tipo de análisis** | Estático (código fuente), segunda corrida tras mitigaciones |

---

## 1. Resumen ejecutivo

### Objetivo de este informe

Documentar el **estado de seguridad del front-end después** de ejecutar el Plan de remediación v1.0, comparado con el informe v1.0 (línea base).

### Conclusión general (después de mitigar)

La aplicación **sigue siendo un front-end estático** integrado con Cognito y API Gateway, pero **mejoró de forma medible** en el cliente:

| Área | Antes (v1.0) | Ahora (v2.0) |
|------|--------------|--------------|
| Integridad CDN (Semgrep) | 11 avisos | **0 avisos** |
| Secretos en Git (Gitleaks) | 0 | **0** |
| Token en llamadas a API | Casi ninguna petición | **`apiFetch` con `Authorization`** |
| XSS por datos de API | Muy extendido | **Mitigado** en pantallas prioritarias (`escapeHtml`) |
| Errores en pantalla | `innerHTML` con `error.message` | **`showLoadError` / texto seguro** |
| Código de autenticación | `getAccessToken` duplicada | **Una sola función** |
| Refresh token en navegador | Guardado en `localStorage` | **Ya no se guarda** (mitigación parcial) |

**Riesgos que permanecen** (no cubiertos por el plan v1.0): tokens `access`/`id` en `localStorage` (V-001 parcial), control de rol solo en cliente (V-002), `empresa_id = 8` por defecto (V-003), IDs y URLs visibles (V-008), sin CSP (V-009), flujo de contraseña directo a Cognito (V-010), sin 2FA en UI (V-011).

### Hallazgos por estado (v2.0)

| Estado | Cantidad | IDs |
|--------|----------|-----|
| **Cerrado** | 4 | V-005, V-007, V-014, (V-013 positivo) |
| **Mitigado** | 3 | V-004, V-006, V-001 (parcial) |
| **Abierto** | 6 | V-001 (residual), V-002, V-003, V-008, V-009, V-010, V-011 |

---

## 2. Comparativa informe v1.0 → v2.0

### 2.1 Herramientas automáticas

| Herramienta | Informe v1.0 | Informe v2.0 | Interpretación |
|-------------|--------------|--------------|----------------|
| **Semgrep** 1.163.0 | 11 hallazgos | **0 hallazgos** | Todos eran CDN sin SRI (V-007), corregidos en Fase 1 del plan |
| **Gitleaks** 8.30.1 | 0 fugas | **0 fugas** | Sin cambios en historial Git |
| Archivos escaneados | 36 | 37 | Incluye `js/utils.js` nuevo |

**Importante:** Semgrep **no detectó** en v1.0 los problemas de `localStorage`, XSS ni APIs sin token; esos salieron de **revisión manual**. Por eso **0 en Semgrep no significa cero riesgo total**, sino **cero coincidencias automáticas** con las reglas ejecutadas.

### 2.2 Tabla de hallazgos (estado actual)

| ID | Problema | Gravedad original | Estado v2.0 | Evidencia |
|----|----------|-------------------|-------------|-----------|
| V-001 | Tokens en `localStorage` | Crítica | **Parcial** | Ya no se guarda `refresh_token`; `access_token` e `id_token` siguen en `js/auth.js` |
| V-002 | Rol/permisos en cliente | Alta | **Abierto** | Sin cambio (fuera de alcance del plan) |
| V-003 | `empresa_id` con fallback 8 | Alta | **Abierto** | Sin cambio (plan v1.0 lo excluyó) |
| V-004 | XSS por `innerHTML` | Alta | **Mitigado** | `js/utils.js`, `escapeHtml` en pantallas P1 y P2 |
| V-005 | Errores en `innerHTML` | Media | **Cerrado** | `showLoadError()` en 5 archivos |
| V-006 | APIs sin `Authorization` | Alta | **Mitigado** | `apiFetch()` / `authHeaders()` en APIs propias |
| V-007 | CDN sin SRI | Media | **Cerrado** | `integrity` + `crossorigin` en 12 HTML con Bootstrap |
| V-008 | Configuración expuesta | Media | **Abierto** | `config.js` sin cambios |
| V-009 | Sin CSP | Media | **Abierto** | Sin cambios |
| V-010 | `USER_PASSWORD_AUTH` | Media | **Abierto** | Sin cambios |
| V-011 | Sin 2FA en UI | Baja | **Abierto** | Sin cambios |
| V-013 | Secretos en Git | Informativa | **Cerrado** | Gitleaks: 0 |
| V-014 | `getAccessToken` duplicada | Baja | **Cerrado** | Una función en `auth.js` |

---

## 3. Medidas aplicadas (Plan de remediación v1.0)

Resumen de lo implementado en `Control-PrecISO-main/` (detalle en `INFORME_EJECUCION_REMEDIACION_v2.md`):

| Fase | Medidas | Hallazgos atendidos |
|------|---------|---------------------|
| 1 | SRI Bootstrap, `showLoadError`, unificar `getAccessToken` | V-007, V-005, V-014 |
| 2 | `utils.js`, `apiFetch`, `authHeaders` en APIs | V-006, base V-004 |
| 3 | `escapeHtml` en listados y tarjetas dinámicas | V-004 |
| 4 | Dejar de persistir `refresh_token` | V-001 parcial |

**Principio respetado:** no se modificaron URLs de API, `COGNITO_CONFIG` ni el flujo de login.

---

## 4. Hallazgos que siguen abiertos (prioridad futura)

### V-001 — Sesión en el navegador (Crítica residual)

**Situación v2.0:** ya no se almacena el **refresh token**, lo que reduce el impacto de un XSS prolongado. Siguen en `localStorage` el **access token** y el **id token**.

**Recomendación futura:** cookies `HttpOnly`, BFF o rediseño de sesión (requiere backend o cambios en Cognito).

### V-002 — Autorización en el cliente (Alta)

Los menús y redirecciones siguen basados en decodificar el JWT en el navegador. El plan v1.0 no cambió esta lógica para no romper el flujo actual.

### V-003 — Tenant por defecto = 8 (Alta)

Se mantiene el fallback `empresa_id = 8` en varias pantallas y en `dashboard.html` cuando falla la API. Requiere acuerdo con el equipo antes de eliminarlo.

### V-008 a V-011 (Media / Baja)

Sin cambios: exposición de IDs/URLs, ausencia de CSP, autenticación por contraseña desde SPA, MFA no visible en la interfaz.

---

## 5. Metodología de la segunda corrida

| Paso | Acción | Resultado v2.0 |
|------|--------|----------------|
| 1 | Ejecutar Plan de remediación v1.0 en código | Ver `INFORME_EJECUCION_REMEDIACION_v2.md` |
| 2 | `semgrep scan --config auto --config p/owasp-top-ten` | 0 hallazgos |
| 3 | `gitleaks detect` | 0 hallazgos |
| 4 | Revisión manual de controles aplicados | Tabla §2.2 |

**Fecha de la corrida:** 20 de mayo de 2026, 14:09 (ver `env-verificacion.txt`).

---

## 6. Conclusión de seguridad (v2.0)

| Aspecto | Valoración |
|---------|------------|
| **Mejora respecto a v1.0** | **Significativa** en integridad CDN, cabeceras HTTP, XSS en cliente y higiene de código |
| **Riesgo global residual** | **Medio–Alto** si aparece XSS (por tokens en `localStorage`) o APIs sin validación en servidor |
| **Adecuación académica** | Evidencia de ciclo **identificar → remediar → verificar** (PDCA / SGSI) |
| **Listo para producción** | **No** sin abordar V-001 completo, V-003 y validación en backend |

---

## 7. Evidencias

| Artefacto | Ruta |
|-----------|------|
| Informe v2.0 (este documento) | `security-analysis/INFORME_VULNERABILIDADES.md` |
| Informe v1.0 (referencia histórica) | Misma ruta, versión 1.0 en historial Git |
| Informe ejecución remediación | `security-analysis/INFORME_EJECUCION_REMEDIACION_v2.md` |
| Plan de remediación | `security-analysis/PLAN_REMEDIACION.md` |
| Semgrep JSON (v2.0) | `security-analysis/semgrep-report.json` |
| Gitleaks JSON | `security-analysis/gitleaks-report.json` |
| Verificación técnica | `security-analysis/VERIFICACION_REMEDIACION_v1.md` |

---

**Fin del informe — versión 2.0 (post-remediación)**
