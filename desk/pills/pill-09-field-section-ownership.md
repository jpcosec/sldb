# Field Section Ownership

**Type:** `decision`
**Scope:** `component`
**Language:** `en`
**Nature:** `context`
**Bound Tasks:** `task-14`, `task-17`

## Why

Fields without section ownership remain globally attached to the document payload, which blocks section-aware queries and navigation.

## What

- Every field node should be able to point to an owning section context.
- Ownership should be represented explicitly, not implied by ad hoc string parsing.
- The initial ownership rule should be deterministic and simple.

## Where

- `src/sldb/core/ir.py`
- `src/sldb/cli/graph.py`
- `src/sldb/cli/commands/fields.py`

## How

Use heading-based structure as the first ownership mechanism. Avoid semantic guessing in the first slice.

## Language

- Use `owning section` for the relationship.
- Use `section-aware field query` for the user-facing capability.

## Scope

This pill covers ownership metadata. It does not require field mutation by section in the same task.
