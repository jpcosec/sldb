# Python AST Structure

`python-ast.yml` is a generated structural snapshot of `src/`, not an authored architecture specification. It records modules, top-level classes, and static import relationships as understood by the installed `spec2viz` CLI.

Regenerate and validate it from the repository root:

```bash
spec2viz diagram generate src --out docs/architecture/spec2viz/python-ast.yml \
  --id sldb-python-ast --title 'SLDB Python AST structure' --package sldb
spec2viz diagram validate docs/architecture/spec2viz/python-ast.yml
spec2viz diagram render docs/architecture/spec2viz/python-ast.yml \
  --out docs/architecture/spec2viz/rendered --renderer mermaid
```

The generated Mermaid view is `rendered/python-ast.mmd`. The 2026-09-14 snapshot contains 518 nodes and 1,236 edges.

This is evidence for review, not semantic truth. In particular, the generator does not establish ownership boundaries, runtime call paths, domain roles, or reliable relative-import resolution. Those concepts belong in the curated specs in this directory and must be declared or reviewed by humans.
