"""Genera HTML formal listo para imprimir a PDF (A4) desde Markdown en esta carpeta."""
from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent

DOC_META: dict[str, dict[str, str]] = {
    "INFORME_VULNERABILIDADES_FINAL.md": {
        "tipo": "INFORME FINAL DE CIERRE",
        "subtitulo": "SAST Semgrep — 11 hallazgos erradicados, 0 abiertos",
        "clasificacion": "Documento académico — Gestión de vulnerabilidades",
        "proyecto": "Control-PrecISO",
    },
    "informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP.md": {
        "tipo": "INFORME DE ESCANEO",
        "subtitulo": "Línea base SAST — 11 hallazgos (SG-001 a SG-011)",
        "clasificacion": "Documento académico — Identificación",
        "proyecto": "Control-PrecISO",
    },
    "PLAN_REMEDIACION.md": {
        "tipo": "PLAN DE TRATAMIENTO",
        "subtitulo": "Remediación de hallazgos Semgrep (SRI — 11 archivos HTML)",
        "clasificacion": "Documento académico — Gestión de vulnerabilidades",
        "proyecto": "Control-PrecISO",
    },
    "INFORME_EJECUCION_REMEDIACION_v2.md": {
        "tipo": "INFORME DE EJECUCIÓN",
        "subtitulo": "Cierre de remediación — 11/11 hallazgos erradicados",
        "clasificacion": "Documento académico — Verificación SAST",
        "proyecto": "Control-PrecISO",
    },
}

CSS = """
:root {
  --ink: #1c2833;
  --muted: #5d6d7e;
  --accent: #1a5276;
  --accent-light: #d4e6f1;
  --border: #bdc3c7;
  --paper: #ffffff;
  --bg: #eceff1;
}
* { box-sizing: border-box; }
html { font-size: 11pt; }
body {
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  line-height: 1.5;
  color: var(--ink);
  background: var(--bg);
  margin: 0;
}
.screen-toolbar {
  max-width: 210mm;
  margin: 10px auto 0;
  padding: 8px 14px;
  font-size: 9pt;
  color: var(--muted);
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: 2px;
}
.screen-toolbar kbd {
  font-family: inherit;
  padding: 1px 5px;
  border: 1px solid var(--border);
  border-radius: 2px;
  background: #f8f9fa;
}
.document {
  max-width: 210mm;
  margin: 10px auto 32px;
  background: var(--paper);
  box-shadow: 0 2px 12px rgba(0,0,0,.12);
}
.doc-cover {
  padding: 22mm 20mm 18mm;
  border-bottom: 3px solid var(--accent);
  page-break-after: always;
}
.doc-cover .org-line {
  font-size: 9pt;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 6mm;
}
.doc-cover .doc-type {
  display: inline-block;
  font-size: 9pt;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-light);
  padding: 4px 10px;
  margin-bottom: 8mm;
}
.doc-cover .doc-project {
  font-size: 22pt;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 4mm;
  line-height: 1.15;
}
.doc-cover .doc-subtitle {
  font-size: 13pt;
  font-weight: 400;
  color: var(--ink);
  margin: 0 0 12mm;
  line-height: 1.35;
}
.doc-cover table.meta-table {
  width: 100%;
  font-size: 10pt;
  border-collapse: collapse;
  margin: 0 0 14mm;
}
.doc-cover table.meta-table td {
  border: 1px solid var(--border);
  padding: 8px 12px;
  vertical-align: top;
}
.doc-cover table.meta-table td:first-child {
  width: 32%;
  font-weight: 600;
  background: #f4f6f7;
  color: var(--accent);
}
.doc-cover .classification {
  font-size: 9pt;
  color: var(--muted);
  border-top: 1px solid var(--border);
  padding-top: 6mm;
  margin: 0;
}
.doc-body {
  padding: 14mm 18mm 18mm;
}
.doc-body > h1:first-child { display: none; }
.doc-body > table:first-of-type { display: none; }
.doc-body > hr:first-of-type { display: none; }
.doc-body h2 {
  font-size: 12.5pt;
  font-weight: 700;
  color: var(--accent);
  margin: 1.4em 0 0.6em;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--accent-light);
  page-break-after: avoid;
}
.doc-body h2::before {
  content: "";
  display: inline-block;
  width: 4px;
  height: 1em;
  background: var(--accent);
  margin-right: 8px;
  vertical-align: -2px;
}
.doc-body h3 {
  font-size: 11pt;
  font-weight: 600;
  color: var(--ink);
  margin: 1.1em 0 0.4em;
  page-break-after: avoid;
}
.doc-body h4 {
  font-size: 10.5pt;
  font-weight: 600;
  margin: 0.9em 0 0.35em;
}
.doc-body p { margin: 0.45em 0 0.65em; text-align: justify; }
.doc-body li { margin: 0.2em 0; }
.doc-body ul, .doc-body ol { margin: 0.4em 0 0.8em; padding-left: 1.4em; }
.doc-body table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8.5pt;
  margin: 0.8em 0 1em;
}
.doc-body thead th {
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  text-align: left;
}
.doc-body th, .doc-body td {
  border: 1px solid var(--border);
  padding: 6px 8px;
  vertical-align: top;
}
.doc-body tr:nth-child(even) td { background: #fafbfc; }
.doc-body code {
  font-family: Consolas, "Cascadia Mono", monospace;
  font-size: 0.9em;
  background: #f4f6f7;
  padding: 1px 5px;
  border: 1px solid #e5e8e8;
  border-radius: 2px;
}
.doc-body pre {
  background: #f8f9fa;
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  padding: 10px 14px;
  font-size: 8pt;
  line-height: 1.4;
  page-break-inside: avoid;
  white-space: pre-wrap;
}
.doc-body pre code { border: none; background: none; padding: 0; }
.doc-body hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.5em 0;
}
.doc-body blockquote, .doc-body em.note {
  font-size: 10pt;
  color: var(--muted);
}
.doc-body strong { color: var(--ink); }
.doc-print-footer {
  margin-top: 14mm;
  padding-top: 4mm;
  border-top: 1px solid var(--border);
  font-size: 8pt;
  color: var(--muted);
  text-align: center;
}
@media print {
  body { background: #fff; }
  .screen-only { display: none !important; }
  .document { box-shadow: none; margin: 0; max-width: none; }
  .doc-cover { padding-top: 15mm; }
  .doc-body { padding: 0; }
  @page {
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
  }
  @page :first { margin-top: 12mm; }
}
"""


def _extract_cover_parts(html: str) -> tuple[str | None, str | None, str]:
    """Obtiene h1, primera tabla y cuerpo sin portada duplicada."""
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    table_match = re.search(r"<table[^>]*>.*?</table>", html, re.DOTALL | re.IGNORECASE)
    h1_html = h1_match.group(0) if h1_match else None
    table_html = table_match.group(0) if table_match else None
    body = html
    if h1_match:
        body = body[h1_match.end() :]
    if table_match:
        # tabla puede estar después del h1 en el fragmento restante
        tm = re.search(r"<table[^>]*>.*?</table>", body, re.DOTALL | re.IGNORECASE)
        if tm:
            body = body[: tm.start()] + body[tm.end() :]
    body = re.sub(r"^\s*<hr\s*/?>\s*", "", body, count=1, flags=re.IGNORECASE)
    if table_html:
        table_html = re.sub(
            r"<table(?![^>]*class=)",
            '<table class="meta-table"',
            table_html,
            count=1,
        )
        # Tablas markdown con cabecera vacía (| | |)
        table_html = re.sub(
            r"<thead>\s*<tr>\s*(?:<th>\s*</th>\s*)+</tr>\s*</thead>",
            "",
            table_html,
            flags=re.IGNORECASE,
        )
    return h1_html, table_html, body.strip()


def _h1_text(h1_html: str | None, fallback: str) -> str:
    if not h1_html:
        return fallback
    text = re.sub(r"<[^>]+>", "", h1_html)
    return re.sub(r"\s+", " ", text).strip()


def build_print_html(md_file: str, html_file: str, page_title: str) -> Path:
    md_path = ROOT / md_file
    out_path = ROOT / html_file
    meta = DOC_META.get(md_file, {})
    raw_html = markdown.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    h1_html, table_html, body_html = _extract_cover_parts(raw_html)
    title_text = _h1_text(h1_html, page_title.split("—")[0].strip())
    tipo = meta.get("tipo", "DOCUMENTO TÉCNICO")
    subtitulo = meta.get("subtitulo", "")
    clasificacion = meta.get("clasificacion", "Uso académico")
    proyecto = meta.get("proyecto", "Control-PrecISO")

    cover_table = table_html or ""
    cover_section = f"""
    <header class="doc-cover">
      <p class="org-line">Seguridad de la información · Evaluación de vulnerabilidades</p>
      <div class="doc-type">{tipo}</div>
      <h1 class="doc-project">{proyecto}</h1>
      <p class="doc-subtitle">{subtitulo or title_text}</p>
      {cover_table}
      <p class="classification">{clasificacion}</p>
    </header>
"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <style>{CSS}</style>
</head>
<body>
  <p class="screen-toolbar screen-only">
    Exportar a PDF: <kbd>Ctrl+P</kbd> → <strong>Guardar como PDF</strong> · Formato A4 · Márgenes predeterminados
  </p>
  <div class="document">
    {cover_section}
    <main class="doc-body">
      {body_html}
      <footer class="doc-print-footer">
        {proyecto} — {tipo} — Versión según metadatos del documento
      </footer>
    </main>
  </div>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    docs = [
        (
            "informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP.md",
            "informes-historicos/INFORME_ESCANEO_INICIAL_SEMGREP_print.html",
            "Informe de escaneo inicial SAST — Control-PrecISO",
        ),
        (
            "INFORME_VULNERABILIDADES_FINAL.md",
            "INFORME_VULNERABILIDADES_FINAL_print.html",
            "Informe final de cierre de vulnerabilidades — Control-PrecISO",
        ),
        (
            "PLAN_REMEDIACION.md",
            "PLAN_REMEDIACION_print.html",
            "Plan de remediación de vulnerabilidades — Control-PrecISO",
        ),
        (
            "INFORME_EJECUCION_REMEDIACION_v2.md",
            "INFORME_EJECUCION_REMEDIACION_v2_print.html",
            "Informe de ejecución del plan de remediación — Control-PrecISO",
        ),
    ]
    for md_file, html_file, title in docs:
        p = build_print_html(md_file, html_file, title)
        print(f"OK -> {p}")
