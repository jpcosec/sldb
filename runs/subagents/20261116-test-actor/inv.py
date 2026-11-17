import ast, sys, pathlib
root = pathlib.Path(sys.argv[1])
for p in sorted(root.rglob("*.py")):
    t = ast.parse(p.read_text())
    for n in ast.walk(t):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and not n.name.startswith("_"):
            args=[a.arg for a in n.args.posonlyargs+n.args.args+n.args.kwonlyargs]
            if "actor" in args:
                used=any(isinstance(x,ast.Name) and x.id=="actor" and isinstance(x.ctx,ast.Load) for x in ast.walk(n))
                print(f"{p.relative_to(root)}:{n.lineno}:{n.name} used={used}")
