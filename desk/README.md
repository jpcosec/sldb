# Desk

Temporary execution workspace for SLDB-driven task routine.

`desk/` exists for two things only:

1. Typed temporary documents that represent active tasks and active task context.
2. Rituals for changing code, testing, documenting, and keeping the repo and git state clean.

Nothing in `desk/` is durable project history. Stable knowledge must end up in code, tests, docs, or git history.

## Structure

- `desk/models/` - SLDB models for desk documents.
- `desk/tasks/` - active task documents only.
- `desk/tasks/Board.md` - active routing board.
- `desk/contexts/` - active context documents only.
- `desk/contexts/pills.md` - pill conventions and current base shape.
- `desk/rituals/` - structured ritual documents for execution, testing, and closeout.

## Models

The current base desk models are:

- `BoardDoc`
- `TaskDoc`
- `PillDoc`
- `RitualDoc`

They live in `desk/models/` and use the current SLDB pattern: `StructuredNLDoc` plus inline `__template__` definitions.

## Exclusions

- No resolved tasks.
- No historical reports.
- No durable feature proposals.
- No duplicate project documentation.
