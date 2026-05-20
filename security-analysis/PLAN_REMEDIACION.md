# PLAN DE REMEDIACIÓN DE VULNERABILIDADES

| | |
|---|---|
| **Proyecto** | Control-PrecISO |
| **Versión del plan** | 1.0 |
| **Fecha** | 20 de mayo de 2026 |
| **Documento base** | `INFORME_VULNERABILIDADES.md` v1.0 |
| **Ámbito** | Solo código en `Control-PrecISO-main/` (HTML, CSS, JavaScript) |

---

## 1. Propósito

Definir **qué cambios de código** se pueden aplicar **ahora**, con la información disponible y **sin coordinación con el equipo**, para **reducir el número y la gravedad** de las vulnerabilidades del informe v1.0, manteniendo el comportamiento que hoy funciona contra **Cognito y API Gateway en AWS**.

Este documento es la **autorización de trabajo**: no se modifica la aplicación hasta recibir confirmación explícita para ejecutar.

---

## 2. Principios (no romper lo que ya funciona)

| # | Principio |
|---|-----------|
| P1 | **No cambiar** URLs de API, `COGNITO_CONFIG`, flujo de login ni tipo de autenticación (`USER_PASSWORD_AUTH`). |
| P2 | **No eliminar** el fallback `empresa_id = 8` en esta versión del plan (riesgo de pantallas vacías en demo; ver §6). |
| P3 | **Solo añadir o endurecer** salida HTML y cabeceras HTTP en `fetch` cuando ya exista sesión. |
| P4 | Tras cada fase: prueba manual mínima (login → dashboard → una pantalla de gestión → una de superadmin si aplica). |
| P5 | Tras cada fase: ejecutar `run-security-scan.ps1` y anotar resultados en `env-verificacion.txt`. |

---

## 3. Alcance y exclusiones

### 3.1 Incluido en v1.0

| ID | Mitigación prevista en código |
|----|------------------------------|
| V-004 | Escape sistemático de datos en `innerHTML` |
| V-005 | Errores sin `innerHTML` inseguro |
| V-006 | Cabecera `Authorization` en `fetch` a APIs propias |
| V-007 | SRI en enlaces Bootstrap CDN (11 páginas) |
| V-014 | Una sola función `getAccessToken()` |
| V-004 (refuerzo) | Reutilizar patrón `escapeHtml` ya existente en 4 pantallas |

### 3.2 Mitigación parcial (opcional en Fase 2)

| ID | Acción | Motivo de “parcial” |
|----|--------|---------------------|
| V-001 | Dejar de guardar `refresh_token` **solo si** no se usa en ningún script | Reduce impacto crítico sin cambiar Cognito; requiere verificación previa con `grep` |

### 3.3 Fuera de alcance v1.0 (no reduce conteo en Semgrep; requiere AWS o rediseño)

| ID | Motivo |
|----|--------|
| V-001 (completo) | Sacar todos los tokens de `localStorage` implica cookies `HttpOnly` o backend intermedio |
| V-002 | La autorización real debe validarse en servidor; en front solo se mantiene la UI actual |
| V-003 | Quitar `empresa_id = 8` puede romper el flujo de demo sin confirmación del equipo |
| V-008 | IDs y URLs públicos en SPA; ocultarlos no es viable solo con HTML estático |
| V-009 | CSP estricta puede romper scripts inline en muchas páginas |
| V-010, V-011 | Configuración en consola Cognito, no en este repositorio |

---

## 4. Resultado esperado (reducción de vulnerabilidades)

| Métrica | Antes (informe v1.0) | Objetivo tras plan v1.0 |
|---------|----------------------|-------------------------|
| Hallazgos **Semgrep** | 11 (CDN sin SRI) | **0** |
| Hallazgos **Gitleaks** | 0 | **0** (mantener) |
| **V-007** | Abierto | **Cerrado** |
| **V-005** | Abierto | **Cerrado** (5 archivos) |
| **V-014** | Abierto | **Cerrado** |
| **V-006** | Abierto | **Mitigado en cliente** (token enviado cuando hay sesión)* |
| **V-004** | Abierto | **Mitigado** en pantallas prioritarias; revisión manual del resto |
| **V-001** | Crítica abierta | **Abierta** o **parcial** (solo si Fase 2 opcional aplica) |
| **V-003, V-002, V-008–V-011** | Abiertos | Documentados como limitación v1.0 |

\*Si el API Gateway ignora el header, la app sigue funcionando igual; si en el futuro exige token, el front ya cumple.

**Resumen para exposición:** el plan v1.0 ataca **5 hallazgos de forma completa** y **refuerza 2 de alta gravedad** (V-004, V-006) sin tocar la nube.

---

## 5. Fases de ejecución

### Fase 0 — Preparación (sin cambiar lógica de negocio)

| Tarea | Descripción | Criterio de hecho |
|-------|-------------|-------------------|
| P0-1 | Crear rama o copia de respaldo del estado actual | Punto de restauración claro |
| P0-2 | Inventariar `fetch(` hacia `amazonaws.com` en todos los HTML | Lista en notas o tabla al final de este plan |
| P0-3 | Inventariar `innerHTML` con interpolación `${` de variables de API | Lista priorizada |
| P0-4 | Ejecutar `run-security-scan.ps1` y guardar reportes como línea base | `semgrep-report.json` con 11 hallazgos |

**Esfuerzo estimado:** bajo (1–2 horas).

---

### Fase 1 — Cambios de muy bajo riesgo

Objetivo: cerrar **V-014**, **V-007** y parte de **V-005** sin afectar APIs ni login.

| ID | Tarea concreta | Archivos |
|----|----------------|----------|
| V-014 | Eliminar la primera definición duplicada de `getAccessToken()`; dejar una función documentada que devuelva `access_token` o, si falta, `id_token` (comportamiento actual de la segunda definición) | `js/auth.js` |
| V-007 | Copiar desde `index.html` el enlace Bootstrap con `integrity` y `crossorigin` al resto de páginas con CDN | `admin-empresas.html`, `admin-login.html`, `confirmar.html`, `dashboard.html`, `documentos.html`, `gestion-riesgos.html`, `login.html`, `matriz-riesgos.html`, `registro.html`, `superadmin-dashboard.html`, `vulnerabilidades.html` |
| V-005 | Sustituir `innerHTML` + `error.message` por `textContent` o nodo de texto seguro | `superadmin-reportes.html`, `superadmin-controles.html`, `superadmin-controles-proveedores.html`, `matriz-riesgos.html`, `admin-empresas.html` (solo bloque de error en loading) |

**Verificación Fase 1:**

- [ ] Login y redirección a `dashboard.html` OK  
- [ ] Semgrep: **0** hallazgos `missing-integrity`  
- [ ] Pantallas superadmin cargan o muestran error legible sin romper layout  

**Esfuerzo estimado:** bajo (medio día).

---

### Fase 2 — Utilidades y cabeceras de API

Objetivo: cerrar **V-006** en el cliente y sentar base para **V-004**.

| ID | Tarea concreta | Archivos |
|----|----------------|----------|
| V-006 | En `auth.js`, añadir `function authHeaders(extra = {})` que merge `Content-Type`, y si hay token `Authorization: Bearer …` | `js/auth.js` |
| V-006 | En cada `fetch` a URL que contenga `execute-api` (o dominio API del proyecto), usar `headers: authHeaders()` o `authHeaders({ ... })` | Todos los HTML con `fetch` inventariados en P0-2 |
| V-006 | Si respuesta `401`, redirigir a `login.html` o llamar `logout()` (comportamiento conservador) | Misma lista; probar al menos 2 pantallas |
| V-004 (base) | Crear `js/utils.js` con `escapeHtml(text)` (mismo algoritmo que en `gestion-riesgos.html`) | `js/utils.js` nuevo |
| V-004 (base) | Añadir `<script src="js/utils.js">` en páginas que aún no tengan `escapeHtml` local | Según inventario P0-3 |

**Regla para no romper AWS:** no cambiar método HTTP, URL, query string ni cuerpo JSON; **solo** añadir cabeceras.

**Verificación Fase 2:**

- [ ] Con sesión válida: mismas pantallas cargan datos que antes  
- [ ] Sin sesión: redirección o error controlado, no pantalla en blanco indefinida  
- [ ] Inspección en DevTools: peticiones a API llevan `Authorization` cuando hay token  

**Esfuerzo estimado:** medio (1–2 días).

---

### Fase 3 — XSS en datos de negocio (V-004)

Objetivo: aplicar `escapeHtml()` a campos de texto que vienen de API en plantillas `innerHTML`.

**Prioridad 1 (datos de usuario / administración):**

| Archivo | Campos a escapar (ejemplos) |
|---------|----------------------------|
| `gestion-proveedores.html` | `nombre_empresa`, `nit`, `contacto_*`, textos en tarjetas |
| `admin-empresas.html` | nombres de usuario, empresa, campos en listados |
| `reportes.html` | textos dinámicos en grids y listas |
| `gestion-controles.html` | títulos, descripciones en acordeón |
| `modificar-proveedor.html` | nombres y labels dinámicos |

**Prioridad 2:**

| Archivo | Notas |
|---------|--------|
| `implementacion.html`, `capacitacion.html`, `auditoria.html`, `auditoria-proveedor.html`, `todo-en-uno.html`, `anadir-proveedor.html` | Misma regla en tarjetas de controles |
| `superadmin-reportes.html`, `superadmin-controles.html` | Datos de empresa en tarjetas (errores ya en Fase 1) |

**Pantallas que ya escapan:** unificar usando `utils.js` en lugar de función local duplicada (`gestion-riesgos.html`, `matriz-riesgos.html`, `vulnerabilidades.html`, `superadmin-controles-proveedores.html`).

**Verificación Fase 3:**

- [ ] Probar con datos normales: listas y fichas se ven igual  
- [ ] Prueba manual opcional: si el API permite, dato con `<test>` en nombre no debe ejecutar script  
- [ ] Revisión: no quedan `${variable_api}` sin `escapeHtml` en archivos Prioridad 1  

**Esfuerzo estimado:** medio–alto (2–3 días según inventario).

---

### Fase 4 — Opcional: aligerar V-001 sin cambiar Cognito

**Solo ejecutar si P0-5 confirma que `refresh_token` no se lee en ningún archivo.**

| Tarea | Acción |
|-------|--------|
| P0-5 | Buscar en el proyecto: `getItem('refresh_token')`, `refresh_token` en `fetch` o renovación de sesión |
| V-001 parcial | Si no hay uso: dejar de hacer `setItem('refresh_token', …)` y de eliminarlo en `logout()` se mantiene por higiene |

**Si sí se usa:** omitir Fase 4 y dejar V-001 documentada para versión 2.0 del plan (con backend).

---

## 6. Inventario de referencia (para ejecutar P0-2 y P0-3)

Lista inicial obtenida del análisis v1.0 (completar al ejecutar P0-2/P0-3 con `grep`).

### HTML con `fetch` a APIs (añadir `authHeaders` en Fase 2)

`vulnerabilidades.html`, `todo-en-uno.html`, `superadmin-reportes.html`, `superadmin-controles-proveedores.html`, `superadmin-controles.html`, `reportes.html`, `modificar-proveedor.html`, `matriz-riesgos.html`, `implementacion.html`, `gestion-riesgos.html`, `gestion-proveedores.html`, `gestion-controles.html`, `capacitacion.html`, `auditoria.html`, `auditoria-proveedor.html`, `anadir-proveedor.html`, `admin-empresas.html`, más `registro.html` y `auth.js` (`getEmpresaId`).

### HTML con Bootstrap CDN sin SRI (Fase 1 — V-007)

Los 11 listados en el informe; referencia de hash en `index.html`.

### Fallback `empresa_id` / valor 8 (no tocar en v1.0 — V-003)

`dashboard.html`, `reportes.html`, `modificar-proveedor.html`, `implementacion.html`, `gestion-proveedores.html`, `gestion-controles.html`, `gestion-riesgos.html`, `matriz-riesgos.html`, `capacitacion.html`, `auditoria.html`, `anadir-proveedor.html`.

---

## 7. Criterios de aceptación del plan completo v1.0

El plan se considera **ejecutado con éxito** cuando:

1. **Semgrep** reporta **0** hallazgos en la regla de integridad CDN (V-007 cerrado).  
2. **Gitleaks** sigue en 0.  
3. Existe **una** `getAccessToken()` en `auth.js` (V-014 cerrado).  
4. Los **5 archivos** de error de V-005 no usan `innerHTML` con `error.message` sin escapar.  
5. **Todos** los `fetch` del inventario P0-2 hacia API propia incluyen `authHeaders()` cuando el usuario tiene sesión (V-006 mitigado en front).  
6. **Prioridad 1** de V-004 aplicada con `escapeHtml` en `utils.js`.  
7. Prueba manual mínima (§5, Fases 1–3) documentada con fecha en `env-verificacion.txt` o nota breve al pie del informe.  
8. **Informe de vulnerabilidades** actualizado a v1.1 con tabla “antes/después” y hallazgos cerrados.

---

## 8. Orden de trabajo recomendado (resumen)

```text
Fase 0  →  inventario + línea base Semgrep
Fase 1  →  auth.js + SRI + errores seguros     [Semgrep 11 → 0]
Fase 2  →  authHeaders + utils.js + todos fetch
Fase 3  →  escapeHtml en pantallas prioritarias
Fase 4  →  (opcional) refresh_token solo si no se usa
```

**No iniciar Fase 3 antes de Fase 2** (conviene tener `utils.js` y `auth.js` estables).

---

## 9. Riesgos de regresión y mitigación

| Riesgo | Probabilidad | Mitigación en el plan |
|--------|--------------|------------------------|
| API rechaza petición con header nuevo | Baja | Si falla, revisar en DevTools; no cambiar URL ni body |
| Escape rompe HTML legítimo | Baja | Solo escapar **texto** insertado, no estructura estática de plantilla |
| SRI incorrecto y Bootstrap no carga | Baja | Copiar hash exacto de `index.html` (misma versión 5.3.8) |
| Quitar `empresa_id = 8` deja demo vacía | Alta si se hiciera | **Excluido** de v1.0 |

---

## 10. Entregables tras la ejecución (cuando se apruebe)

| Entregable | Ubicación |
|------------|-----------|
| Código mitigado | `Control-PrecISO-main/` |
| Plan (este documento) | `security-analysis/PLAN_REMEDIACION.md` |
| Informe actualizado | `security-analysis/INFORME_VULNERABILIDADES.md` v1.1 |
| Evidencia Semgrep/Gitleaks | `security-analysis/semgrep-report.json`, `gitleaks-report.json` |
| HTML imprimible del informe | Regenerar con `_build_informe_print_html.py` |

---

## 11. Siguiente versión del plan (futuro, no v1.0)

Para cuando haya coordinación con el equipo o acceso a AWS:

- V-003: eliminar fallback `8` y obligar `getEmpresaId()` o mensaje de error.  
- V-001: diseño de sesión con cookies `HttpOnly` o BFF.  
- V-002 / V-006: validación en API Gateway (authorizer JWT).  
- V-009: CSP gradual (report-only primero).

---

**Fin del plan de remediación — versión 1.0**

**Estado:** ejecutado el 20 de mayo de 2026. Ver `INFORME_EJECUCION_REMEDIACION_v2.md` e `INFORME_VULNERABILIDADES.md` v2.0.

**Versión HTML:** `PLAN_REMEDIACION_print.html` (generar con `python _build_informe_print_html.py`).
