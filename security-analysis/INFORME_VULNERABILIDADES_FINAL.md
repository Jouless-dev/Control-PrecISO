# INFORME FINAL DE ANÁLISIS DE VULNERABILIDADES

| | |
|---|---|
| **Proyecto** | Control-PrecISO (aplicación web SGSI / ISO 27001) |
| **Versión del informe** | **FINAL** (integra remediación, verificación y despliegue Docker) |
| **Fecha** | 20 de mayo de 2026 |
| **Alcance** | Código front-end, evidencias SAST/secrets, despliegue local containerizado |
| **Referencias** | Informe v1.0, Plan y ejecución de remediación, `DOCKER_SETUP.md` |

---

## 1. Resumen ejecutivo

Se completó el ciclo de seguridad **identificar → planificar → remediar → verificar → desplegar**:

| Fase | Resultado |
|------|-----------|
| **Línea base (v1.0)** | 11 hallazgos Semgrep + 13 hallazgos manuales (V-001…V-014) |
| **Remediación** | Plan v1.0 ejecutado en front-end (sin cambiar AWS) |
| **Verificación SAST** | Semgrep **0** hallazgos, Gitleaks **0** fugas (corrida final 22:04) |
| **Despliegue local** | Docker + nginx en `http://localhost:8080` |

### Conclusión en una frase

**Semgrep pasó de 11 a 0 porque se corrigió un único tipo de problema repetido 11 veces (CDN sin SRI); no porque desaparecieron todas las vulnerabilidades del informe manual.** Tras los controles del front-end, **4 hallazgos quedaron cerrados, 3 mitigados y 6 siguen abiertos o parciales**. El riesgo global bajó en el cliente, pero **permanece medio–alto** por sesión en `localStorage` y controles solo en navegador.

---

## 2. Aclaración obligatoria: ¿Por qué 11 → 0 en Semgrep?

Esta es la pregunta central para entender el informe con lógica académica.

### 2.1 Dos “universos” de hallazgos distintos

| Fuente | ¿Qué cuenta? | v1.0 | FINAL |
|--------|----------------|------|-------|
| **Semgrep** (automático) | Coincidencias de reglas en el código escaneado | **11** | **0** |
| **Informe manual** (OWASP / revisión) | Riesgos de diseño y malas prácticas (V-001…V-014) | **13 IDs** | **Ver §5** |

**No son lo mismo.** En v1.0, los 11 de Semgrep **no eran 11 vulnerabilidades diferentes**.

### 2.2 Los 11 de Semgrep = una sola regla, once archivos

Todos los avisos iniciales correspondían a la **misma regla**: recurso Bootstrap cargado desde CDN **sin atributo `integrity`** (Subresource Integrity, SRI).

| Dato | Valor |
|------|-------|
| Regla / tipo | CDN sin verificación de integridad |
| ID en informe manual | **V-007** (un solo hallazgo de diseño) |
| Repeticiones en código | **11 archivos HTML** |
| Lo que reporta Semgrep | 1 problema × 11 archivos = **11 líneas en el reporte** |

**Controles que eliminaron los 11 avisos:** Fase 1 del plan — añadir `integrity` y `crossorigin="anonymous"` al `<link>` de Bootstrap en cada HTML afectado.

Por eso, al re-ejecutar Semgrep tras la remediación, el resultado es **0**: la regla ya no encuentra coincidencias. **Eso solo demuestra el cierre de V-007 en la herramienta automática**, no el cierre del inventario manual completo.

### 2.3 Lo que Semgrep NO detectó (y por eso 0 ≠ “sin riesgo”)

En v1.0, Semgrep **no generó avisos** para, entre otros:

- Tokens en `localStorage` (**V-001**)
- APIs sin cabecera `Authorization` (**V-006**)
- XSS por `innerHTML` con datos de API (**V-004**)
- `empresa_id` por defecto (**V-003**)
- Autorización solo en cliente (**V-002**)

Esos ítems salieron de **revisión manual** alineada a OWASP Top 10. El plan v1.0 atendió varios de ellos con cambios de código que **las reglas Semgrep usadas no modelan** o no alcanzaron a marcar.

### 2.4 Diagrama lógico

```text
INFORME v1.0
├── Semgrep: 11  ──►  Todos = V-007 (SRI) en 11 HTML
│                      └── Control: integrity en Bootstrap  ──►  Semgrep FINAL: 0
│
└── Manual: 13 IDs (V-001…V-014)
       ├── Cerrados con controles front-end: V-005, V-007, V-014, V-013
       ├── Mitigados: V-004, V-006, V-001 (parcial)
       └── Abiertos / sin cambio: V-001 residual, V-002, V-003, V-008…V-011
```

---

## 3. Ciclo del proyecto y documentación (orden lógico)

| Orden | Documento | Rol en el ciclo |
|-------|-----------|-----------------|
| 1 | `informes-historicos/INFORME_VULNERABILIDADES_v1.0.md` | **Identificación** — estado inicial |
| 2 | `PLAN_REMEDIACION.md` | **Planificación** — qué se va a corregir y qué no |
| 3 | `INFORME_EJECUCION_REMEDIACION_v2.md` | **Implementación** — qué se hizo en código |
| 4 | `VERIFICACION_REMEDIACION_v1.md` | **Verificación técnica** — Semgrep/Gitleaks |
| 5 | **`INFORME_VULNERABILIDADES_FINAL.md` (este)** | **Cierre** — síntesis, matriz control–riesgo, Docker |
| — | `INDICE_INFORMES.md` | Índice maestro de la carpeta |

**Despliegue (entorno local):** `docker-compose.yml`, `serve-docker.ps1`, `DOCKER_SETUP.md` en la raíz del repositorio.

---

## 4. Matriz de controles aplicados → vulnerabilidades

Cada control del plan se relaciona con uno o más IDs. Los que **no** tienen control en código siguen abiertos.

| Control implementado | Archivos / artefacto | Vulnerabilidad | Efecto |
|---------------------|----------------------|----------------|--------|
| SRI en Bootstrap CDN | 11+ HTML | **V-007** | **Cerrado** — elimina los 11 avisos Semgrep |
| `showLoadError()` | 5 HTML | **V-005** | **Cerrado** — errores sin `innerHTML` peligroso |
| Una sola `getAccessToken()` | `js/auth.js` | **V-014** | **Cerrado** |
| `apiFetch` + `authHeaders` | `js/auth.js`, 18+ HTML | **V-006** | **Mitigado** — token en APIs propias |
| `escapeHtml` centralizado | `js/utils.js`, pantallas P1/P2 | **V-004** | **Mitigado** — XSS reducido en listados |
| No guardar `refresh_token` | `js/auth.js` | **V-001** | **Parcial** — menor exposición de sesión |
| Sin cambio en Cognito/URLs | — | **V-008, V-010, V-011** | **Abierto** |
| Sin validación servidor | — | **V-002, V-003** | **Abierto** |
| Sin CSP | — | **V-009** | **Abierto** |
| Gitleaks en CI/local | `gitleaks-report.json` | **V-013** | **Cerrado** (0 fugas) |
| **Docker + nginx** | `Dockerfile`, `docker-compose.yml` | **Riesgo operativo** | **Mejora** — ver §6 |

---

## 5. Estado final de cada hallazgo (informe manual)

| ID | Problema | Gravedad | Estado FINAL | Relación con Semgrep 11→0 |
|----|----------|----------|--------------|---------------------------|
| V-001 | Tokens en `localStorage` | Crítica | **Parcial** | No medido por Semgrep |
| V-002 | Rol solo en cliente | Alta | **Abierto** | No medido por Semgrep |
| V-003 | `empresa_id = 8` por defecto | Alta | **Abierto** | No medido por Semgrep |
| V-004 | XSS / `innerHTML` | Alta | **Mitigado** | No medido por Semgrep |
| V-005 | Errores en DOM | Media | **Cerrado** | No medido por Semgrep |
| V-006 | APIs sin `Authorization` | Alta | **Mitigado** | No medido por Semgrep |
| V-007 | CDN sin SRI | Media | **Cerrado** | **Único origen de los 11 avisos** → 0 tras SRI |
| V-008 | Config expuesta | Media | **Abierto** | No medido por Semgrep |
| V-009 | Sin CSP | Media | **Abierto** | No medido por Semgrep |
| V-010 | Login contraseña en SPA | Media | **Abierto** | No medido por Semgrep |
| V-011 | Sin 2FA en UI | Baja | **Abierto** | No medido por Semgrep |
| V-013 | Secretos en Git | Info | **Cerrado** | Gitleaks 0 (independiente de Semgrep) |
| V-014 | Código duplicado auth | Baja | **Cerrado** | No medido por Semgrep |

### Resumen numérico honesto

| Concepto | Cantidad |
|----------|----------|
| Hallazgos manuales inventariados | 13 IDs |
| **Cerrados** | 4 (V-005, V-007, V-014, V-013) |
| **Mitigados** | 3 (V-004, V-006, V-001 parcial) |
| **Abiertos o parciales** | 6+ (V-001 residual, V-002, V-003, V-008–V-011) |
| Avisos Semgrep v1.0 | 11 (todos V-007) |
| Avisos Semgrep FINAL | **0** |

---

## 6. Despliegue local con Docker (control de entorno)

No sustituye los controles de código, pero **cierra el requisito de alojamiento local** documentado para el proyecto.

| Elemento | Descripción |
|----------|-------------|
| Imagen | `nginx:alpine` sirviendo `Control-PrecISO-main/` |
| Orquestación | `docker compose up` — puerto **8080** |
| Evidencia en SAST | Semgrep FINAL escaneó también el `Dockerfile` (42 archivos Git) — **0 hallazgos** |
| Arquitectura | Front en contenedor local; **Cognito y API Gateway siguen en AWS** |

**Beneficio de seguridad operativa:** entorno reproducible, sin depender de abrir archivos `file://`, y superficie de servicio acotada a nginx estático.

---

## 7. Metodología de la verificación FINAL

| Paso | Herramienta / acción | Resultado (20-may-2026, 22:04) |
|------|----------------------|--------------------------------|
| 1 | Código remediado según plan v1.0 | Ver `INFORME_EJECUCION_REMEDIACION_v2.md` |
| 2 | `semgrep scan` (auto + OWASP) | **0** hallazgos, 42 archivos, 260 reglas |
| 3 | `gitleaks detect` | **0** fugas |
| 4 | Revisión manual + matriz §4 | Estados en §5 |
| 5 | Despliegue Docker verificado | Contenedor `control-preciso-web` |

Evidencias: `semgrep-report.json`, `gitleaks-report.json`, `env-verificacion.txt`.

---

## 8. Conclusión de seguridad FINAL

| Criterio | Valoración |
|----------|------------|
| ¿Se entiende el 11→0? | Sí: **11 repeticiones de V-007**, corregidas con SRI |
| ¿Quedó el sistema sin riesgo? | **No** — persisten V-001 (parcial), V-002, V-003 y otros |
| ¿Mejoró el front-end? | **Sí** — token en APIs, menos XSS, SRI, higiene auth |
| ¿Cumple ciclo SGSI / ISO 27001 académico? | **Sí** — evidencia de tratamiento de riesgos y verificación |
| ¿Listo para producción? | **No** sin backend, CSP y sesión fuera de `localStorage` |

---

## 9. Evidencias y archivos

| Artefacto | Ubicación |
|-----------|-----------|
| Informe FINAL (este) | `INFORME_VULNERABILIDADES_FINAL.md` |
| HTML imprimible | `INFORME_VULNERABILIDADES_FINAL_print.html` |
| Línea base v1.0 | `informes-historicos/INFORME_VULNERABILIDADES_v1.0.md` |
| Post-remediación v2.0 | `informes-historicos/INFORME_VULNERABILIDADES_v2.0.md` |
| Índice | `INDICE_INFORMES.md` |

---

**Fin del informe — versión FINAL**
