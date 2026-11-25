# ADR: The Mechanism Stays In SLDB, The Notation Content Moves To specIR

- Status: Accepted, not yet executed
- Date: 2026-11-25
- Decision Maker: the owner
- Related repos: `sldb`, `IR` (specIR), `graph_ui`

## Context

SLDB ships eight notations (`src/sldb/notations/builtin/`: UML class and sequence, statechart,
activity, component, deployment, a component-view matrix and `reflection`) and one spec class per
diagram type (`sldb.models.notation.diagram_specs`). specIR, which replaced spec2viz, imports those
classes from internal modules and adds its own notations for its domain types.

Asked where BPMN, ORCA and IFML belong, the owner drew the line by kind of thing, not by standard:
"everything that is a semantic model projected into specs goes to specIR; the mechanism for that
may be SLDB's".

## Decision

- **SLDB keeps the mechanism**: `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `SpecDoc`,
  `SpecNodeDoc`, `ViewDoc`, and resolving and validating a view against a notation.
- **specIR owns the content**: every notation that describes a modelling standard or a domain
  (UML, BPMN, ORCA, IFML, specIR's layers) and the spec classes per diagram type. specIR seeds them
  into a store when it is installed there.
- A standard is a notation, never code: no branch per notation in a resolver, a view or a renderer.
- `graph_ui` draws whatever notation the store holds. Layout stays generic (graph, lanes by
  partition, grid); a notation asks for a layout kind, it does not bring one.

## Consequences

- The builtin notations and `diagram_specs` move out of SLDB. SLDB needs one minimal notation of
  its own for its tests; about ten test files use the builtins today.
- specIR stops importing SLDB internals because the classes become its own. The earlier request to
  export them from `sldb.api` is void.
- A BPMN notation is specIR work, not an SLDB request.
- SLDB still owes three pieces of mechanism: a notation declaring which standard it implements, a
  document no glyph matches reported as a gap instead of failing the whole view, and a rule
  predicate over a model's semantic tags.

## Not verified

- Whether `reflection` (SLDB drawing itself) stays in SLDB as its test notation.
