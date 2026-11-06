---
# board-xxx
id: board-sldb-desk
# Affected workspace or domain
scope: sldb-local-desk
# List of task-xxx paths
tasks:
- desk/tasks/task-diseño-set-bootstrap-de-modelos-tras-la-convergencia-átomo-field.md
- desk/tasks/task-diseño-jerarquía-de-modelos-de-evidencia-family-o-herencia.md
- desk/tasks/task-gd23-selectores-de-documento-id-prefijo-glob-modelo-where-como-api-de-sldb.md
- desk/tasks/task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction.md
- desk/tasks/task-gd26-scaffold-de-store-desde-carpetas-y-semillas-declaradas.md
- desk/tasks/task-go07-anclas-a-documentos-con-hash-de-contrato.md
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
- GD23: Selectores de documento (id, prefijo, glob, modelo, where) como API de sldb [draft] - sldb.api.select_documents(store, selector, *, expect='many'|'one') con claves ref, prefix, path_glob, model (con herencia), where (sobre la facet payload de GO04, sin Validator.extract) e include_linked, combinadas por conjunción, orden por ruta relativa, error de ambigüedad con candidatos; glob_structural y find_structural pasan por ella sin cambiar su salida; CLI sldb docs select con envelope; GET /docs/select; docs/architecture/selectors.md.
- GD24: Transacción multi-documento en sldb.api y /save atómico (absorbe doc_io.DocTransaction) [draft] - sldb.api.transaction(store) anidable que escribe en el momento y revierte bytes, entradas y shards ante excepción; operaciones create, update (expected_source_hash, expected), delete, move, track, untrack, write_file y record; sldb.api.apply_batch con prevalidación; /save delega en apply_batch y es atómico (rolled_back: true, cambio de contrato en CHANGELOG, DA2); toda ruta de escritura valida contra el modelo (G4); docs/architecture/transactions.md. Produce G_WRITE_API.
- GD26: Scaffold de store desde carpetas y semillas declaradas [draft] - StoreDeclaration gana folders y seeds (modos if_missing y managed; fuentes text, file con pkg: y document con track); sldb.api.scaffold_store(store, *, declaration=None, apply=False, template_root) idempotente con reporte created/rewritten/present/conflicts; sldb.api.build_store ejecuta apply_declaration y luego scaffold_store; CLI sldb stores scaffold [--apply] y stores build con sección scaffold; doc en docs/architecture/store-declaration.md.
- GO07: Anclas a documentos con hash de contrato [draft] - Campos __doc_anchors__ y from: de Provenance con la forma doc:Model:name@sha256:<hash>, validados al escribir y pinneados en el guardado; estados intact/changed/lost; check_doc_anchors(store) -> list[Finding] usado por anchors check; aristas references desde los campos __doc_anchors__; entrada derivada <campo>__anchor_state en la facet payload calculada al leer; docs/architecture/anchoring.md y CHANGELOG.
