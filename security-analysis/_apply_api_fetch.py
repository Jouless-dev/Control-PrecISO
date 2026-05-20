"""Reemplaza await fetch por await apiFetch en URLs de API Gateway (no Cognito)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "Control-PrecISO-main"


def patch_file(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    original = content

    def replacer(match: re.Match) -> str:
        start = match.start()
        window = content[start : start + 1200]
        if "cognito-idp" in window:
            return match.group(0)
        return "await apiFetch("

    content = re.sub(r"\bawait fetch\s*\(", replacer, content)
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for html in sorted(ROOT.glob("*.html")):
        if patch_file(html):
            changed.append(html.name)
    print("Updated:", ", ".join(changed) if changed else "none")


if __name__ == "__main__":
    main()
