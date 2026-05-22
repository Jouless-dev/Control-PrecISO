"""Genera HTML formal listo para imprimir a PDF (A4) desde INFORME_FINAL.md."""
from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent

DOC_META: dict[str, dict[str, str]] = {
    "INFORME_FINAL.md": {
        "tipo": "INFORME FINAL",
        "subtitulo": "Análisis SAST Semgrep — escaneo, tratamiento y cierre (11/11 erradicadas)",
        "clasificacion": "Documento académico — Gestión de vulnerabilidades",
        "proyecto": "Control-PrecISO",
    },
}

CSS = """
:root {
  --ink: #1c2833;
  --muted: #5d6d7e;
  --accent: #1a5276;
  --border: #d5d8dc;
  --bg: #fafbfc;
}
* { box-sizing: border-box; }
body {
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.55;
  color: var(--ink);
  margin: 0;
  background: #fff;
}
.cover {
  page-break-after: always;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 3cm 2.5cm;
  border-bottom: 4px solid var(--accent);
}
.cover .tipo { font-size: 10pt; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); font-weight: 600; }
.cover h1 { font-size: 22pt; font-weight: 700; margin: 0.6em 0 0.3em; line-height: 1.25; color: var(--ink); border: none; }
.cover .subtitulo { font-size: 13pt; color: var(--muted); margin-bottom: 2em; }
.cover-meta { width: 100%; border-collapse: collapse; font-size: 10.5pt; margin-top: 1.5em; }
.cover-meta td { padding: 0.45em 0.75em; border: 1px solid var(--border); vertical-align: top; }
.cover-meta td:first-child { width: 32%; font-weight: 600; background: var(--bg); color: var(--accent); }
.content { max-width: 18cm; margin: 0 auto; padding: 1.5cm 2cm 2cm; }
.content h1 { font-size: 16pt; color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 0.25em; margin-top: 1.8em; page-break-after: avoid; }
.content h2 { font-size: 13pt; color: var(--ink); margin-top: 1.4em; page-break-after: avoid; }
.content h3 { font-size: 11.5pt; margin-top: 1.1em; }
.content p { text-align: justify; margin: 0.65em 0; }
.content table { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin: 1em 0; page-break-inside: avoid; }
.content th, .content td { border: 1px solid var(--border); padding: 0.4em 0.55em; text-align: left; vertical-align: top; }
.content th { background: var(--accent); color: #fff; font-weight: 600; }
.content tr:nth-child(even) { background: var(--bg); }
.content code { font-size: 9pt; background: #eef2f5; padding: 0.1em 0.35em; border-radius: 3px; }
.content pre { background: #f4f6f7; border: 1px solid var(--border); padding: 0.75em 1em; font-size: 8.5pt; overflow-x: auto; page-break-inside: avoid; }
.content ul, .content ol { margin: 0.5em 0; padding-left: 1.4em; }
.content blockquote { border-left: 4px solid var(--accent); margin: 1em 0; padding: 0.5em 1em; background: var(--bg); color: var(--muted); }
.content hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }
.footer-note { margin-top: 3em; padding-top: 1em; border-top: 1px solid var(--border); font-size: 9pt; color: var(--muted); text-align: center; }
@media print {
  body { background: #fff; }
  .cover { min-height: auto; padding: 2cm; }
  .content { padding: 0; max-width: none; }
  .content h1 { page-break-before: auto; }
  a { color: var(--ink); text-decoration: none; }
}
"""

def _extract_cover_parts(raw_html: str) -> tuple[str | None, str | None, str]:
    h1_match = re.search(r"<h1[^>]*>.*?</h1>", raw_html, re.DOTALL | re.IGNORECASE)
    h1_html = h1_match.group(0) if h1_match else None
    rest = raw_html[h1_match.end() :] if h1_match else raw_html
    table_match = re.search(
        r"<table[^>]*>.*?</table>\s*",
        rest,
        re.DOTALL | re.IGNORECASE,
    )
    table_html = table_match.group(0) if table_match else None
    body = rest[table_match.end() :] if table_match else rest
    if table_html:
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
    clasificacion = meta.get("clasificacion", "")
    proyecto = meta.get("proyecto", "Control-PrecISO")
    fecha = "Mayo 2026"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title}</title>
  <style>{CSS}</style>
</head>
<body>
  <section class="cover">
    <div class="tipo">{tipo}</div>
    <h1>{title_text}</h1>
    <div class="subtitulo">{subtitulo}</div>
    {table_html or ""}
    <table class="cover-meta">
      <tr><td>Proyecto</td><td>{proyecto}</td></tr>
      <tr><td>Clasificación</td><td>{clasificacion}</td></tr>
      <tr><td>Fecha</td><td>{fecha}</td></tr>
    </table>
  </section>
  <div class="content">
    {body_html}
    <p class="footer-note">Control-PrecISO — Informe generado desde {md_file}</p>
  </div>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    p = build_print_html(
        "INFORME_FINAL.md",
        "INFORME_FINAL_print.html",
        "Informe final de vulnerabilidades — Control-PrecISO",
    )
    print(f"OK -> {p}")
