# Rituals

This file defines the operating rituals for desk-driven work in SLDB.

## Core Rules

- No task is complete without testing.
- No task is complete without its own closing commit.
- `desk/tasks/` contains only active work.
- `desk/contexts/` contains only active task context.
- No task is closed until its closing change is committed to git.
- Resolved tasks are deleted only after their closing change is committed; history belongs in git.
- Resolved context docs are deleted once their content is stable elsewhere.
- Trust the code and git history, not stale task prose.
- Delete legacy or obsolete content instead of preserving fake work.

## Atomization Ritual

Before execution:

1. ATOMIZE - Break work into the smallest independently completable tasks.
2. DEDUPE - Merge overlapping tasks.
3. CLEAN - Delete stale or legacy content when deletion is the correct outcome.
4. AUDIT - Verify current reality from code, tests, and git history.
5. RESOLVE - Remove contradictory end states and circular dependencies.
6. BIND - Link each non-trivial implementation step to an active task and its required context docs.
7. INDEX - Update `desk/tasks/Board.md`.
8. EXECUTE - Work with explicit task boundaries.

Atomization rule:

- One task should be completable and verifiable by one agent in one session.
- If a task has more than 3-4 independently failing steps, split it.

## Task Lifecycle

When starting work:

1. Ensure the task exists in `desk/tasks/`.
2. Ensure dependencies are explicit.
3. Ensure required context docs exist in `desk/contexts/`.
4. Ensure the board reflects the active task set.

When finishing work:

1. INVALIDATE - Check whether existing tests are stale and fix or delete them.
2. VERIFY - Add or update tests for the completed behavior.
3. TEST - Run the relevant test suite; all required tests must pass.
4. CHANGELOG - Update `changelog.md` if the repo workflow requires it.
5. DOCUMENT - Push stable knowledge into durable docs if new guidance was created.
6. CLEAN - Delete stale desk artifacts that are no longer true.
7. DELETE - Remove the resolved task file.
8. BOARD - Remove the task from `desk/tasks/Board.md`.
9. COMMIT - Make an atomic closing commit. A task is not closed before this commit exists.

## Permanent Guardrail

- Every task closes with its own atomic commit.
- Deleting a task file or removing it from the board before that commit is invalid.
- This rule is permanent ritual policy, even if a pill also restates it for active execution context.

## Task Shape

Each active task should contain only actionable present-state information:

- objective
- references
- concrete end state
- suggested implementation path
- dependencies
- validation

Do not keep historical reports, resolved task archives, or stale diagnoses in `desk/tasks/`.

## Board Rule

`desk/tasks/Board.md` is the single index of active work.

- It should list only active tasks.
- Closed or historical items do not stay on the board.
- Board updates and task-file updates happen together.

## Context Rule

- `desk/contexts/` contains only active context docs.
- Context docs must name the tasks they serve.
- Once a task closes and the context is no longer needed, delete the context doc.
