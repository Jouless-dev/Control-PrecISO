"""Añade config.js, auth.js y utils.js si faltan y la página usa apiFetch."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Control-PrecISO-main"
BLOCK = (
    '<script src="js/config.js"></script>\n'
    '    <script src="js/auth.js"></script>\n'
    '    <script src="js/utils.js"></script>\n'
)


def needs_scripts(content: str) -> bool:
    return "apiFetch(" in content or "authHeaders(" in content


def has_auth(content: str) -> bool:
    return 'src="js/auth.js"' in content


def inject(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    if not needs_scripts(content) or has_auth(content):
        if has_auth(content) and 'src="js/utils.js"' not in content:
            content = content.replace(
                '<script src="js/auth.js"></script>',
                '<script src="js/auth.js"></script>\n    <script src="js/utils.js"></script>',
                1,
            )
            path.write_text(content, encoding="utf-8")
            return True
        return False
    # Insertar antes del primer <script> en el documento
    idx = content.find("<script")
    if idx == -1:
        idx = content.find("</body>")
    if idx == -1:
        return False
    new_content = content[:idx] + BLOCK + "    " + content[idx:]
    path.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    for html in sorted(ROOT.glob("*.html")):
        if inject(html):
            print("scripts:", html.name)


if __name__ == "__main__":
    main()
