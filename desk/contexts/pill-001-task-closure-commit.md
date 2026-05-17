# Guardrail: close every task with its own commit

ID: pill-001

## What

Task closure in this routine is defined by a completed change plus a dedicated closing commit in git.

## Why

If a task can be called done without a closing commit, the board and desk documents drift away from the durable execution record.

## When

Apply this pill whenever a task is being finished, deleted from `desk/tasks/`, or removed from a board.

## Where

Applies to `desk/RITUALS.md`, `desk/IMPLEMENTATION-WORKFLOW.md`, task closeout, and any future workspace that reuses this routine.

## How

Keep task files active until tests, cleanup, board updates, and the closing change are ready, then create one atomic commit that closes the task.

## How Not

Do not delete a finished task file and call it closed before the closing commit exists. Do not rely on memory or an uncommitted working tree as the record of closure.

## Tags

- system:sldb
- workspace:desk
- topic:git
- topic:task-closure
