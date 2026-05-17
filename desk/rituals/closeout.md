# Closeout ritual for tracked desk tasks

ID: ritual-closeout

## Purpose

Close a desk task only after tests, board cleanup, store cleanup when needed, and a dedicated closing commit.

## Trigger

Start when the implementation work for a task is complete.

## Preconditions

- Relevant tests pass.
- Board updates are prepared.
- Any stale context docs are ready to be removed.
- The closing change is ready to commit.

## Steps

1. Invalidate or fix stale tests if they no longer prove the intended behavior.
1. Run the required validation commands and confirm they pass.
1. Remove stale context docs that are no longer needed.
1. Untrack the task document from the local store if it is tracked.
1. Delete the resolved task file and remove it from the board.
1. Create one atomic closing commit for the task.

## Validation

- The task is gone from desk/tasks.
- The board no longer routes the task.
- The local store stays consistent after untracking.
- A dedicated closing commit exists in git.

## Failure Modes

- Deleting the task before the closing commit exists.
- Leaving a stale tracked document in the store.
- Calling a task closed while tests still fail.

## Completion

The task has left the active workspace and its closure is recorded by its own git commit.

## Tags

- system:sldb
- workspace:desk
- topic:rituals
- topic:closeout
