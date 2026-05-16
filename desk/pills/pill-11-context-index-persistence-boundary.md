# Context Index Persistence Boundary

**Type:** `decision`
**Scope:** `component`
**Language:** `en`
**Nature:** `context`
**Bound Tasks:** `task-16`

## Why

Persisting too much of the document IR too early will make the store schema unstable and heavier than needed.

## What

- Persist only the section/context subset needed for search and navigation.
- Do not persist full surface trees in store artifacts for this slice.
- Runtime fallback behavior must remain possible if persisted section data is absent.

## Where

- `src/sldb/store/models.py`
- `src/sldb/store/io.py`
- `src/sldb/store/semantic.py`
- `src/sldb/store/query.py`

## How

Add the smallest store model that supports durable section context. Keep it aligned with `DocumentIR.context_index`, not with the full conceptual SMG model.

## Language

- Use `persisted section context` for the store artifact.
- Use `runtime IR` for the reconstructed full document representation.

## Scope

This pill limits persistence scope. It does not require full graph persistence.
