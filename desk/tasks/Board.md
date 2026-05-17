# Desk Board

ID: board-001
Scope: desk

## Purpose

Route the active desk execution set: tasks, pills, and the ritual documents that govern execution and closure.

## Tasks

- desk/tasks/task-014-define-sldb-core-runtime-layout.md
- desk/tasks/task-015-model-sldb-readme-as-doc.md
- desk/tasks/task-016-define-sldb-git-versioning-policy.md
- desk/tasks/task-017-migrate-store-core-runtime-routing.md
- desk/tasks/task-018-standardize-atomdoc.md
- desk/tasks/task-019-materialize-atoms-across-artifacts.md
- desk/tasks/task-020-prove-atom-materialization-slice.md

## Pills

- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-002-test-real-cli-surfaces.md
- desk/contexts/pill-003-capture-cli-gaps.md
- desk/contexts/pill-004-opsys-boundary.md
- desk/contexts/pill-005-subagent-execution.md

## Rituals

- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md

## Notes

Every closed task must end in its own closing commit. Any missing SLDB capability discovered during execution must become a new active desk task.

## Task Details

- Define the .sldb core/runtime/.config layout [active] - Turn the .sldb layout proposal into an executable design target with clear boundaries between durable core state, runtime state, and local config.
- Model .sldb/README.md as a structured SLDB document [active] - Define and implement the document model for .sldb/README.md as the typed entrypoint into the store.
- Define git and versioning policy for .sldb [active] - Make the durable-versus-runtime versioning policy of .sldb explicit and operational.
- Migrate the flat store implementation to core/runtime routing [active] - Refactor the current store implementation so it respects the new core/runtime/.config split.
- Standardize AtomDoc as the durable conceptual source model [active] - Define AtomDoc as a first-class structured model for durable conceptual source material.
- Materialize atoms into docs, features, tasks, and pills [active] - Design and implement the SLDB surfaces that materialize AtomDoc into downstream workflow artifacts.
- Prove one atom materialization slice end to end [active] - Run one small concept through the full path from atom to durable doc, deferred feature, active task, and temporary pill.

## Tags

- system:sldb
- workspace:desk
- topic:routing
