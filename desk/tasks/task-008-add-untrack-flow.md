# Add a tracked-document untrack flow for closed desk items

ID: task-008
Status: active

## Goal

Allow closed tracked documents to leave the active workspace without leaving broken store entries behind.

## Scope

In scope: document untrack or delete workflow for the local store. Out of scope: destructive content deletion policy beyond store routing.

## References

- src/sldb/cli/parser.py
- src/sldb/cli/commands/doc.py
- src/sldb/store/io.py
- .sldb/documents/TaskDoc.yaml

## Dependencies

- task-002

## Pills

- pill-001
- pill-002
- pill-003

## Files

- src/sldb/cli/parser.py
- src/sldb/cli/commands/doc.py
- src/sldb/store/
- desk/tasks/

## Implementation Path

Add or define the missing workflow for removing a tracked document from the active store when the workspace document itself is intentionally deleted.

## Validation

- closed tracked docs can be removed from the store cleanly
- stores update no longer reports intentional task closure as missing docs
- desk closeout can keep the store consistent

## Done When

There is a supported way to close and remove tracked workspace documents without leaving stale store entries.

## Tags

- system:sldb
- topic:store
- topic:docs
- workspace:desk
