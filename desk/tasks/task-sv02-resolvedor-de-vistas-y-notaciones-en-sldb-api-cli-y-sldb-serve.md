---
id: task-sv02-resolvedor-de-vistas-y-notaciones-en-sldb-api-cli-y-sldb-serve
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- ddc049b4
- 6ba8bb20
- tests/notations/test_notation_view_and_routes.py
- atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve
depends_on:
- task-sv01-modelos-de-vocabulario-visual-paletas-y-notaciones-builtin-en-sldb
pills: []
files:
- src/sldb/api/notations/__init__.py
- src/sldb/api/notations/notation_view.py
- src/sldb/api/notations/projection_view.py
- src/sldb/api/notations/notation_sync.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/notations.py
- src/sldb/cli/parsers/public.py
- src/sldb/cli/commands/notations.py
- src/sldb/cli/serve/notations_routes.py
- src/sldb/cli/serve/routes.py
- docs/architecture/notations-and-views.md
- CHANGELOG.md
- tests/notations/test_notation_view_and_routes.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SV02: Resolvedor de vistas y notaciones en sldb.api, CLI y sldb serve

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo SV02 del plan desk/drawer/plans/absorber-spec2viz-y-modelos-ui (dag.yaml rev 1). Hoy graph_ui importa spec2viz.notation_view.resolve_view y resolve_documents y mantiene su propio evaluador de ViewDoc en projection_views.py. Llevar el resolvedor y la sincronizacion de notaciones/paletas a sldb.api, CLI y sldb serve permite servir vistas diagramaticas y de proyeccion directamente sobre el grafo del store sin depender de spec2viz ni de YAMLs intermedios.

## Goal

_Describe the concrete result this task must produce._

resolve_view, resolve_documents, evaluate_projection_view, sync_notation y sync_palette en sldb.api.notations (reexportados en sldb.api); subcomando CLI sldb notations (list, sync, view, resolve) con envelope JSON; rutas en sldb serve (GET /notations, GET /notations/view, POST /notations/resolve, GET /views/projection, GET|POST /views/projection/evaluate y POST /views/projection/save); docs/architecture/notations-and-views.md y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/notations/__init__.py, src/sldb/api/notations/notation_view.py, src/sldb/api/notations/projection_view.py, src/sldb/api/notations/notation_sync.py, src/sldb/api/__init__.py, src/sldb/cli/parsers/notations.py, src/sldb/cli/parsers/public.py, src/sldb/cli/commands/notations.py, src/sldb/cli/serve/notations_routes.py, src/sldb/cli/serve/routes.py, docs/architecture/notations-and-views.md, CHANGELOG.md, tests/notations/test_notation_view_and_routes.py. Fuera: enriquecimiento de /document/segments (SV03) y vistas tabulares/compuestas con reglas de GD25 (que usan /views/<name>).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 1, SV02): (1) En src/sldb/api/notations/notation_view.py, implementar resolve_view(store, spec_ref, pythonpath=None) y resolve_documents(store, notation_ref, doc_refs, *, relation_refs=None, spec_style=None, pythonpath=None, docs=None) siguiendo el contrato de notacion (§2–§15): casado de glifos por modelo + where_matches sobre payload aplanado, compartimentos con rutas con punto, interpolacion de label y keyword sin dejar {campo} sin resolver, casado de links sobre contains y RelationDoc ordenados por posicion nn, fragmentos UML consecutivos por data.group, estilo resuelto con resolve_style y resolve_line_color, y leyenda (glyphs, links, kinds). (2) En src/sldb/api/notations/projection_view.py, implementar evaluate_projection_view(store, view_or_ref, pythonpath=None), list_projection_views(store, pythonpath=None) y save_projection_view(store, name, view, pythonpath=None, actor=None): evalua las entradas nodes [{model, where}] y RelationFilter(relations, direction) sobre el store y, si la vista nombra una notation, aplica resolve_documents para devolver nodos y aristas estilizados junto con layout, ink y legend. (3) En src/sldb/api/notations/notation_sync.py, implementar sync_palette(store, name_or_path="default") y sync_notation(store, name_or_path) que registran los modelos de SV01 si faltan y escriben PaletteDoc, NotationDoc, GlyphDoc, LinkDoc y RelationTypeDoc en el store. (4) Exponer CLI sldb notations list|sync|view|resolve y rutas HTTP en sldb serve: GET /notations, GET /notations/view?spec=, POST /notations/resolve, GET /views/projection, GET|POST /views/projection/evaluate, POST /views/projection/save.

## Validation

_List the checks required before this task can close._

- pytest tests/notations/test_notation_view_and_routes.py -q sin fallos ni saltados
- sldb notations sync y sldb notations view devuelven JSON con nodes, links, fragments, skipped y legend
- GET /notations/view y POST /views/projection/evaluate en sldb serve devuelven el mismo payload que sldb.api

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de SV02 cumplida, tests en verde, G_SV_VIEW_RESOLVER satisfecho en dag.yaml.
