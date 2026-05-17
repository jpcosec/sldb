# Testing

This file defines the minimum testing rules for implementation work in SLDB.

## Core Rule

- No task is complete without testing.

## Testing Workflow

For every active implementation task:

1. INVALIDATE - Check whether existing tests are stale, wrong, or no longer aligned with the intended behavior.
2. VERIFY - Add new tests or update existing tests to cover the intended behavior.
3. TEST - Run the relevant test suite.
4. PASS - Do not mark the task complete unless the required tests pass.

## Test Policy

- Tests are part of the implementation, not an optional follow-up.
- If semantics change, tests must be updated to reflect the intended contract.
- If a test encodes stale behavior, fix or delete it before using it as proof.
- Prefer the smallest relevant test scope first, then run broader suites before closing a task.

## Completion Gate

Before deleting a task file, deleting bound context docs, or calling work complete, verify:

1. The intended behavior is covered by tests.
2. The relevant tests pass.
3. No known failing tests were ignored to force completion.

## Anti-Patterns

- Skipping tests to move faster.
- Treating stale tests as canonical truth.
- Closing a task with failing relevant tests.
- Adding runtime changes without validating them.
