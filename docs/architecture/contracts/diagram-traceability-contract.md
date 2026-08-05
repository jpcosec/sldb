# Diagram Traceability Contract

## Purpose and governing sources

This contract defines how architecture diagrams declare their traceability:
every diagram source (`.puml`, `.mmd`) is a projection of specyaml and is
registered in the vista registry. The canonical render
(`docs/architecture/sldb_Kernel_Vistas_UML.html`) is a generated artifact.

Governing sources:
- `docs/architecture/spec2viz/desk/atoms/atom-diagram-as-projection.md`
- `docs/architecture/spec2viz/desk/atoms/atom-traceability-symmetry.md`
- `docs/architecture/spec2viz/desk/atoms/atom-generated-artifact-drift.md`
- `docs/architecture/spec2viz/desk/atoms/atom-coverage-warning.md`
- `desk/atoms/graph-projection.md`
- `desk/atoms/projection-spec.md`
- `desk/atoms/provenance-record.md`
- `docs/architecture/target-system-overview.md`
- `docs/architecture/contracts/specyaml-schema-contract.md`

## In-scope

- the vista registry `docs/architecture/vistas/vistas.yml`
- traceability headers required in `core-diagrams/*.puml`
- the generated-artifact rule for the vistas HTML
- validation rules enforced by `scripts/validate_spec_traceability.py`

## Explicit non-goals

- no claim that Mermaid and PlantUML renders are semantically diffed
- no node-level coverage check (element ↔ spec node) beyond headers and registry
- no runtime implementation claims

## Vista registry

`vistas.yml` is the single registry of views. Each vista entry MUST declare:

```yaml
- id: dNN                 # stable, matches the HTML section id
  nav: <nav label>
  lbl: <section label>
  title: <h2>
  desc: <section description>
  mmd: vistas/<file>.mmd  # Mermaid source of truth for the render
  puml: <file>.puml | null
  specs: [sldb.target.*, ...]   # may be empty
```

- `mmd` files under `docs/architecture/vistas/` are the render sources.
- `puml` files under `docs/architecture/core-diagrams/` are the PlantUML
  documentation projection; a vista may legitimately have `puml: null`.
- Mapping vista ↔ puml is 1:1; a puml file without vista is an error.

## PUML traceability header

Every `core-diagrams/*.puml` MUST start with:

```
' --- trazabilidad (diagram-traceability-contract) ---
' vista: dNN
' governed-by: <spec-id> [, <spec-id>...]
```

The header must agree with `vistas.yml` (`puml:` and `specs:` fields).

## Generated artifact rule

- `sldb_Kernel_Vistas_UML.html` is produced ONLY by
  `scripts/generate_vistas_html.py` from `vistas/template.html` + `vistas.yml`
  + `*.mmd`.
- Hand edits to the HTML are forbidden; the validator regenerates and diffs.
- Section elements carry `data-spec` / `data-puml` attributes sourced from the
  registry, so browser tooling (e.g. the annotation layer) can key marks to
  spec identity.

## Validation

`scripts/validate_spec_traceability.py` MUST pass:

1. registry well-formed; `mmd`/`puml`/`specs` references exist
2. puml headers present and consistent with the registry (vista, specs)
3. vista ↔ puml 1:1
4. HTML drift check: committed HTML == regenerated HTML
5. specyaml `views:` ↔ vista `specs:` symmetry (shared with schema contract)

Warnings (non-fatal): vista with empty `specs:`; spec with empty `views:`.

## Downstream constraints

- Adding a diagram = registry entry + mmd source (+ optional puml) + regenerate.
- Renaming a vista id is breaking: annotations and puml headers key on it.
- deskops closeout for any task touching these paths requires validator green.
