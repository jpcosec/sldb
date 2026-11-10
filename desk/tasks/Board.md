---
sldb:
  by: agent
  at: '2026-11-10T04:52:49Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-sldb-desk
# Affected workspace or domain
scope: sldb-local-desk
# List of task-xxx paths
tasks:
- desk/tasks/task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field.md
- desk/tasks/task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia.md
- desk/tasks/task-reglas-rule-graph-no-compone-la-federación-entera-de-stores-enlazados-27-s-por-comando-de-deskops.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-keep-sldb-cli-output-tied-to-document-contracts.md
- desk/contexts/pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops.md
- desk/contexts/pill-keep-template-markers-reversible-at-the-document-boundary.md
- desk/contexts/pill-model-registration-must-be-queryable.md
- desk/contexts/pill-put-a-small-onboarding-surface-before-the-deep-system.md
- desk/contexts/pill-sldb-cli-errors-must-stay-actionable-and-machine-safe.md
- desk/contexts/pill-store-health-is-owned-by-sldb.md
- desk/contexts/pill-stores-init-must-be-idempotent-and-fail-safely.md
- desk/contexts/pill-keep-the-text-layer-and-the-graph-layer-separate-inside-sldb.md
- desk/contexts/pill-context-pills-carry-reasoning-not-a-copy-of-code-or-docs.md
# List of ritual-xxx paths
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
- desk/rituals/phase.md
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

Enruta las tasks activas del desk local de sldb, las pills que las acompañan y los rituales del ciclo de vida.

## Notes

_Add short operational notes about the current routed set._

Activa: task-congelar-journal-autoridad-arbol (diseño, en borrador). La auditoría de documentación de septiembre de 2026 está cerrada: autodocumentación (aca36681), contexto del store y federación (f16688d0), y ownership de AST y secciones (closeout del 2026-10-18). El trabajo diferido vive en desk/drawer/; lo que espera decisión del dueño está en las notas abiertas del inbox.

## Task Details

_Generated from the task references above._

- Diseño: set bootstrap de modelos tras la convergencia átomo/field [draft] - Un documento de decisión en docs/ (SpecDoc o PlanDoc trackeado) que evalúe la propuesta de siete modelos, diga qué se adopta, qué no y por qué, con ejemplos de cada modelo sobre documentos reales del store.
- Diseño: jerarquía de modelos de evidencia (__family__ o herencia) [draft] - Un documento de decisión en docs/ que compare __family__ vs herencia de clases para los modelos de evidencia, con la recomendación y sus consecuencias para deskops (RunDoc, materializaciones, closeout_evidence).
- reglas: rule_graph no compone la federación entera de stores enlazados (27 s por comando de deskops) [draft] - La evaluación de reglas (on_write, on_transition, edges_holding/edges_blocked, rules check/explain) no compone la federación entera de stores enlazados salvo que una regla lo necesite. Los findings quedan idénticos a los de hoy, y un comando de deskops sobre el desk de deskops vuelve a tardar del orden de 1-2 s.
