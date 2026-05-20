# INFORME DE AN├üLISIS DE VULNERABILIDADES

| | |
|---|---|
| **Proyecto** | Control-PrecISO (aplicaci├│n web SGSI / ISO 27001) |
| **Versi├│n del informe** | 1.0 |
| **Fecha** | 20 de mayo de 2026 |
| **Tipo de an├ílisis** | Est├ítico (c├│digo fuente), sin pruebas de intrusi├│n en servidor |

---

## 1. Resumen

### ┬┐Qu├® se analiz├│?

El **front-end** de la aplicaci├│n: p├íginas HTML, JavaScript y estilos en la carpeta `Control-PrecISO-main/`. La app inicia sesi├│n con **Amazon Cognito** y obtiene datos de **APIs en AWS**. No se revis├│ la configuraci├│n de la nube ni el backend fuera de este c├│digo.

### ┬┐Cu├íl es la conclusi├│n general?

La aplicaci├│n **funciona**, pero presenta **riesgos de seguridad importantes** t├¡picos de un prototipo web:

- La sesi├│n queda guardada en el navegador de forma que un atacante con XSS podr├¡a **robarla**.
- Qui├®n puede ver qu├® depende mucho del **navegador**, no solo del servidor.
- Los datos que vienen de las APIs se muestran a veces de forma **insegura** (riesgo de XSS).
- Casi las peticiones a las APIs **no env├¡an el token** de acceso.

**Buenas noticias:** no se encontraron contrase├▒as ni claves subidas al control de versiones (Gitleaks). Semgrep detect├│ **11 problemas** del mismo tipo: falta de verificaci├│n de integridad en Bootstrap cargado desde internet.

### Hallazgos por gravedad

| Gravedad | Cantidad | Significado breve |
|----------|----------|-------------------|
| Cr├¡tica | 1 | Robo de sesi├│n posible |
| Alta | 4 | Acceso indebido, XSS o APIs sin proteger en el cliente |
| Media | 5 | Configuraci├│n d├®bil, CDN, errores mostrados en pantalla |
| Baja | 2 | Mejoras de dise├▒o y MFA no visible |
| Positivo | 1 | Sin secretos filtrados en Git |

### Qu├® corregir primero

1. Dejar de guardar el **token de renovaci├│n** en `localStorage`.
2. Enviar el **token en todas las llamadas** a las APIs.
3. Quitar el **empresa_id = 8** por defecto y validar la empresa en el servidor.
4. Dejar de usar `innerHTML` con datos del servidor; usar escape o `textContent`.
5. A├▒adir **integridad (SRI)** al Bootstrap del CDN en las p├íginas que faltan.

---

## 2. C├│mo se realiz├│ el an├ílisis

| Paso | Herramienta / m├®todo | Resultado |
|------|----------------------|-----------|
| 1 | **Semgrep** (reglas autom├íticas + OWASP) | 11 avisos |
| 2 | **Gitleaks** (b├║squeda de secretos en Git) | 0 fugas |
| 3 | **Revisi├│n manual** del c├│digo | 13 hallazgos documentados |

**Referencia:** OWASP Top 10 (2021) para clasificar los riesgos.

**L├¡mites del an├ílisis:** no se prob├│ la app en ejecuci├│n ni la consola de AWS. Algunos archivos ZIP grandes no los analiz├│ Semgrep. En `registro.html` el an├ílisis autom├ítico fue parcial por un car├ícter especial en una expresi├│n regular.

---

## 3. La aplicaci├│n en pocas palabras

| Elemento | Descripci├│n |
|----------|-------------|
| Tecnolog├¡a | HTML, CSS y JavaScript (sin framework) |
| Login | Amazon Cognito |
| Datos | Varios servicios en API Gateway |
| Interfaz | Bootstrap desde CDN (jsDelivr) |

---

## 4. Hallazgos de seguridad

### Tabla resumen

| ID | Problema | Gravedad | ┬┐Qu├® puede pasar? |
|----|----------|----------|-------------------|
| **V-001** | Tokens de sesi├│n en `localStorage` | Cr├¡tica | Si hay XSS, roban la cuenta y renuevan la sesi├│n |
| **V-002** | Permisos y rol solo revisados en el navegador | Alta | Un usuario podr├¡a intentar ver pantallas de otro rol |
| **V-003** | ID de empresa por defecto = **8** y editable en el navegador | Alta | Ver o modificar datos de otra empresa (si el API no valida) |
| **V-004** | Datos de APIs insertados con `innerHTML` sin filtrar | Alta | XSS: ejecutar c├│digo malicioso en el navegador de la v├¡ctima |
| **V-005** | Mensajes de error mostrados como HTML sin filtrar | Media | XSS secundario v├¡a texto de error manipulado |
| **V-006** | Llamadas a APIs sin cabecera de autorizaci├│n | Alta | Acceso a datos sin demostrar qui├®n es el usuario |
| **V-007** | Bootstrap del CDN sin atributo `integrity` | Media | Si el CDN se compromete, podr├¡an inyectar c├│digo |
| **V-008** | IDs de Cognito y URLs de APIs visibles en el c├│digo | Media | Facilita el reconocimiento del atacante |
| **V-009** | Sin pol├¡tica de seguridad de contenido (CSP) | Media | Un XSS es m├ís dif├¡cil de contener |
| **V-010** | Login con usuario/contrase├▒a directo desde la web | Media | M├ís exposici├│n a phishing y fuerza bruta |
| **V-011** | No hay doble factor (2FA) en la interfaz | Baja | Depende solo de la configuraci├│n de Cognito |
| **V-014** | Funci├│n duplicada en `auth.js` | Baja | Confusi├│n al mantener el c├│digo |

*Nota: V-006 agrupa las vistas de superadmin y el resto de pantallas donde el `fetch` no env├¡a token.*

---

### Explicaci├│n de cada hallazgo

#### V-001 ÔÇö Sesi├│n guardada en el navegador (Cr├¡tica)

**En palabras simples:** al iniciar sesi├│n, la aplicaci├│n guarda tres ÔÇ£llavesÔÇØ (tokens) dentro del navegador, incluida la que sirve para **renovar** la sesi├│n sin volver a poner la contrase├▒a.

**Riesgo:** si alguien consigue ejecutar JavaScript falso en la p├ígina (XSS), puede copiar esas llaves y usar la cuenta de la v├¡ctima.

**D├│nde:** `js/auth.js`, l├¡neas donde se hace `localStorage.setItem` para `access_token`, `id_token` y `refresh_token`.

---

#### V-002 ÔÇö Qui├®n es el usuario se decide en el navegador (Alta)

**En palabras simples:** la app lee el token en el cliente para saber si hay sesi├│n y qu├® rol tiene (Superadmin, AdminEmpresa, etc.) y muestra u oculta men├║s. Eso **no basta** si el servidor no comprueba lo mismo.

**D├│nde:** `js/auth.js` (`getUserRole`, `isAuthenticated`) y p├íginas como `dashboard.html`.

---

#### V-003 ÔÇö Identificador de empresa manipulable (Alta)

**En palabras simples:** muchas pantallas usan un n├║mero de empresa guardado en el navegador. Si no existe, usan **8** como valor fijo. En el dashboard, si la API no responde, tambi├®n se guarda **8**.

**Riesgo:** un atacante podr├¡a cambiar ese n├║mero y pedir datos de otra organizaci├│n, si el backend no valida.

**D├│nde (ejemplos):** `dashboard.html`, `reportes.html`, `gestion-proveedores.html`, `gestion-controles.html`, y otras vistas de gesti├│n.

---

#### V-004 ÔÇö Mostrar datos de la API como HTML sin filtrar (Alta)

**En palabras simples:** nombres de proveedores, riesgos, empresas, etc. se pegan en la p├ígina con `innerHTML`. Si un dato contiene c├│digo HTML o script, el navegador podr├¡a ejecutarlo.

**Excepci├│n parcial:** algunas pantallas (`gestion-riesgos`, `matriz-riesgos`, `vulnerabilidades`, `superadmin-controles-proveedores`) s├¡ usan una funci├│n `escapeHtml`.

**Ejemplo claro:** en `gestion-proveedores.html`, el nombre del proveedor se inserta directo en la plantilla HTML.

---

#### V-005 ÔÇö Errores mostrados como HTML (Media)

**En palabras simples:** cuando falla una petici├│n, el mensaje de error se escribe en la p├ígina con `innerHTML`. Un mensaje malicioso podr├¡a incluir etiquetas HTML.

**D├│nde:** `superadmin-reportes.html`, `superadmin-controles.html`, `matriz-riesgos.html`, `admin-empresas.html` y similares.

---

#### V-006 ÔÇö APIs llamadas sin token (Alta)

**En palabras simples:** la mayor├¡a de las peticiones `fetch` a las APIs de negocio **no incluyen** `Authorization: Bearer ÔÇª`. Solo hay token visible en `getEmpresaId()` (`auth.js`) y en un caso de `registro.html`.

**Riesgo:** si en AWS las APIs est├ín abiertas o solo miran el par├ímetro `empresa_id`, cualquiera podr├¡a leer o cambiar datos.

**D├│nde:** destacan `superadmin-reportes.html` y `superadmin-controles.html`, pero el patr├│n se repite en reportes, proveedores, auditor├¡a, etc.

---

#### V-007 ÔÇö Librer├¡a Bootstrap sin comprobar integridad (Media)

**En palabras simples:** en 11 p├íginas se carga Bootstrap desde internet sin el atributo `integrity` que comprueba que el archivo no fue alterado. Semgrep lo report├│ 11 veces. Solo `index.html` lo hace bien.

**P├íginas afectadas:** entre otras, `login.html`, `dashboard.html`, `registro.html`, `admin-empresas.html`.

---

#### V-008 ÔÇö Datos de configuraci├│n visibles (Media)

**En palabras simples:** en el c├│digo aparecen el ID del User Pool de Cognito, el Client ID y varias URLs de API. No son secretos igual que una contrase├▒a, pero **aumentan la informaci├│n** que tiene un atacante.

**D├│nde:** `js/config.js` y varios HTML.

---

#### V-009 ÔÇö Sin pol├¡tica CSP (Media)

**En palabras simples:** no hay cabecera ni metaetiqueta que limite de d├│nde puede cargarse script o estilo. Eso agrava el impacto de un posible XSS.

---

#### V-010 ÔÇö Contrase├▒a enviada desde la web al login (Media)

**En palabras simples:** el formulario manda usuario y contrase├▒a con el flujo `USER_PASSWORD_AUTH` directo a Cognito. Es habitual en prototipos, pero exige buenas pol├¡ticas de contrase├▒a y rate limiting en Cognito.

**D├│nde:** `js/auth.js`.

---

#### V-011 ÔÇö Sin segundo factor en la app (Baja)

**En palabras simples:** en las pantallas revisadas no aparece un paso de verificaci├│n en dos pasos; todo depende de c├│mo est├® configurado Cognito en la nube.

---

#### V-014 ÔÇö C├│digo duplicado en autenticaci├│n (Baja)

**En palabras simples:** la funci├│n `getAccessToken()` est├í definida dos veces en `auth.js`. La segunda reemplaza a la primera y puede generar errores al mantener el proyecto.

---

## 5. Resultado de herramientas autom├íticas

| Herramienta | Resultado |
|-------------|-----------|
| **Semgrep** | 11 hallazgos: Bootstrap CDN sin SRI (lista en V-007) |
| **Gitleaks** | Ning├║n secreto detectado en el historial Git revisado |

Los detalles t├®cnicos completos est├ín en `semgrep-report.json` y `gitleaks-report.json` dentro de esta misma carpeta.

---

## 6. Conclusi├│n

Control-PrecISO es adecuada como **proyecto acad├®mico y demostraci├│n**, pero **no cumple pr├ícticas m├¡nimas para un entorno productivo** en manejo de sesi├│n, llamadas a API y prevenci├│n de XSS.

| Aspecto | Valoraci├│n |
|---------|------------|
| Riesgo global | **Alto** si existiera XSS o APIs sin validaci├│n en servidor |
| Punto fuerte | Uso de Cognito; sin fugas de secretos en Git; algo de escape HTML en m├│dulos de riesgos |
| Uso del informe | Evidencia de la fase de **identificaci├│n de vulnerabilidades** en un SGSI |

Tras aplicar correcciones, conviene **volver a ejecutar** Semgrep y Gitleaks y actualizar este informe.

---

**Fin del informe ÔÇö versi├│n 1.0**
