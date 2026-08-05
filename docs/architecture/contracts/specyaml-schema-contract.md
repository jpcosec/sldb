# SpecYAML Schema Contract

## Purpose and governing sources

This contract defines what a valid specyaml document is: the machine-readable
specification format under `docs/architecture/spec2viz/`. Specyaml is the
documental nexus between `desk/atoms/` (governing knowledge atoms) and the
diagram projections (`core-diagrams/*.puml`, generated vistas HTML).

Governing sources:
- `docs/architecture/spec2viz/desk/atoms/atom-specyaml-nexus.md`
- `docs/architecture/spec2viz/desk/atoms/atom-reference-edge.md`
- `docs/architecture/spec2viz/desk/atoms/atom-traceability-symmetry.md`
- `desk/atoms/concept-binding.md`
- `desk/atoms/ports-and-adapters.md`
- `docs/architecture/target-system-overview.md`
- `docs/architecture/contracts/atom-ontology-map.md`
- `docs/architecture/contracts/diagram-traceability-contract.md`

## In-scope

- required top-level shape of every `spec2viz/*.yml`
- node and edge field rules
- the `atoms:` cross-reference rule (edge spec → atoms)
- the `views:` coverage rule (edge spec → vistas)
- versioning rule for spec evolution

## Explicit non-goals

- no runtime implementation claims
- no validation of diagram rendering correctness (that is the traceability contract)
- no replacement of atoms; specyaml references atoms, never duplicates their prose
- no claim that node-level diagram coverage is machine-checked today (spec↔vista
  level only)

## Document shape

Every specyaml file MUST carry:

```yaml
id: sldb.target.<name>      # unique, stable, kebab/snake within sldb.target.*
title: <human title>
type: component | deployment
version: "<semver>"
views: [<vista-id>, ...]    # may be empty; see coverage rule
data:
  nodes: { <NodeId>: <node> , ... }
  # plus exactly one relation collection:
  #   edges:       component specs      (from / to / relation / label?)
  #   connections: deployment specs     (from / to / protocol)
  # deployment specs may add: artifacts: { <ArtifactId>: <node> , ... }
```

## Node rules

- `label` (required): display text.
- `kind` (required): one of `core`, `boundary`, `database`, `server`, `client`, `backend`.
- `contains` (optional): list of node/artifact ids defined in the same file.
- `atoms` (optional but expected for kernel-significant nodes): list of atom ids
  that MUST exist as `desk/atoms/<atom>.md`. This is the only sanctioned edge
  from specyaml into the atom layer.
- Node ids are stable identifiers: renaming an id is a breaking spec change.

## Edge rules

- `from` / `to` MUST reference ids defined in `nodes` or `artifacts` of the same file.
- `relation` (component) / `protocol` (deployment) is required on every edge.
- `label` is optional and carries semantics, not routing.

## Views rule (edge spec → vistas)

- `views:` lists vista ids (`d00`–`dNN`) declared in
  `docs/architecture/vistas/vistas.yml`.
- Symmetry is mandatory: `spec.views` contains `dNN` iff the vista entry lists
  the spec in its `specs:` field. The validator enforces this.
- A spec with empty `views:` is a coverage WARNING (spec sin proyección visual).

## Versioning rule

- `version` bumps on any structural change (node/edge add, remove, rename).
- Editorial changes (label wording) do not bump.
- Consumers pin by `id`, not by file name.

## Validation

- `scripts/validate_spec_traceability.py` MUST pass:
  - schema shape and kind vocabulary
  - edge referential integrity
  - `atoms:` targets exist in `desk/atoms/`
  - `views:` ↔ vista `specs:` symmetry
- Coverage warnings are reported, not fatal.

## Downstream constraints

- Any task touching `spec2viz/` must re-run the generator and validator before closeout.
- The vistas HTML is a generated artifact and must never be hand-edited.
