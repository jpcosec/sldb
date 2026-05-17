# Extend the SLDB routine pattern to drawer workspaces

ID: task-006
Status: active

## Goal

Give drawer-style backlog work the same board and ritual treatment as desk, adapted for plans and deferred features.

## Scope

In scope: drawer boards, drawer rituals, and routing conventions for non-executing plans. Out of scope: executing the entire backlog workflow immediately.

## References

- desk/tasks/Board.md
- desk/models/board.py
- desk/models/ritual.py

## Dependencies

- task-005

## Pills

- pill-001
- pill-002
- pill-003

## Files

- desk/
- drawer/

## Implementation Path

Define how drawer differs from desk, then add the boards and rituals needed for deferred work without mixing it into the active execution surface.

## Validation

- drawer has a clear board shape
- drawer has explicit ritual docs
- desk and drawer responsibilities are separated

## Done When

Drawer work has its own structured routing and ritual surface instead of being mixed into desk.

## Tags

- system:sldb
- topic:workflow
- topic:drawer
- workspace:desk
