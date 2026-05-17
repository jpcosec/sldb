# Fix empty-list document updates in tracked TaskDoc workflows

ID: task-007
Status: active

## Goal

Allow tracked task documents to be updated to genuinely empty list fields without breaking roundtrip validation or field-update commands.

## Scope

In scope: list-field update behavior during document mutation. Out of scope: unrelated renderer changes.

## References

- desk/models/task.py
- src/sldb/cli/commands/fields.py
- src/sldb/runtime/validation.py

## Dependencies

- none

## Pills

- pill-002
- pill-003

## Files

- desk/models/task.py
- src/sldb/cli/commands/fields.py
- src/sldb/runtime/validation.py

## Implementation Path

Reproduce the empty-list update failure, identify whether rendering or extraction loses the section, and make empty lists roundtrip safely for tracked task documents.

## Validation

- field update can set depends_on to an empty list
- updated task documents still validate
- no required sibling fields disappear during update

## Done When

Tracked docs can be updated to empty list values without corrupting the document or failing validation.

## Tags

- system:sldb
- topic:fields
- topic:validation
- workspace:desk
