import ast

src = open("main_app/i18n.py", encoding="utf-8").read()
tree = ast.parse(src)
seen = {}
for node in ast.walk(tree):
    if isinstance(node, ast.Dict):
        for k in node.keys:
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                seen[k.value] = seen.get(k.value, 0) + 1
dups = sorted(k for k, v in seen.items() if v > 1)
print("genuine duplicate keys:", len(dups))
for d in dups:
    print("  ", repr(d))