---
# board-xxx
id: board-sldb-desk
# Affected workspace or domain
scope: sldb-local-desk
# List of task-xxx paths
tasks:
- desk/tasks/task-congelar-journal-autoridad-arbol.md
- desk/tasks/task-build-code-self-documentation.md
- desk/tasks/task-unify-store-context-and-federation.md
- desk/tasks/task-correct-ast-ownership-and-section-contracts.md
- desk/tasks/task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico.md
# List of pill-xxx paths
pills:
- desk/pills/pill-015-self-documentation-boundaries.md
- desk/pills/pill-001-sldb-vs-deskops-boundary.md
- desk/pills/pill-002-onboarding-surface-before-depth.md
- desk/pills/pill-003-template-marker-roundtrip-contract.md
- desk/pills/pill-004-store-init-idempotency.md
- desk/pills/pill-005-store-health-is-sldb-owned.md
- desk/pills/pill-006-model-registration-is-queryable.md
- desk/pills/pill-007-sldb-text-layer-vs-kgdb-graph-layer.md
- desk/pills/pill-008-sldb-cli-document-contract.md
- desk/pills/pill-009-cli-error-and-serialization-failure-mode.md
- desk/pills/pill-010-active-board-slice-execution-map.md
- desk/pills/pill-011-addressability-task-execution-context.md
- desk/pills/pill-012-query-task-execution-context.md
- desk/pills/pill-013-composition-task-execution-context.md
- desk/pills/pill-014-semantic-export-task-execution-context.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- system:deskops
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

Current review follow-up: CLI self-documentation is active; shared store context/federation and AST ownership/section contracts are separate open tasks. Their task files define scope and validation. Historical rows below have not been reclassified.

- Mapear arquitectura real de SLDB [active] - _Describe the concrete result this task must produce._

## Task Details

_Generated from the task references above._

- Congelar el journal y rediseñar la autoridad: el árbol guarda, el journal es una vista [draft] - Dejar por escrito la dirección de diseño para cuando se retome: el **árbol es la autoridad**; el **journal es una interfaz de lectura** sobre él (como `git log`/`git diff` sobre el object database), no un segundo almacén.
- Build code-derived self-documentation [active] - Provide repeatable scan, materialization, tracking, and freshness checks for code documentation.
- Unify store context and federation [open] - Resolve project operations from the nearest enclosing store and make known stores discoverable through a maintained global catalog.
- Correct AST ownership and section contracts [open] - Make field ownership and section boundaries reliable enough for structural queries and documentation provenance.
- Borrar la capa runtime/edges y podar el surface publico [draft] - Borrar edge_sync.py, edge_rebuild.py, edge_doc_contribution.py, edge_index/doc_contribution.py, models/doc_edges.py, models/edge_contribution.py, api/edges/rebuild_edges.py, cli/commands/edges.py, cli/parsers/edges.py, cli/serve/edges_routes.py, y podar api/__init__.py.
