---
sldb:
  by: agent
  at: '2026-11-11T09:00:54Z'
  authority: generated
  via: create_document
id: task-h9-run-view-y-list-views-encuentran-una-viewdoc-de-un-store-enlazado-y-leen-su-archivo-desde-la-raíz
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/views/
- tests/api/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-h9-run-view-no-encuentra-una-viewdoc-de-un-store-enlazado-unknown-view-bloquea-cc34-de-deskops-da4.md
---

# H9: run_view y list_views encuentran una ViewDoc de un store enlazado y leen su archivo desde la raíz de ese store

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión del coordinador (DA4 -> B, 2026-11-11), prioridad detrás de seguridad. Las ViewDoc de deskops viven solo en el paquete (DA4, del dueño) y un desk las encuentra por el store enlazado; hoy run_view da Unknown view en todo store que solo enlaza.

## Goal

_Describe the concrete result this task must produce._

run_view, list_views y sldb serve encuentran una ViewDoc de un store enlazado, la leen desde la raíz de ese store por la guarda de lectura y la evalúan sobre el store que llama.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/views/, tests/api/, docs/, CHANGELOG.md. Fuera: la forma del resultado de run_view y los agregados de deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisión del coordinador (DA4 -> B, 2026-11-11): las ViewDoc de deskops viven solo como semillas del paquete (DA4, decisión del dueño), y un desk las encuentra por el store de deskops enlazado. Prioridad justo detrás de la tarea de seguridad live_stale. Desbloquea CC34 de deskops en los desks que no son el repo deskops.

REPORTE (worker de CC34, sldb 1c3132aa; nota de inbox 5ac79287): run_view (y por lo tanto sldb serve GET /views/<x>) sobre un store A que enlaza a un store B que trackea la ViewDoc da 'Unknown view'.

CAUSA (src/sldb/api/views/list_views.py):
- load_view busca f"{VIEW_MODEL}:{name}" en el índice, pero el índice compuesto nombra el nodo enlazado '<link>:ViewDoc:<name>' (por ejemplo 'lib:ViewDoc:board').
- read_view resuelve node.semantics['path'] contra open_store(store_path).project_root, el root del store LOCAL, no el del store enlazado que trackea la ViewDoc.
- list_views compone el índice con include_linked=False, así que tampoco lista las enlazadas.

ARREGLO (v1-v5):
v1 (resolución): load_view busca primero la ViewDoc local ('ViewDoc:<name>'). Si no hay, busca una enlazada ('<link>:ViewDoc:<name>'). Si hay más de una enlazada con el mismo nombre, el error las nombra (ambigua); no elige una.
v2 (archivo): read_view lee el archivo desde el project_root del store que trackea la ViewDoc (el enlazado, para un nodo enlazado). Lee por la guarda de lectura de la tarea de seguridad (sldb.store.source_read: dentro de la raíz de ese store, sin symlinks) si ya está en main; si no, deja un TODO con la referencia a esa tarea. Hoy read_view hace .read_text() sin guarda.
v3 (list_views): lista también las ViewDoc enlazadas, con el nombre calificado cuando hay choque.
v4 (evaluación): la ViewDoc enlazada se evalúa sobre los documentos del store A (el que llama), no sobre los del store B.
v5 (tests, tests/api/): un store A que enlaza a B, con la ViewDoc solo en B. run_view(A, 'board') la encuentra, lee su archivo desde la raíz de B y la evalúa sobre los documentos de A. list_views(A) la lista. Con dos enlazados con el mismo nombre, el error nombra la ambigüedad. Una ViewDoc local gana sobre una enlazada.

VALIDACIÓN: los 7 pasos del workflow de sldb los corre el coordinador. El worker corre los tests que toca, tests/api de views y test_clean_code_rules (límites de 80 líneas efectivas por archivo y 10 de lógica por función; un archivo nuevo necesita eje en contracts/layers.toml).

## Validation

_List the checks required before this task can close._

- Test con store A que enlaza a B y la ViewDoc solo en B: run_view(A) la encuentra y evalúa sobre A
- list_views(A) la lista; ambigüedad nombrada; la local gana
- test_clean_code_rules y tests de views verdes
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

v1-v5 hechos con causa raíz escrita y tests verdes; CHANGELOG y docs.
