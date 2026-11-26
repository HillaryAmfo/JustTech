import re
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from main_app.i18n import FR

roots = [pathlib.Path("templates"), pathlib.Path("main_app/tests.py")]
pat = re.compile(r"\{\{\s*'((?:[^'\\]|\\.)*)'\s*\|tr\b")
pat_with = re.compile(r"\{%\s*with\b[^%]*?'((?:[^'\\]|\\.)*)'\s*\|tr\b")
keys = set()
for root in roots:
    for p in root.rglob("*"):
        if p.suffix in (".html", ".py"):
            text = p.read_text(encoding="utf-8")
            for pattern in (pat, pat_with):
                for m in pattern.finditer(text):
                    keys.add(m.group(1).replace("\\'", "'"))
missing = sorted(k for k in keys if k not in FR)
print("tr keys found:", len(keys))
print("missing from FR dict:", len(missing))
for k in missing:
    print("  MISSING:", repr(k))
sys.exit(1 if missing else 0)