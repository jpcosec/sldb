import json, subprocess, sys, tempfile, pathlib, ast
src = pathlib.Path("tests/notations/test_component_spec_python.py").read_text()
mod = ast.parse(src)
TREE = next(ast.literal_eval(n.value) for n in mod.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "TREE")
from spec2viz.generators import python_ast
d = pathlib.Path(tempfile.mkdtemp(dir="/dev/shm"))
for rel, text in TREE.items():
    (d / rel).parent.mkdir(parents=True, exist_ok=True); (d / rel).write_text(text, encoding="utf-8")
spec = python_ast.generate_python_ast_spec(d)
nodes = spec["data"]["nodes"]
pick = lambda kind: {k: v["label"] for k, v in nodes.items() if v["kind"] == kind}
out = {"_source": "spec2viz@" + subprocess.check_output(["git", "-C", "/mnt/ssd/proyectos/SLDB_1/spec2viz", "rev-parse", "HEAD"], text=True).strip() + " spec2viz.generators.python_ast.generate_python_ast_spec",
       "modules": pick("module"), "classes": pick("class"),
       "defines": sorted([e["from"], e["to"]] for e in spec["data"]["edges"] if e["relation"] == "defines")}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(python_ast.__file__)
