# Implementation Workflow

This file defines the explicit implementation workflow for active work in SLDB.

## Preconditions

Before implementation starts:

1. The work must be represented by active task files in `desk/tasks/`.
2. The task set must be atomized.
3. Dependencies must be explicit.
4. Required context pills must exist for any ambiguous aspect.
5. `desk/tasks/Board.md` must match the active task set.

## Implementation Workflow

1. ATOMIZE - Split large work into the smallest independently completable tasks.
2. DEDUPE - Merge overlaps and remove duplicate task intent.
3. CLEAN - Delete stale or obsolete content instead of preserving it.
4. AUDIT - Check code, tests, and git history before claiming anything is missing or done.
5. RESOLVE - Remove contradictions in intended end state.
6. BIND - Bind the task to the required context pills.
7. IMPLEMENT - Make only the changes required for the active task.
8. INVALIDATE - Check whether existing tests are stale.
9. VERIFY - Add or update tests for the implemented behavior.
10. TEST - Run the relevant tests; all required tests must pass.
11. CLEAN - Remove stale pills or desk artifacts made redundant by the implementation.
12. DELETE - Remove the resolved task file.
13. BOARD - Update `desk/tasks/Board.md` in the same logical change.
14. COMMIT - Make an atomic commit only after the workflow is complete.

## Scope Discipline

- One task should be completable and verifiable by one agent in one session.
- If a task contains more than 3-4 independently failing steps, split it.
- Do not solve multiple unrelated concerns under one task.

## Truth Hierarchy

- Code is truth.
- Git history is the durable record.
- Docs are index and current guidance.
- Task files and pills are temporary execution scaffolding.

## Completion Rule

Work is not complete until:

- the intended behavior exists in code
- the relevant tests pass
- stale temporary task artifacts are removed
- the board reflects the current active state
