# SMG IR Boundary

**Type:** `model`
**Scope:** `domain`
**Language:** `en`
**Nature:** `context`
**Bound Tasks:** `task-13`, `task-14`, `task-15`, `task-16`, `task-18`

## Why

SLDB needs a richer document artifact between raw markdown surface and store/query layers, but it should not absorb a full external reasoning system just to model sections and context.

## What

- `SMG` in SLDB means `Surface + Meaning + Graph`.
- The current implementation target is a lightweight `DocumentIR`, not full RDF/OWL.
- Section/context indexing belongs inside that IR boundary.
- Full reasoning/export can remain the concern of a different library later.

## Where

- `src/sldb/core/ir.py`
- `src/sldb/cli/graph.py`
- `docs/architecture/smg-ir.md`

## How

Prefer adding explicit, typed IR artifacts that preserve reversibility and support navigation. Do not jump straight from markdown surface to persisted knowledge-graph abstractions.

## Language

- Use `DocumentIR` for the runtime artifact.
- Use `section/context index` for the minimal "what is this section about" layer.
- Use `SMG` only for the conceptual 3-layer model.

## Scope

This pill governs the architecture boundary. It does not require implementing RDF, OWL, or external reasoners inside SLDB.
