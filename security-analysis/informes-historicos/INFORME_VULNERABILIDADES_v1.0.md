# INFORME DE ANÁLISIS DE VULNERABILIDADES

| | |
|---|---|
| **Proyecto** | Control-PrecISO (aplicación web SGSI / ISO 27001) |
| **Versión del informe** | 1.0 |
| **Fecha** | 20 de mayo de 2026 |
| **Tipo de análisis** | Estático (código fuente), sin pruebas de intrusión en servidor |

---

## 1. Resumen

### ¿Qué se analizó?

El **front-end** de la aplicación: páginas HTML, JavaScript y estilos en la carpeta `Control-PrecISO-main/`. La app inicia sesión con **Amazon Cognito** y obtiene datos de **APIs en AWS**. No se revisó la configuración de la nube ni el backend fuera de este código.

### ¿Cuál es la conclusión general?

La aplicación **funciona**, pero presenta **riesgos de seguridad importantes** típicos de un prototipo web:

- La sesión queda guardada en el navegador de forma que un atacante con XSS podría **robarla**.
- Quién puede ver qué depende mucho del **navegador**, no solo del servidor.
- Los datos que vienen de las APIs se muestran a veces de forma **insegura** (riesgo de XSS).
- Casi las peticiones a las APIs **no envían el token** de acceso.

**Buenas noticias:** no se encontraron contraseñas ni claves subidas al control de versiones (Gitleaks). Semgrep detectó **11 problemas** del mismo tipo: falta de verificación de integridad en Bootstrap cargado desde internet.

### Hallazgos por gravedad

| Gravedad | Cantidad | Significado breve |
|----------|----------|-------------------|
| Crítica | 1 | Robo de sesión posible |
| Alta | 4 | Acceso indebido, XSS o APIs sin proteger en el cliente |
| Media | 5 | Configuración débil, CDN, errores mostrados en pantalla |
| Baja | 2 | Mejoras de diseño y MFA no visible |
| Positivo | 1 | Sin secretos filtrados en Git |

### Qué corregir primero

1. Dejar de guardar el **token de renovación** en `localStorage`.
2. Enviar el **token en todas las llamadas** a las APIs.
3. Quitar el **empresa_id = 8** por defecto y validar la empresa en el servidor.
4. Dejar de usar `innerHTML` con datos del servidor; usar escape o `textContent`.
5. Añadir **integridad (SRI)** al Bootstrap del CDN en las páginas que faltan.

---

## 2. Cómo se realizó el análisis

| Paso | Herramienta / método | Resultado |
|------|----------------------|-----------|
| 1 | **Semgrep** (reglas automáticas + OWASP) | 11 avisos |
| 2 | **Gitleaks** (búsqueda de secretos en Git) | 0 fugas |
| 3 | **Revisión manual** del código | 13 hallazgos documentados |

**Referencia:** OWASP Top 10 (2021) para clasificar los riesgos.

**Límites del análisis:** no se probó la app en ejecución ni la consola de AWS. Algunos archivos ZIP grandes no los analizó Semgrep. En `registro.html` el análisis automático fue parcial por un carácter especial en una expresión regular.

---

## 3. La aplicación en pocas palabras

| Elemento | Descripción |
|----------|-------------|
| Tecnología | HTML, CSS y JavaScript (sin framework) |
| Login | Amazon Cognito |
| Datos | Varios servicios en API Gateway |
| Interfaz | Bootstrap desde CDN (jsDelivr) |

---

## 4. Hallazgos de seguridad

### Tabla resumen

| ID | Problema | Gravedad | ¿Qué puede pasar? |
|----|----------|----------|-------------------|
| **V-001** | Tokens de sesión en `localStorage` | Crítica | Si hay XSS, roban la cuenta y renuevan la sesión |
| **V-002** | Permisos y rol solo revisados en el navegador | Alta | Un usuario podría intentar ver pantallas de otro rol |
| **V-003** | ID de empresa por defecto = **8** y editable en el navegador | Alta | Ver o modificar datos de otra empresa (si el API no valida) |
| **V-004** | Datos de APIs insertados con `innerHTML` sin filtrar | Alta | XSS: ejecutar código malicioso en el navegador de la víctima |
| **V-005** | Mensajes de error mostrados como HTML sin filtrar | Media | XSS secundario vía texto de error manipulado |
| **V-006** | Llamadas a APIs sin cabecera de autorización | Alta | Acceso a datos sin demostrar quién es el usuario |
| **V-007** | Bootstrap del CDN sin atributo `integrity` | Media | Si el CDN se compromete, podrían inyectar código |
| **V-008** | IDs de Cognito y URLs de APIs visibles en el código | Media | Facilita el reconocimiento del atacante |
| **V-009** | Sin política de seguridad de contenido (CSP) | Media | Un XSS es más difícil de contener |
| **V-010** | Login con usuario/contraseña directo desde la web | Media | Más exposición a phishing y fuerza bruta |
| **V-011** | No hay doble factor (2FA) en la interfaz | Baja | Depende solo de la configuración de Cognito |
| **V-014** | Función duplicada en `auth.js` | Baja | Confusión al mantener el código |

*Nota: V-006 agrupa las vistas de superadmin y el resto de pantallas donde el `fetch` no envía token.*

---

### Explicación de cada hallazgo

#### V-001 — Sesión guardada en el navegador (Crítica)

**En palabras simples:** al iniciar sesión, la aplicación guarda tres “llaves” (tokens) dentro del navegador, incluida la que sirve para **renovar** la sesión sin volver a poner la contraseña.

**Riesgo:** si alguien consigue ejecutar JavaScript falso en la página (XSS), puede copiar esas llaves y usar la cuenta de la víctima.

**Dónde:** `js/auth.js`, líneas donde se hace `localStorage.setItem` para `access_token`, `id_token` y `refresh_token`.

---

#### V-002 — Quién es el usuario se decide en el navegador (Alta)

**En palabras simples:** la app lee el token en el cliente para saber si hay sesión y qué rol tiene (Superadmin, AdminEmpresa, etc.) y muestra u oculta menús. Eso **no basta** si el servidor no comprueba lo mismo.

**Dónde:** `js/auth.js` (`getUserRole`, `isAuthenticated`) y páginas como `dashboard.html`.

---

#### V-003 — Identificador de empresa manipulable (Alta)

**En palabras simples:** muchas pantallas usan un número de empresa guardado en el navegador. Si no existe, usan **8** como valor fijo. En el dashboard, si la API no responde, también se guarda **8**.

**Riesgo:** un atacante podría cambiar ese número y pedir datos de otra organización, si el backend no valida.

**Dónde (ejemplos):** `dashboard.html`, `reportes.html`, `gestion-proveedores.html`, `gestion-controles.html`, y otras vistas de gestión.

---

#### V-004 — Mostrar datos de la API como HTML sin filtrar (Alta)

**En palabras simples:** nombres de proveedores, riesgos, empresas, etc. se pegan en la página con `innerHTML`. Si un dato contiene código HTML o script, el navegador podría ejecutarlo.

**Excepción parcial:** algunas pantallas (`gestion-riesgos`, `matriz-riesgos`, `vulnerabilidades`, `superadmin-controles-proveedores`) sí usan una función `escapeHtml`.

**Ejemplo claro:** en `gestion-proveedores.html`, el nombre del proveedor se inserta directo en la plantilla HTML.

---

#### V-005 — Errores mostrados como HTML (Media)

**En palabras simples:** cuando falla una petición, el mensaje de error se escribe en la página con `innerHTML`. Un mensaje malicioso podría incluir etiquetas HTML.

**Dónde:** `superadmin-reportes.html`, `superadmin-controles.html`, `matriz-riesgos.html`, `admin-empresas.html` y similares.

---

#### V-006 — APIs llamadas sin token (Alta)

**En palabras simples:** la mayoría de las peticiones `fetch` a las APIs de negocio **no incluyen** `Authorization: Bearer …`. Solo hay token visible en `getEmpresaId()` (`auth.js`) y en un caso de `registro.html`.

**Riesgo:** si en AWS las APIs están abiertas o solo miran el parámetro `empresa_id`, cualquiera podría leer o cambiar datos.

**Dónde:** destacan `superadmin-reportes.html` y `superadmin-controles.html`, pero el patrón se repite en reportes, proveedores, auditoría, etc.

---

#### V-007 — Librería Bootstrap sin comprobar integridad (Media)

**En palabras simples:** en 11 páginas se carga Bootstrap desde internet sin el atributo `integrity` que comprueba que el archivo no fue alterado. Semgrep lo reportó 11 veces. Solo `index.html` lo hace bien.

**Páginas afectadas:** entre otras, `login.html`, `dashboard.html`, `registro.html`, `admin-empresas.html`.

---

#### V-008 — Datos de configuración visibles (Media)

**En palabras simples:** en el código aparecen el ID del User Pool de Cognito, el Client ID y varias URLs de API. No son secretos igual que una contraseña, pero **aumentan la información** que tiene un atacante.

**Dónde:** `js/config.js` y varios HTML.

---

#### V-009 — Sin política CSP (Media)

**En palabras simples:** no hay cabecera ni metaetiqueta que limite de dónde puede cargarse script o estilo. Eso agrava el impacto de un posible XSS.

---

#### V-010 — Contraseña enviada desde la web al login (Media)

**En palabras simples:** el formulario manda usuario y contraseña con el flujo `USER_PASSWORD_AUTH` directo a Cognito. Es habitual en prototipos, pero exige buenas políticas de contraseña y rate limiting en Cognito.

**Dónde:** `js/auth.js`.

---

#### V-011 — Sin segundo factor en la app (Baja)

**En palabras simples:** en las pantallas revisadas no aparece un paso de verificación en dos pasos; todo depende de cómo esté configurado Cognito en la nube.

---

#### V-014 — Código duplicado en autenticación (Baja)

**En palabras simples:** la función `getAccessToken()` está definida dos veces en `auth.js`. La segunda reemplaza a la primera y puede generar errores al mantener el proyecto.

---

## 5. Resultado de herramientas automáticas

| Herramienta | Resultado |
|-------------|-----------|
| **Semgrep** | 11 hallazgos: Bootstrap CDN sin SRI (lista en V-007) |
| **Gitleaks** | Ningún secreto detectado en el historial Git revisado |

Los detalles técnicos completos están en `semgrep-report.json` y `gitleaks-report.json` dentro de esta misma carpeta.

---

## 6. Conclusión

Control-PrecISO es adecuada como **proyecto académico y demostración**, pero **no cumple prácticas mínimas para un entorno productivo** en manejo de sesión, llamadas a API y prevención de XSS.

| Aspecto | Valoración |
|---------|------------|
| Riesgo global | **Alto** si existiera XSS o APIs sin validación en servidor |
| Punto fuerte | Uso de Cognito; sin fugas de secretos en Git; algo de escape HTML en módulos de riesgos |
| Uso del informe | Evidencia de la fase de **identificación de vulnerabilidades** en un SGSI |

Tras aplicar correcciones, conviene **volver a ejecutar** Semgrep y Gitleaks y actualizar este informe.

---

**Fin del informe — versión 1.0**
