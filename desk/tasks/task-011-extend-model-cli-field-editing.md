# Extend model CLI editing to add and remove fields

ID: task-011
Status: active

## Goal

Allow the CLI to add and remove model fields as part of the same safe draft workflow used for template editing.

## Scope

In scope: field add and remove operations, field metadata updates, typed modification errors, and contract-version changes. Out of scope: free-form Python refactors unrelated to the document contract.

## References

- README.md
- src/sldb/cli/parser.py
- src/sldb/cli/commands/models.py
- docs/models.py

## Dependencies

- 

## Pills

- pill-002
- pill-003

## Files

- src/sldb/cli/parser.py
- src/sldb/cli/commands/models.py
- src/sldb/store/
- tests/

## Implementation Path

Build field add and remove operations on top of the model draft workflow, require field descriptions and types, and version the contract whenever the active model changes.

## Validation

- fields can be added from the CLI into the draft
- fields can be removed from the CLI from the draft
- typed errors cover missing fields and incompatible markers
- model version changes are visible after promotion

## Done When

The CLI can safely add and remove contract fields and persist versioned model changes only after validation succeeds.

## Tags

- system:sldb
- topic:models
- topic:fields
- topic:versioning
