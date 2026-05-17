# Support structured model composition at render time

ID: task-012
Status: active

## Goal

Allow SLDB models to compose structured child models at render time so boards, tasks, rituals, and future step models can render richer views from references.

## Scope

In scope: render-time model composition, selective expansion policies, board-to-task composition, ritual-step composition, and composition tests. Out of scope: generic uncontrolled transclusion of every referenced document.

## References

- desk/models/board.py
- desk/models/task.py
- desk/models/ritual.py
- src/sldb/links.py
- README.md

## Dependencies

- 

## Pills

- pill-002
- pill-003

## Files

- desk/models/
- src/sldb/core/
- src/sldb/links.py
- tests/

## Implementation Path

Design a composition mechanism that can expand referenced task and step models during rendering while leaving some relationships, such as pills, as references only.

## Validation

- BoardDoc can render task-derived structure from referenced tasks
- pill references remain references by policy
- rituals can compose structured steps through a step model
- render-time composition is covered by tests

## Done When

SLDB supports explicit structured composition in render time for models like BoardDoc and RitualDoc without collapsing all references into free-form transclusion.

## Tags

- system:sldb
- topic:composition
- topic:rendering
- topic:models
