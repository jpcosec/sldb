"""Run an sldb CLI command in-process and report every .md opened outside the project root."""
import os, sys, runpy
root = os.path.realpath(os.getcwd())
opened = set()
def hook(event, args):
    if event == "open":
        p = str(args[0])
        if p.endswith(".md"):
            opened.add(os.path.realpath(p))
sys.addaudithook(hook)
sys.argv = ["sldb"] + sys.argv[1:]
try:
    runpy.run_module("sldb", run_name="__main__")
except SystemExit as exc:
    code = exc.code
else:
    code = 0
outside = sorted(p for p in opened if not p.startswith(root + os.sep))
print(f"[audit] {' '.join(sys.argv[1:])}: .md fuera de la raíz abiertos: {outside}; rc={str(code).splitlines()[0][:120]!r}", file=sys.stderr)
