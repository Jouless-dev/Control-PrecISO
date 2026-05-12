# INFORME DE ANÁLISIS DE VULNERABILIDADES

**Proyecto:** Control-PrecISO (aplicación web SGSI / ISO 27001)  
**Alcance del análisis:** Código fuente versionado en el repositorio (rama `main`), sin despliegue activo ni pruebas de penetración dinámicas.  
**Fecha del informe:** 12 de mayo de 2026  
**Clasificación del documento:** Técnico / uso académico y de cumplimiento interno  
**Restricción:** No se modificó código de la aplicación; únicamente evidencias en `security-analysis/`.

---

## 1. Resumen ejecutivo

Se realizó un análisis de seguridad de aplicaciones combinando **SAST (Semgrep)**, **detección de secretos (Gitleaks)**, **análisis de dependencias (OWASP Dependency-Check 12.2.2)** y **revisión manual** orientada a OWASP Top 10:2021 e ISO/IEC 27001:2022.

**Stack detectado:** aplicación **estática** basada en **HTML5, JavaScript (vanilla), CSS**, integración con **Amazon Cognito** y múltiples **API Gateway** (REST). No existe `package.json` en la raíz del código analizado; las dependencias de terceros aparecen principalmente como **CDN (Bootstrap)** en HTML y como **artefactos empaquetados** (`mysql2-layer.zip`, `control-preciso.zip`) analizados parcialmente por Dependency-Check.

**Hallazgos agregados (prioridad de negocio):**

| Severidad (informe) | Cantidad aproximada | Comentario breve |
|----------------------|---------------------|-------------------|
| Crítica | 1 | Tokens de sesión (incl. refresh) en `localStorage` → robo vía XSS o malware de extensión. |
| Alta | 4 | Control de acceso basado solo en cliente, `empresa_id` manipulable, patrones XSS por `innerHTML`, APIs llamadas sin credenciales visibles en algunas vistas admin. |
| Media | 5 | CDN sin SRI (11 coincidencias Semgrep), `USER_PASSWORD_AUTH`, exposición de superficie AWS, errores reflejados al DOM, ausencia de CSP. |
| Baja / Informativa | 4 | IDs públicos de Cognito, URLs de API enumerables, Dependency-Check sin CVE en JSON de esta ejecución, Gitleaks sin fugas, calidad de código menor. |

**Herramientas y entorno:** ver `security-analysis/env-verificacion.txt`. Python, pip, Node.js y Java estaban disponibles; Semgrep se usó desde la instalación existente (`semgrep` v1.162.x); Gitleaks v8.30.1 se instaló vía `winget`; OWASP Dependency-Check se descargó en `security-analysis/dependency-check-tool/`.

**Remediación inmediata recomendada (antes de exposición amplia o producción):**

1. Sustituir almacenamiento de **refresh token** (y preferiblemente todos los tokens) fuera de `localStorage` (cookies `HttpOnly` + SameSite, flujo PKCE con almacenamiento efímero, o BFF).  
2. Garantizar **autorización en servidor** para `empresa_id` y recursos multi-tenant (no confiar en valores de `localStorage` o query string).  
3. Eliminar o sustituir **innerHTML** con datos remotos por APIs seguras (`textContent`, plantillas escapadas, DOMPurify si aplica).  
4. Añadir **SRI** (`integrity` + `crossorigin`) en recursos CDN o alojar dependencias con control de integridad.  
5. Revisar endpoints llamados **sin cabecera `Authorization`** en vistas sensibles; asumir que el backend debe validar siempre identidad y permisos.

---

## 2. Metodología utilizada

### 2.1 Semgrep (SAST)

- Comando: `semgrep scan --config auto --config p/owasp-top-ten` sobre el repositorio, excluyendo `security-analysis/` y `dependency-check-tool/`.  
- Evidencia: `security-analysis/semgrep-report.json`, `security-analysis/semgrep-report.txt`.  
- **Limitación:** el análisis quedó acotado a archivos **rastreados por Git**; archivos &gt; 1 MB (p. ej. algunos ZIP) fueron omitidos por política de Semgrep.  
- **Nota de parseo:** Semgrep registró advertencia de parseo parcial en `registro.html` (posible conflicto con caracteres especiales en regex de validación de contraseña); no invalida el resto del escaneo pero reduce cobertura en ese archivo.

### 2.2 Gitleaks (secret scanning)

- Comando: `gitleaks detect --source . --report-path security-analysis/gitleaks-report.json --report-format json`.  
- Resultado: **0 hallazgos** en el historial analizado (array vacío).  
- **Limitación:** no analiza secretos solo presentes en working copy no commiteados; tampoco sustituye revisión de secretos en backends no incluidos en el repo.

### 2.3 OWASP Dependency-Check

- CLI 12.2.2; escaneo de la carpeta `Control-PrecISO-main/`.  
- **Primera ejecución:** fallo de actualización NVD por **HTTP 429** (límite de tasa sin API key).  
- **Segunda ejecución:** ` --noupdate` completó el análisis usando datos locales ya descargados parcialmente.  
- Evidencia: `security-analysis/dependency-check-report.html`, `security-analysis/dependency-check-report.json`.  
- El JSON listó **135 dependencias** identificadas (incluye extracción parcial de contenidos dentro de ZIPs / lockfiles temporales); **no se observaron entradas `CVE-*` en el JSON exportado** en esta corrida (no equivale a “cero riesgo”, sino a ausencia de coincidencias CVE en la base efectivamente consultada).

### 2.4 Revisión manual

- Inspección dirigida de `js/auth.js`, `js/config.js`, páginas HTML con `fetch`, `localStorage` e `innerHTML`.  
- Mapeo a OWASP Top 10:2021, CWE e controles ISO 27001:2022 (Anexo A) donde aplica.

---

## 3. Stack tecnológico detectado

| Componente | Evidencia |
|------------|-----------|
| Frontend | Múltiples `.html`, `styles.css`, JS embebido y `js/*.js`. |
| Autenticación | Amazon Cognito (`cognito-idp.*.amazonaws.com`), flujo `InitiateAuth` / `USER_PASSWORD_AUTH`. |
| Backend consumido | Varios `execute-api.us-east-1.amazonaws.com` (API Gateway). |
| Datos embebidos | `controles-iso.json`, hojas de cálculo bajo `documentos/`. |
| CI | `.gitlab-ci.yml` (no ampliado en este informe). |
| Gestor de paquetes (app principal) | **No** hay `package.json` en la raíz del módulo web; dependencias de librerías aparecen vía CDN y ZIPs. |

**Herramientas verificadas (instalación):** Python 3.14.x, pip 26.x, Node.js v22.x, OpenJDK 25.x — detalle en `env-verificacion.txt`.

---

## 4. Vulnerabilidades encontradas

### 4.1 Tabla maestra

| ID | Vulnerabilidad | Severidad | Riesgo | OWASP Top 10:2021 | Archivo(s) afectado(s) | Evidencia | CWE | ISO 27001:2022 (referencia orientativa) |
|----|----------------|-----------|--------|-------------------|-------------------------|-----------|-----|----------------------------------------|
| V-001 | Tokens Cognito (`access_token`, `id_token`, **`refresh_token`**) almacenados en `localStorage` | Crítica | Alto | A07 – Identification and Authentication Failures | `Control-PrecISO-main/js/auth.js` | `security-analysis/semgrep-report.json` (contexto general); revisión manual auth | CWE-522, CWE-923 | A.5.16, A.5.17, A.8.26 |
| V-002 | Control de acceso basado en **decodificación JWT en cliente** (`atob`, claims `cognito:groups`) sin enforcement visible en front | Alta | Alto | A01 – Broken Access Control | `Control-PrecISO-main/js/auth.js`, `dashboard.html`, múltiples vistas | Manual + Semgrep limitado a patrones | CWE-602, CWE-639 | A.5.15, A.5.16, A.8.3 |
| V-003 | **Multi-tenant frágil:** `empresa_id` desde `localStorage` con **fallback fijo (8)**; posible IDOR si el API confía en el parámetro | Alta | Alto | A01 – Broken Access Control | `dashboard.html`, `reportes.html`, `gestion-proveedores.html`, etc. | Manual | CWE-639, CWE-284 | A.5.15, A.8.3 |
| V-004 | **DOM XSS / XSS almacenado** potencial: `innerHTML` con interpolación de datos de API **sin escape** en múltiples pantallas | Alta | Alto | A03 – Injection | `gestion-riesgos.html`, `gestion-proveedores.html`, `admin-empresas.html`, … | Manual (grep `innerHTML`) | CWE-79 | A.5.23, A.8.28 |
| V-005 | Reflejo de **`error.message`** en `innerHTML` (XSS de segundo orden si el error contiene HTML/markup malicioso) | Media | Medio | A03 – Injection | `superadmin-reportes.html`, `superadmin-controles.html`, `matriz-riesgos.html`, … | Manual | CWE-79 | A.8.28 |
| V-006 | Peticiones a **APIs sensibles sin cabecera `Authorization`** en vistas de reporting superadmin | Alta | Medio–Alto | A01 / A05 | `superadmin-reportes.html` | Manual | CWE-306, CWE-639 | A.5.15, A.8.3 |
| V-007 | **CDN (Bootstrap) sin `integrity` (SRI)** — integridad de cadena de suministro / XSS por CDN comprometido | Media (Semgrep: WARNING) | Medio | A08 – Software and Data Integrity Failures | 11 archivos HTML (p. ej. `login.html`, `dashboard.html`, …) | `semgrep-report.json` regla `html.security.audit.missing-integrity.*` | CWE-353 | A.5.9, A.5.23, A.8.31 |
| V-008 | **Superficie de ataque expuesta:** `userPoolId`, `clientId`, múltiples URLs de API Gateway en código legible | Media | Medio | A05 – Security Misconfiguration | `js/config.js`, múltiples `.html` | Manual | CWE-200, CWE-668 | A.5.9, A.5.19 |
| V-009 | **Ausencia de CSP** y otras cabeceras HTTP de endurecimiento (aplicación estática servida típicamente sin políticas) | Media | Medio | A05 – Security Misconfiguration | Global (HTML servido) | Manual | CWE-693 | A.5.14, A.8.12 |
| V-010 | Uso de **`USER_PASSWORD_AUTH`** desde SPA (superficie de fuerza bruta / phishing / ausencia de MFA a nivel app) | Media | Medio | A07 – Identification and Authentication Failures | `js/auth.js`, `registro.html`, `confirmar.html` | Manual | CWE-287, CWE-307 | A.5.17 |
| V-011 | **MFA/2FA no implementado** en el flujo observado (dependencia exclusiva de políticas Cognito) | Baja | Bajo | A07 | Front + Cognito | Manual | — | A.5.17 |
| V-012 | **Análisis de dependencias:** 135 dependencias rastreadas; **0 CVE** en el JSON exportado en esta ejecución (base NVD incompleta / 429) | Informativa | Bajo | A06 – Vulnerable and Outdated Components | ZIPs / lockfiles extraídos | `dependency-check-report.json` | — | A.5.19, A.8.8, A.8.26 |
| V-013 | **Secretos en Git:** Gitleaks sin coincidencias | Informativa | Bajo | A07 / buena práctica | Repositorio | `gitleaks-report.json` (`[]`) | — | A.5.34, A.8.12 |
| V-014 | **Duplicación de función** `getAccessToken()` en `auth.js` (mantenimiento / riesgo de lógica divergente) | Baja | Bajo | A04 – Insecure Design (calidad) | `js/auth.js` | Manual | CWE-1041 | A.5.23 |

### 4.2 Fragmentos representativos y descripción técnica

#### V-001 — Tokens en `localStorage` (Crítica / Riesgo alto)

Tras autenticación exitosa se persisten **tres tokens** en `localStorage`. Cualquier script XSS en el origen (o extensión maliciosa) puede leerlos y suplantar la sesión, en particular el **refresh token** que permite renovación prolongada.

```42:46:d:\Universidad\Proyecto de seguridad\Control-PrecISO-main\Control-PrecISO-main\js\auth.js
        // Guardar el token en localStorage
        localStorage.setItem('access_token', data.AuthenticationResult.AccessToken);
        localStorage.setItem('id_token', data.AuthenticationResult.IdToken);
        localStorage.setItem('refresh_token', data.AuthenticationResult.RefreshToken);
        localStorage.setItem('user_email', email);
```

- **Probabilidad:** Alta si existe cualquier vector XSS o compromiso del mismo origen.  
- **Impacto:** Alto (secuestro de cuenta, acceso a datos de empresa, escalada si el token contiene grupos privilegiados).

#### V-003 — `empresa_id` con valor por defecto (Alta / Riesgo alto)

Si el backend usa `empresa_id` enviado por el cliente sin validación estricta contra el token, un usuario podría manipular datos de otra organización (IDOR).

```25:38:d:\Universidad\Proyecto de seguridad\Control-PrecISO-main\Control-PrecISO-main\dashboard.html
    async function cargarEmpresaId() {
        try {
            const empresaId = await getEmpresaId();
            if (empresaId) {
                localStorage.setItem('empresa_id', empresaId);
                console.log('Empresa ID cargado:', empresaId);
            } else {
                console.log('No se pudo obtener empresa_id, usando valor por defecto');
                localStorage.setItem('empresa_id', 8);
            }
        } catch (error) {
            console.error('Error en cargarEmpresaId:', error);
            localStorage.setItem('empresa_id', 8);
        }
    }
```

#### V-004 — `innerHTML` con datos remotos sin escape (Alta / Riesgo alto)

Ejemplo: opciones construidas concatenando `nombre` y `codigo` desde la API directamente en HTML.

```249:253:d:\Universidad\Proyecto de seguridad\Control-PrecISO-main\Control-PrecISO-main\gestion-riesgos.html
                    const select = document.getElementById('amenaza_id');
                    select.innerHTML = '<option value="">Seleccionar Amenaza</option>';
                    result.data.forEach(a => {
                        select.innerHTML += `<option value="${a.id}">${a.codigo} - ${a.nombre}</option>`;
                    });
```

- **Riesgo:** Si la API devuelve cadenas con HTML/JS malicioso (por datos corruptos o cuenta comprometida), se ejecuta en el contexto del usuario.

#### V-006 — API sin `Authorization` en vista superadmin (Alta / Riesgo medio–alto)

```80:83:d:\Universidad\Proyecto de seguridad\Control-PrecISO-main\Control-PrecISO-main\superadmin-reportes.html
        async function cargarReportes() {
            try {
                const response = await fetch(API_EMPRESAS);
                const data = await response.json();
```

- **Riesgo:** Depende del endurecimiento del API Gateway (IAM, Cognito authorizer, WAF). Si el endpoint es público, hay **exposición de listado de empresas** y metadatos de cumplimiento.

#### V-007 — CDN sin SRI (Media / Riesgo medio) — hallazgo automático

Semgrep (`html.security.audit.missing-integrity.missing-integrity`) reportó **11 ocurrencias** en etiquetas `<link>` o `<script>` a `cdn.jsdelivr.net` sin atributo `integrity`. Consolidado como un único riesgo de cadena de suministro / integridad.

Ejemplo (`dashboard.html`):

```4:8:d:\Universidad\Proyecto de seguridad\Control-PrecISO-main\Control-PrecISO-main\dashboard.html
    <script src="js/config.js"></script>
    <script src="js/auth.js"></script>
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
```

#### V-010 — `USER_PASSWORD_AUTH` (Media / Riesgo medio)

```14:20:d:\Universidad\Proyecto de seguridad\Control-PrecISO-main\Control-PrecISO-main\js\auth.js
            body: JSON.stringify({
                AuthFlow: 'USER_PASSWORD_AUTH',
                ClientId: COGNITO_CONFIG.clientId,
                AuthParameters: {
                    USERNAME: email,
                    PASSWORD: password
                }
            })
```

- **Riesgo:** Incrementa superficie de ataques de credenciales en cliente; debe compensarse con MFA obligatorio, políticas de contraseña, riesgo de bots, y consideración de flujos Hosted UI / PKCE.

---

## 5. Priorización de remediación

### 5.1 Riesgo alto (acción inmediata)

| ID | Acción correctiva orientativa |
|----|-------------------------------|
| V-001 | Migrar tokens a modelo **BFF** o cookies **HttpOnly** + **Secure** + **SameSite**; acortar vida del refresh; considerar revocación y rotación. |
| V-002, V-003 | **Autorización server-side** obligatoria: derivar `empresa_id` y roles del token verificado en backend; eliminar fallbacks numéricos en cliente. |
| V-004, V-005 | Sustituir `innerHTML` por construcción segura o sanitizar con biblioteca mantenida; nunca interpolar errores crudos. |
| V-006 | Añadir **authorizer** (Cognito/JWT) a API Gateway o validación Lambda; enviar siempre `Authorization` desde cliente y **rechazar** sin token. |

### 5.2 Riesgo medio

| ID | Acción correctiva orientativa |
|----|-------------------------------|
| V-007 | Añadir **SRI** y `crossorigin` a CDN o servir Bootstrap desde origen propio con hashing. |
| V-008 | Mover configuración no secreta a build-time/env; endurecer CORS y rate limiting en API; minimizar datos en respuestas. |
| V-009 | Definir **CSP**, `X-Frame-Options`/`frame-ancestors`, `Referrer-Policy`, `Permissions-Policy` en el servidor de estáticos. |
| V-010 | Habilitar **MFA** en Cognito; valorar flujo **SRP** / Hosted UI según documentación AWS actual. |

### 5.3 Riesgo bajo / informativo

| ID | Acción |
|----|--------|
| V-011 | Política organizacional MFA + concienciación. |
| V-012 | Registrar **NVD API key** y repetir Dependency-Check; añadir `package.json` explícito si se adopta npm. |
| V-013 | Mantener Gitleaks en CI en cada push. |
| V-014 | Unificar helpers de token; pruebas unitarias en módulo auth. |

---

## 6. Conclusión de seguridad

La aplicación presenta un **nivel de madurez de seguridad típico de un MVP front-end** con integración directa a Cognito y APIs públicas: funcionalmente operativa, pero con **riesgos elevados en autenticación/sesión (A07)**, **control de acceso multi-tenant (A01)** y **superficie XSS (A03)**, más **debilidades de integridad de cadena de suministro en CDN (A08)**.

**Nivel estimado de exposición:** **Alto** frente a un atacante con capacidad de ejecutar JavaScript en el origen (XSS) o de invocar APIs mal configuradas; **Medio** frente a un adversario solo remoto sin XSS, dependiendo del endurecimiento real del API Gateway (no observable solo desde el front estático).

**Fortalezas observadas:** uso de Cognito en lugar de password propio; en algunas pantallas uso de `escapeHtml` (buen patrón, no homogéneo); Gitleaks sin fugas en el historial Git analizado.

**Recomendación académica / SGSI:** documentar este informe como **evidencia de evaluación de vulnerabilidades** (ciclo PDCA / tratamiento de riesgos ISO 27001) y planificar remediación, prueba de regresión y **nueva corrida de herramientas** tras cambios.

---

## Anexo A — Ubicación de evidencias

| Artefacto | Ruta |
|-----------|------|
| Informe (este documento) | `security-analysis/INFORME_VULNERABILIDADES.md` |
| Semgrep JSON | `security-analysis/semgrep-report.json` |
| Semgrep TXT | `security-analysis/semgrep-report.txt` |
| Gitleaks JSON | `security-analysis/gitleaks-report.json` |
| Dependency-Check HTML | `security-analysis/dependency-check-report.html` |
| Dependency-Check JSON | `security-analysis/dependency-check-report.json` |
| Verificación de entorno | `security-analysis/env-verificacion.txt` |
| CLI Dependency-Check (descargado) | `security-analysis/dependency-check-tool/` |
| ZIP de distribución ODC | `security-analysis/dependency-check-dist.zip` |

---

## Anexo B — Conteo por severidad (informe propio)

| Severidad | Cantidad (IDs V-001…V-014) |
|-----------|----------------------------|
| Crítica | 1 |
| Alta | 4 |
| Media | 5 |
| Baja | 2 |
| Informativa | 2 |

**Hallazgos automáticos Semgrep:** 11 coincidencias de la misma familia de reglas (consolidadas en **V-007** en la tabla maestra).

---

*Fin del informe.*
