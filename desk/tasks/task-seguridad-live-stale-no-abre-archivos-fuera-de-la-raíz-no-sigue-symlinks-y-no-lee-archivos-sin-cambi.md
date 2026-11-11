---
id: task-seguridad-live-stale-no-abre-archivos-fuera-de-la-raíz-no-sigue-symlinks-y-no-lee-archivos-sin-cambi
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
- src/sldb/store/edge_index/live_stale.py
- src/sldb/store/edge_index/compose.py
- src/sldb/store/models/doc_edges.py
- src/sldb/store/
- tests/store/
- tests/api/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-seguridad-live-stale-lee-todos-los-archivos-trackeados-y-sigue-symlinks-fuera-de-la-ra-z-al-cargar-el-ndice-de-aristas.md
---

# SEGURIDAD: live_stale no abre archivos fuera de la raíz, no sigue symlinks y no lee archivos sin cambios al cargar el índice de aristas

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del overlord. Desde GO04 d7eefdeb, cargar el índice de aristas abre y hashea cada archivo trackeado y sigue symlinks fuera de la raíz, antes de que un consumidor (graph_ui) pueda aplicar sus guardas. Bloquea la integración de graph_ui (test_mindmap_workspace_reader).

## Goal

_Describe the concrete result this task must produce._

Cargar el índice de aristas no abre archivos fuera de la raíz, no sigue symlinks y no lee el contenido de archivos que no cambiaron desde el build; tests de regresión con symlink saliente y archivo protegido.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/store/edge_index/live_stale.py, src/sldb/store/edge_index/compose.py, src/sldb/store/models/doc_edges.py, src/sldb/store/, tests/store/, tests/api/, docs/, CHANGELOG.md. Fuera: rebuild y stale global (a2 de la nota).

## Implementation Path

_Outline the expected implementation route or affected surface._

SEGURIDAD (decisión del overlord, 2026-11-11, prioridad sobre CC34). Nota de origen: inbox 9c9dac6b (de la integración de graph_ui).

REPRODUCCIÓN (coordinador; log runs/subagents/20261111-repro-livestale/repro.log; sldb 9c9dac6b): un desk de prueba con dos documentos trackeados. Uno se reemplaza por un symlink a /dev/shm/outside-secret/secreto-externo.md, fuera de la raíz. Un proceso nuevo llama sldb.api.edges.edge_reading.load_edge_index(.sldb, include_linked=False) con un audit hook de 'open'. Abre 26 .md, entre ellos el archivo fuera de la raíz a través del symlink.

CAUSA: src/sldb/store/edge_index/live_stale.py (GO04 d7eefdeb). live_stale corre en cada lectura del índice (compose._with_live_stale) y, por cada documento trackeado, _file_hash hace path.stat() y path.read_text(), siguiendo symlinks, sin comprobar que la ruta resuelta quede dentro de la raíz. El caché _FILE_HASHES es por proceso, así que un proceso nuevo lee todo.

ARREGLO (s1-s6):
s1 (raíz): antes de abrir, path.resolve() tiene que quedar dentro de la raíz del proyecto (is_relative_to(root.resolve())). Un symlink que escapa, o una ruta que resuelve afuera, no se abre ni se hashea: el documento cuenta como stale (moved) sin leerlo y queda nombrado en un hallazgo (store/path-outside-root o similar), sin error.
s2 (sin seguir symlinks dentro de la raíz): un documento trackeado que es symlink, aunque apunte dentro de la raíz, no se lee por esta vía. Se compara con lstat y se marca como stale con su motivo. La decisión es revisable: si rompe un caso real de sldb, el worker lo escribe y propone.
s3 (no leer de más): al cargar el índice no se lee el contenido de un archivo cuyo lstat (mtime_ns, size) coincide con el registrado al construir el shard. Para eso el shard (DocEdges) guarda el stat del build, y si cambia el contrato de DocEdges se migra como en GO04. Solo se hashea un archivo cuyo stat cambió. Con esto, un proceso nuevo sobre un store recién construido no abre ningún .md del proyecto. Es lo que pide graph_ui: sus archivos protegidos no se abren mientras no cambien.
s4 (tests de regresión, tests/store/): con el audit hook de 'open' de la reproducción:
- un symlink trackeado que apunta fuera de la raíz no se abre y su documento sale stale con motivo;
- un archivo dentro de la raíz sin cambios desde el build no se abre en un proceso nuevo (el caso del archivo protegido de graph_ui);
- un archivo editado sí se lee y sale stale como hoy;
- test_stale_shard_hashes.py sigue verde.
s5 (servidores): el informe dice si sldb serve usa load_edge_index y en qué interfaz escucha por defecto (cli/parsers/serve.py: --host 127.0.0.1). Si hay un camino que escuche fuera de localhost por defecto, se avisa enseguida al coordinador.
s6 (fuera): el hueco a2 de la misma nota (rebuild no resuelve la stale de una edición externa; stale es global) no entra aquí; queda en la nota del inbox de sldb.

VALIDACIÓN: los 7 pasos del workflow de sldb (.github/workflows): bash tools/check.sh --fast; pytest, un proceso por archivo; python -m build; make world en pron; sldb stores build en deskops; sldb stores build --check; sldb stores build && sldb selfdoc check. Los corre el coordinador en clon limpio. El worker corre los archivos de test que toca y los de tests/store/ y tests/api/ que usan el índice de aristas.

## Validation

_List the checks required before this task can close._

- Test con audit hook: symlink saliente no abierto y stale con motivo
- Test: archivo sin cambios no abierto en un proceso nuevo; editado sí y stale
- test_stale_shard_hashes y tests de edge_index verdes
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

s1-s5 hechos con causa raíz escrita y tests verdes; CHANGELOG y docs.
