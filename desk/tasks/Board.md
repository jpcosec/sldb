---
# board-xxx
id: board-sldb-desk
# Affected workspace or domain
scope: sldb-local-desk
# List of task-xxx paths
tasks:
- desk/tasks/task-build-code-self-documentation.md
- desk/tasks/task-unify-store-context-and-federation.md
- desk/tasks/task-correct-ast-ownership-and-section-contracts.md
- desk/tasks/task-mapear-arquitectura-real-de-sldb.md
- desk/tasks/task-definir-arquitectura-objetivo-modular-de-sldb.md
- desk/tasks/task-dise-ar-estrategia-de-extracci-n-y-modularizaci-n.md
- desk/tasks/task-ejecutar-refactor-base-del-n-cleo-sldb.md
- desk/tasks/task-define-sldb-addressability-model.md
- desk/tasks/task-design-sldb-ast-query-primitives.md
- desk/tasks/task-expand-sldb-composition-modes.md
- desk/tasks/task-tighten-semantic-export-provenance-contract.md
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

- Build code-derived self-documentation [active] - Provide repeatable scan, materialization, tracking, and freshness checks for code documentation.
- Unify store context and federation [open] - Resolve project operations from the nearest enclosing store and make known stores discoverable through a maintained global catalog.
- Correct AST ownership and section contracts [open] - Make field ownership and section boundaries reliable enough for structural queries and documentation provenance.
- Mapear arquitectura real de SLDB [active] - _Describe the concrete result this task must produce._

Producir un relevamiento estructural del sistema actual usando AST, dependencias, hubs y flujos reales.
- Definir arquitectura objetivo modular de SLDB [active] - _Describe the concrete result this task must produce._

Definir bounded contexts, contratos entre componentes y criterio de separación para una arquitectura más modular.
- Diseñar estrategia de extracción y modularización [active] - _Describe the concrete result this task must produce._

Definir slices de migración, paquetes candidatos y estrategia para sacar legacy del árbol activo y dejarlo sólo en git.
- Ejecutar refactor base del núcleo SLDB [active] - _Describe the concrete result this task must produce._

Implementar los primeros cortes estructurales: romper ciclos, extraer servicios de dominio y adelgazar el CLI.
- Define SLDB addressability model [active] - _Describe the concrete result this task must produce._

Define how meaningful document units in SLDB receive stable or derivable addresses so they can be queried, updated, composed, and exported with provenance.
- Design SLDB AST query primitives [active] - _Describe the concrete result this task must produce._

Define the first public query primitives that should operate directly on SLDB document structure rather than on downstream graph semantics.
- Expand SLDB composition modes [active] - _Describe the concrete result this task must produce._

Design a broader composition model for SLDB so composition covers more than current transclusion and render-time child summarization.
- Tighten semantic export provenance contract [active] - _Describe the concrete result this task must produce._

Clarify what provenance and structure SLDB must preserve when exporting graph-ready knowledge to downstream systems such as KGDB.
