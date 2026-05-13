"""Genera HTML listo para imprimir a PDF (A4) a partir de archivos Markdown en esta carpeta."""
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
html { font-size: 11pt; }
body {
  font-family: "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.45;
  color: #1a1a1a;
  background: #fafafa;
  margin: 0;
}
.print-hint {
  background: #e8f4fc;
  border: 1px solid #7eb8da;
  color: #0c4a6e;
  padding: 10px 14px;
  margin: 12px auto 0;
  max-width: 210mm;
  border-radius: 6px;
  font-size: 10pt;
}
article.informe {
  max-width: 210mm;
  margin: 12px auto 24px;
  padding: 14mm 16mm;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
}
h1 { font-size: 18pt; margin-top: 0; page-break-after: avoid; }
h2 { font-size: 13pt; margin-top: 1.2em; page-break-after: avoid; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
h3 { font-size: 11pt; margin-top: 1em; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin-top: 0.9em; }
p, li { orphans: 3; widows: 3; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 7.5pt;
  margin: 10px 0;
  page-break-inside: auto;
}
thead { display: table-header-group; }
tr { page-break-inside: avoid; page-break-after: auto; }
th, td {
  border: 1px solid #bbb;
  padding: 4px 5px;
  vertical-align: top;
  word-break: break-word;
  hyphens: auto;
}
th { background: #f0f4f8; font-weight: 600; }
code {
  font-family: ui-monospace, Consolas, "Cascadia Mono", monospace;
  font-size: 0.88em;
  background: #f4f4f4;
  padding: 1px 4px;
  border-radius: 3px;
}
pre {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  padding: 10px 12px;
  font-size: 8pt;
  overflow-x: auto;
  page-break-inside: avoid;
  white-space: pre-wrap;
  word-break: break-word;
}
pre code { background: none; padding: 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.2em 0; }
ul, ol { padding-left: 1.2em; }
@media print {
  body { background: #fff; }
  .screen-only { display: none !important; }
  article.informe {
    box-shadow: none;
    margin: 0;
    padding: 0;
    max-width: none;
  }
  @page {
    size: A4;
    margin: 14mm 12mm;
  }
  a { color: #000; text-decoration: none; }
}
@media screen {
  .screen-only { }
}
"""


def build_print_html(md_file: str, html_file: str, page_title: str) -> Path:
    md_path = ROOT / md_file
    out_path = ROOT / html_file
    md = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        md,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="print-hint screen-only">
    <strong>Exportar a PDF:</strong> use <kbd>Ctrl+P</kbd> (Windows) o el menú Imprimir →
    <strong>Guardar como PDF</strong> / <strong>Microsoft Print to PDF</strong>.
    Documento optimizado para papel A4.
  </div>
  <article class="informe">
{body}
  </article>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    docs = [
        (
            "INFORME_VULNERABILIDADES.md",
            "INFORME_VULNERABILIDADES_print.html",
            "Informe de análisis de vulnerabilidades — Control-PrecISO",
        ),
        (
            "PLAN_REMEDIACION.md",
            "PLAN_REMEDIACION_print.html",
            "Plan de remediación — Control-PrecISO",
        ),
    ]
    for md_file, html_file, title in docs:
        p = build_print_html(md_file, html_file, title)
        print(f"OK -> {p}")
