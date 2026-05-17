# Testing ritual for desk task closure

ID: ritual-testing

## Purpose

Verify the intended behavior with the right test scope before a task can close.

## Trigger

Run after implementation changes and before closeout.

## Preconditions

- The intended behavior is clear.
- Relevant tests or test locations are known.

## Steps

1. Check whether existing tests are stale or encode obsolete behavior.
1. Add or update tests for the intended contract.
1. Run the smallest relevant test scope first.
1. Run broader validation when the task changes shared behavior.
1. Do not proceed to closeout while relevant tests fail.

## Validation

- The intended behavior is covered.
- The relevant tests pass.
- No known failure was ignored to force completion.

## Failure Modes

- Treating stale tests as truth.
- Skipping tests to move faster.
- Closing with failing relevant tests.

## Completion

The task has trustworthy test evidence and can proceed to closeout.

## Tags

- system:sldb
- workspace:desk
- topic:rituals
- topic:testing
