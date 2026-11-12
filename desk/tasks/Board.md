---
sldb:
  by: agent
  at: '2026-11-12T02:26:15Z'
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
- desk/tasks/task-main-de-sldb-en-verde-el-workflow-ci-falla-desde-el-2026-10-20-run-42758984024.md
- desk/tasks/task-stores-check-no-aborta-ante-un-documento-que-su-modelo-rechaza-lo-nombra-como-hallazgo-y-sigue-con-e.md
- desk/tasks/task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru.md
- desk/tasks/task-sldb-create-document-y-track-document-file-evalúan-las-reglas-on-write-h4-declare-write-conserva-la.md
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
- main de sldb en verde: el workflow CI falla desde el 2026-10-20 (run 42758984024) [draft] - El workflow CI de sldb (jobs test 3.12/3.13 y store) termina en success sobre main.
- stores check no aborta ante un documento que su modelo rechaza: lo nombra como hallazgo y sigue con el resto (H1 de la nota 3895e9f7); H2 y H3 quedan con tests de regresión [draft] - sldb stores check sobre un store con documentos que su modelo rechaza termina el diagnóstico: cada documento inválido es un hallazgo por documento con su código, el resto del store se diagnostica como hoy y la salida JSON está completa. Además (corrección del 2026-11-12), con caché frío una escritura o un untrack de un documento ya no cae por otro inválido del mismo modelo (H2), y una transacción fallida restaura todo lo que escribió, shards derivados incluidos (H3).
- run_view no compone en cada proceso el índice de aristas de todos los stores enlazados: sldb views run board y deskops view board en menos de 1 s con el store construido (H11) [draft] - Con el store construido, sldb views run board y deskops view board, en un proceso nuevo cada vez, tardan menos de 1 s sobre el desk de deskops con sus stores enlazados; en frío (sin caché de disco) no tardan más que hoy; el resultado y la revision de la vista no cambian.
- sldb: create_document y track_document_file evalúan las reglas on_write (H4), declare --write conserva la declaración de tags (H5), la familia de tags da su evaluación estructurada (H6) y se documenta qué documentos ve (H7) [draft] - create_document y track_document_file evalúan on_write como save (H4); stores declare --write conserva tag_namespaces y tag_models (H5); un hallazgo de la familia de tags lleva su evaluación estructurada y rules check, rules explain y tags check la exponen en su salida JSON (H6); la guía de reglas y de tags dice qué documentos ve la familia (H7).
