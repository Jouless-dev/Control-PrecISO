# Guía: análisis de vulnerabilidades, mitigación y Git (Control-PrecISO)

Esta guía es para el miembro del equipo que trabaja **solo en seguridad** (informes, Semgrep, mitigaciones en código) mientras el resto mantiene el proyecto desplegado.

---

## 1. Herramientas ya instaladas en tu PC (Windows)

| Herramienta | Versión aprox. | Para qué |
|-------------|----------------|----------|
| **Git** | 2.54+ | Clonar, ramas, subir cambios |
| **Python 3.12** | 3.12.10 | Semgrep, scripts de informes |
| **Semgrep** | 1.163+ | SAST (HTML/JS, OWASP) |
| **Gitleaks** | 8.30.1 | Secretos en historial Git |
| **Java (Temurin 17)** | 17.0.19 | OWASP Dependency-Check (opcional) |

**Importante:** cierra y vuelve a abrir PowerShell o Cursor después de instalar, para que `git`, `python`, `semgrep` y `gitleaks` estén en el PATH.

Comprueba:

```powershell
git --version
python --version
semgrep --version
gitleaks version
java -version
```

---

## 2. Tu repositorio (entrega al equipo)

**Repositorio propio (seguridad y mitigaciones):**  
https://github.com/Jouless-dev/Control-PrecISO

Tus compañeros pueden clonar o descargar ZIP desde GitHub e integrar en su GitLab/repo principal:

```powershell
git clone https://github.com/Jouless-dev/Control-PrecISO.git
```

### Subir cambios a tu GitHub

```powershell
cd "D:\Universidad\Control-PrecISO-main"
git remote add origin https://github.com/Jouless-dev/Control-PrecISO.git
# Si ya existe origin: git remote set-url origin https://github.com/Jouless-dev/Control-PrecISO.git
git add .
git commit -m "Seguridad: informes, reportes Semgrep/Gitleaks y scripts de análisis"
git branch -M main
git push -u origin main
```

La primera vez GitHub pedirá iniciar sesión (navegador o token personal).

---

## 3. Flujo de trabajo diario

### 3.1 Crear rama (no trabajes en `main` directo)

```powershell
cd "D:\Universidad\Control-PrecISO-main"
git checkout -b feature/remediacion-seguridad
```

### 3.2 Ejecutar análisis automático

```powershell
.\security-analysis\run-security-scan.ps1
```

Actualiza:

- `security-analysis/semgrep-report.json` / `.txt`
- `security-analysis/gitleaks-report.json`
- `security-analysis/env-verificacion.txt`

### 3.3 Mitigar vulnerabilidades

Sigue el orden del plan:

- `security-analysis/PLAN_REMEDIACION.md`
- Hallazgos: `security-analysis/INFORME_VULNERABILIDADES.md`

Tras cada bloque de cambios, vuelve a ejecutar `run-security-scan.ps1` y anota en el informe la fecha de la nueva corrida.

### 3.4 Regenerar PDF del plan (opcional)

```powershell
cd security-analysis
python _build_informe_print_html.py
.\generar_pdf_PLAN_REMEDIACION.ps1
```

### 3.5 Subir al repositorio

```powershell
cd "D:\Universidad\Control-PrecISO-main"
git status
git add Control-PrecISO-main/ security-analysis/
git add -u
git commit -m "Seguridad: mitigación V-00X y reportes Semgrep/Gitleaks actualizados"
git push -u origin feature/remediacion-seguridad
```

Luego abre un **Merge Request / Pull Request** hacia `main` para que el equipo revise.

**No subas:** `dependency-check-tool/`, `dependency-check-dist.zip` (están en `.gitignore` de `security-analysis/`).

---

## 4. OWASP Dependency-Check (opcional)

Solo si necesitas actualizar `dependency-check-report.json`:

1. Descarga el ZIP desde [releases de Dependency-Check](https://github.com/jeremylong/Dependency-Check/releases).
2. Descomprime en `security-analysis/dependency-check-tool/`.
3. Ejecuta el `.bat` apuntando a `Control-PrecISO-main/`.

Si NVD devuelve error 429, solicita API key en https://nvd.nist.gov/developers/request-an-api-key o usa `--noupdate` con datos ya descargados.

---

## 5. Qué entregar al equipo

| Entregable | Archivo |
|------------|---------|
| Informe | `security-analysis/INFORME_VULNERABILIDADES.md` |
| Plan de remediación | `security-analysis/PLAN_REMEDIACION.md` |
| Evidencia Semgrep | `semgrep-report.json`, `semgrep-report.txt` |
| Evidencia Gitleaks | `gitleaks-report.json` |
| Código mitigado | `Control-PrecISO-main/` (HTML, `js/auth.js`, etc.) |

---

## 6. Problemas frecuentes

| Problema | Solución |
|----------|----------|
| `git` no reconocido | Reinicia terminal; reinstala Git con winget |
| `semgrep` no reconocido | `python -m pip install semgrep` y reinicia terminal |
| Semgrep no escanea archivos | Debe existir `.git` y archivos en `git add` |
| `python` abre Microsoft Store | Desactiva alias: Configuración → Aplicaciones → Alias de ejecución → desactiva `python.exe` |
| Push rechazado | `git pull origin main` primero, resuelve conflictos, vuelve a push |

---

## 7. Contacto con el equipo

Antes del primer push confirma:

1. URL exacta del repositorio  
2. Rama base (`main` / `master`)  
3. Si usan GitLab: usuario y token o SSH configurado  
