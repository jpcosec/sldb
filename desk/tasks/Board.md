---
# board-xxx
id: board-sldb-desk
# Affected workspace or domain
scope: sldb-local-desk
# List of task-xxx paths
tasks:
- desk/tasks/task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field.md
- desk/tasks/task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia.md
- desk/tasks/task-gd27-espacios-de-nombres-y-jerarquía-de-tags-reemplazo-de-texto-en-documentos-trackeados.md
- desk/tasks/task-gd22-referencias-entrantes-buscar-y-reescribir.md
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
- GD27: Espacios de nombres y jerarquía de tags; reemplazo de texto en documentos trackeados [draft] - StoreDeclaration gana tag_namespaces ({name, hierarchical, folder_axis, anchored_by}); un store que los declara rechaza al escribir un tag de namespace no declarado y un tag jerárquico sin ancla para cada prefijo; sldb.api.tag_tree y tag_folder; sldb.api reexporta sldb.api.semantic; CLI sldb tags namespaces|tree|check; sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None) con conteo exacto, re-extracción, validación contra el modelo y re-track dentro de sldb.api.transaction; CLI sldb docs replace con envelope; docs/architecture/tags.md y sección en transactions.md.
- GD22: Referencias entrantes - buscar y reescribir [draft] - sldb.api.referrers(store, target) devuelve las referencias entrantes (campos escalares, elementos de listas y menciones en superficies no modeladas) desde el índice y el grafo de proyecto de GD21; sldb.api.rewrite_references(store, target, replacement | None, *, transaction=None) las reescribe o quita dentro de una transacción de GD24 (todo o nada) y devuelve un RewriteReport; CLI sldb edges referrers y sldb edges rewrite --to | --remove [--dry-run] con envelope; GET /edges/referrers y POST /edges/rewrite; docs/architecture/references.md.
