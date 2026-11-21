# Python AST Structure

`python-ast.yml` is a generated structural snapshot of `src/`, not an authored architecture specification. It records modules, top-level classes, and static import relationships as understood by `sldb notations from-graph`.

Regenerate and validate it from the repository root:

```bash
sldb notations from-graph --python src --module-prefix sldb --id sldb-python-ast \
  --title 'SLDB Python AST structure' --output docs/architecture/spec2viz/python-ast.yml
sldb notations validate docs/architecture/spec2viz/python-ast.yml
specir diagram render docs/architecture/spec2viz/python-ast.yml \
  --out docs/architecture/spec2viz/rendered --renderer mermaid
```

Build the HTML catalog from `vistas.yml` and sync its specs into the store (neither step uses `spec2viz`):

```bash
specir catalog build --config docs/architecture/spec2viz/vistas.yml --out <html>
sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml
sldb notations sync --catalog docs/architecture/spec2viz/vistas.yml --check
```

The generated Mermaid view is `rendered/python-ast.mmd`. The 2026-09-14 snapshot contains 518 nodes and 1,236 edges.

This is evidence for review, not semantic truth. In particular, the generator does not establish ownership boundaries, runtime call paths, domain roles, or reliable relative-import resolution. Those concepts belong in the curated specs in this directory and must be declared or reviewed by humans.
