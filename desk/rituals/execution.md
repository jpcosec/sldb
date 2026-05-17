# Execution ritual for active desk tasks

ID: ritual-execution

## Purpose

Carry one active desk task through scoped implementation with explicit task and pill binding.

## Trigger

Start when a desk task becomes the current execution target.

## Preconditions

- The task exists in desk/tasks.
- Dependencies are explicit.
- Required pills exist.
- The board routes the task as active.

## Steps

1. Atomize the work into one coherent deliverable.
1. Audit code, docs, tests, and git state before changing anything.
1. Bind the task to the pills that remove ambiguity.
1. Implement only the changes required for the active task.
1. Keep scope tight and avoid unrelated fixes.
1. Prepare validation before calling the work complete.

## Validation

- The active task is explicit.
- Required pills are named in the task.
- Changes stay within task scope.
- The work is ready for testing and closeout.

## Failure Modes

- Working without an active task doc.
- Mixing unrelated concerns into one task.
- Skipping pill binding when ambiguity still exists.

## Completion

The implementation is complete enough to enter the testing and closeout rituals.

## Tags

- system:sldb
- workspace:desk
- topic:rituals
- topic:execution
