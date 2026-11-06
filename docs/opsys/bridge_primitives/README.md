# Opsys Bridge Primitives

## Purpose

This document defines the primitives that connect the documentary surface to the code surface.

The documentary surface holds intent, policy, procedure, evidence, and declared structure.
The code surface holds implementation, executable behavior, and runtime constraints.

Bridge primitives let both surfaces remain distinct while still being linked, checked, and synchronized.

## Why A Bridge Layer Exists

Without a bridge layer:

- documentation drifts from implementation
- code loses declared intent
- procedures become stale prose
- examples rot silently
- operational rules stay trapped in team memory

With a bridge layer:

- documentary records can point to code precisely
- alignment rules can be expressed explicitly
- drift can be linted and tested
- transforms can synchronize both surfaces intentionally

## Bridge Primitive Set

The first bridge primitive set is:

1. `Reference`
2. `Constraint`
3. `Lint`
4. `Probe`
5. `Transform`

## Reference

### Definition

A `Reference` links an operational record or documentary artifact to a code target.

The reference should be resolvable, not just textual.

### Why It Exists

- to connect intent to implementation
- to make traceability explicit
- to support navigation in both directions
- to let later lints and probes verify the link

### Static Shape

Suggested fields:

- `source_kind`
- `source_id`
- `target_kind`
- `target_locator`
- `target_display`
- `relation_type`
- `resolution_method`
- `status`
- `notes`

### Target Kinds

Typical target kinds:

- file
- module
- class
- function
- method
- test
- command
- flag
- symbol
- generated artifact

### Resolution Methods

Typical resolution methods:

- path exists
- symbol resolves
- command resolves
- glob match
- parser target exists
- test target exists

### Action Surface

- `references create`
- `references show`
- `references list`
- `references verify`
- `references trace`
- `references repair`

### Notes

`Reference` should become the minimal cross-surface currency of the system.

If a documentary artifact cannot reference the code surface in a durable way, the system will struggle to support trustworthy transforms, lints, or probes later.

## Constraint

> **Reemplazada por `RuleDoc` (GO06, 2026-11-06).** Esta sección queda como registro
> histórico. Una regla de sldb es hoy un documento `RuleDoc` (sujeto `model <= X`, `where`,
> `condition`, severidad, momento y `message`) que evalúan `sldb rules check` y
> `sldb rules explain`: ver [docs/architecture/rules.md](../../architecture/rules.md).

### Definition

A `Constraint` is a declared rule that should hold across documentary and code surfaces.

### Why It Exists

- to turn expectations into named rules
- to let the team reason about alignment explicitly
- to support linting and probing from shared semantics

### Static Shape

Suggested fields:

- `name`
- `scope`
- `statement`
- `severity`
- `evaluation_mode`
- `source_surfaces`
- `target_surfaces`
- `remediation_hint`

### Constraint Examples

- every first-class CLI noun must have help coverage
- every documented command example must resolve to a real command path
- every onboarding ritual must reference at least one executable probe
- every routine with a hook must define a trigger

### Action Surface

- `constraints create`
- `constraints show`
- `constraints list`
- `constraints check`
- `constraints violations`

## Lint

### Definition

A `Lint` is a cheap, frequent, mostly deterministic executable check over one or more surfaces.

### Why It Exists

- to detect drift early
- to keep standards operational
- to provide fast feedback before deeper probes or tests run

### Static Shape

Suggested fields:

- `name`
- `scope`
- `constraint_ref`
- `inputs`
- `severity`
- `autofixable`
- `fix_hint`

### Lint Examples

- broken references
- stale command examples
- unresolved symbol links
- missing help coverage for documented command groups
- routine/checklist mismatch

### Action Surface

- `lints list`
- `lints show`
- `lints run`
- `lints result`
- `lints fix`

## Probe

### Definition

A `Probe` is an executable alignment check that tests whether documentary claims and code behavior still agree.

### Why It Exists

- to validate cross-surface truth
- to test behavior, not just structure
- to catch subtle divergence that lint cannot detect

### Static Shape

Suggested fields:

- `name`
- `intent`
- `target_surface`
- `documentary_inputs`
- `code_inputs`
- `expected_shape`
- `failure_signal`
- `evidence_mode`

### Probe Examples

- run a documented CLI example and compare output shape
- verify a documented command group exists in parser/help/runtime
- verify references to files and symbols still resolve
- verify documented onboarding steps remain recoverable

### Action Surface

- `probes create`
- `probes show`
- `probes list`
- `probes run`
- `probes result`
- `probes explain`

## Transform

### Definition

A `Transform` converts one surface representation into another while preserving intended meaning.

### Why It Exists

- to reduce duplicate maintenance
- to generate useful derivatives
- to synchronize documentary and code surfaces intentionally

### Static Shape

Suggested fields:

- `name`
- `source_kind`
- `target_kind`
- `inputs`
- `outputs`
- `direction`
- `reversible`
- `safety_level`

### Transform Examples

- generate help docs from structured command definitions
- derive checklist stubs from routine definitions
- materialize code annotations from documentary records
- build documentary views from code metadata

### Action Surface

- `transforms create`
- `transforms show`
- `transforms list`
- `transforms preview`
- `transforms run`
- `transforms diff`

## Bridge Execution Order

The bridge layer should usually work in this order:

1. define references
2. declare constraints
3. run lints for cheap drift detection
4. run probes for executable alignment validation
5. use transforms where synchronization should be automated

## Relation To Documentary Primitives

Bridge primitives are not replacements for documentary primitives.

They extend them.

Examples:

- an `IssueReport` can have references and probes
- a `Routine` can have constraints and transforms
- a `Checklist` can be guarded by lints or probes
- a `Ritual` can require reference verification before closure

## First Credible Slice

The smallest useful bridge slice is:

1. `Reference`
2. one or two high-value `Constraint` definitions
3. a `Lint` for broken or stale references
4. a `Probe` for at least one documented CLI walkthrough

That is enough to prove the documentary-to-code bridge without overbuilding the system.

## Open Questions

1. Should `Reference` targets be purely symbolic, purely path-based, or support both from the first slice?
2. Should `Lint` and `Probe` both derive from a shared executable-check primitive?
3. Which transforms should remain advisory only, and which should be allowed to write changes automatically?
4. Which failures should block workflow progression, and which should only warn?
