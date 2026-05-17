# Implementation Workflow

This file defines the lifecycle for active work driven by desk task/context documents.

## Preconditions

Before implementation starts:

1. The work must be represented by active task files in `desk/tasks/`.
2. The task set must be atomized.
3. Dependencies must be explicit.
4. Required context documents must exist for any ambiguous aspect.
5. `desk/tasks/Board.md` must match the active task set.

## Implementation Workflow

1. ATOMIZE - Split large work into the smallest independently completable tasks.
2. DEDUPE - Merge overlaps and remove duplicate task intent.
3. CLEAN - Delete stale or obsolete content instead of preserving it.
4. AUDIT - Check code, tests, and git history before claiming anything is missing or done.
5. RESOLVE - Remove contradictions in intended end state.
6. BIND - Bind the task to the required context documents.
7. IMPLEMENT - Make only the changes required for the active task.
8. INVALIDATE - Check whether existing tests are stale.
9. VERIFY - Add or update tests for the implemented behavior.
10. TEST - Run the relevant tests; all required tests must pass.
11. DOCUMENT - Move stable knowledge into durable docs when needed.
12. CLEAN - Remove stale context docs or other desk artifacts made redundant by the implementation.
13. DELETE - Remove the resolved task file.
14. BOARD - Update `desk/tasks/Board.md` in the same logical change.
15. COMMIT - Make an atomic closing commit. Work is not closed before this commit exists.

## Scope Discipline

- One task should be completable and verifiable by one agent in one session.
- If a task contains more than 3-4 independently failing steps, split it.
- Do not solve multiple unrelated concerns under one task.

## Truth Hierarchy

- Code is truth.
- Git history is the durable record.
- Docs are index and current guidance.
- Task files and context files are temporary execution scaffolding.

## Completion Rule

Work is not complete until:

- the intended behavior exists in code
- the relevant tests pass
- stale temporary task artifacts are removed
- stable context has been absorbed into durable docs when appropriate
- the board reflects the current active state
- the closing change has its own commit in git
