# Task 01: Link Recovery And Compose

## Goal

Implement explicit document links with `[[...]]` and transclusion links with `![[...]]`, plus `recover` and `compose` commands.

## Scope

- parse `[[target]]`
- parse `![[target]]`
- resolve tracked document targets
- add `sldb recover`
- add `sldb compose`

## Expected Changes

- CLI updates in `src/sldb/cli.py`
- link parsing/extraction support in the document processing layer
- resolution logic against tracked docs and file paths
- tests for link parsing, resolution, recover, and compose

## Suggested Milestones

1. define link syntax and resolution rules
2. implement parser support for links
3. implement recovery bundle output
4. implement compose/transclusion behavior
5. add CLI commands and tests

## Acceptance Criteria

- `recover` returns structured linked context
- `compose` resolves `![[...]]` deterministically
- unresolved links are reported clearly
- roundtrip behavior remains stable for non-link documents
