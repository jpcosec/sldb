# Structure desk ritual documents as RitualDoc instances

ID: task-005
Status: active

## Goal

Bring the active desk ritual surfaces into SLDB-native RitualDoc form so desk can self-host its execution guidance.

## Scope

In scope: ritual document instances and routing from the board. Out of scope: redesigning the ritual policy itself unless modeling requires it.

## References

- desk/RITUALS.md
- desk/IMPLEMENTATION-WORKFLOW.md
- desk/TESTING.md
- desk/models/ritual.py

## Dependencies

- none

## Pills

- pill-001
- pill-002

## Files

- desk/RITUALS.md
- desk/IMPLEMENTATION-WORKFLOW.md
- desk/TESTING.md
- desk/tasks/Board.md

## Implementation Path

Decide which current ritual docs should become RitualDoc instances, model them explicitly, and update board routing so the structured ritual set is what desk points at.

## Validation

- ritual docs conform to RitualDoc
- board routes the structured ritual docs
- desk can track the ritual docs through the CLI

## Done When

Desk rituals are represented by actual RitualDoc documents instead of prose-only permanent notes.

## Tags

- system:sldb
- topic:workflow
- topic:rituals
- workspace:desk
