FILE:desk/tasks/task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores.md
---
sldb:
  by: agent
  at: '2026-11-11T14:46:01Z'
  authority: generated
  via: create_document
id: task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores
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
- src/sldb/api/stores/
- src/sldb/store/
- src/sldb/api/documents/
- tests/store/
- tests/api/
- docs/
- CHANGELOG.md
- contracts/layers.toml
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-seguridad-resto-rebuild-track-y-check-store-todav-a-leen-archivos-trackeados-sin-la-guarda-de-ra-z-y-symlinks.md
---

# SEGURIDAD (resto): toda lectura de un documento trackeado pasa por la guarda de raíz y symlinks (stores check/update/build, track, rebuild)

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del overlord. Tras la tarea de seguridad live_stale, stores check y stores update todavía abren un documento trackeado que es symlink hacia fuera de la raíz (reproducido sobre sldb main 7b9b1e6d).

## Goal

_Describe the concrete result this task must produce._

Ninguna operación del store abre un documento trackeado que resuelva fuera de la raíz o sea symlink: un solo punto de apertura (source_read), hallazgo nombrado en lugar de error, track rechaza symlinks, con tests de audit hook.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/stores/, src/sldb/store/, src/sldb/api/documents/, tests/store/, tests/api/, docs/, CHANGELOG.md, contracts/layers.toml. Fuera: el comportamiento de stale/rebuild (a2) y la forma de los hallazgos ya existentes.

## Implementation Path

_Outline the expected implementation route or affected surface._

SEGURIDAD, resto de la tarea live_stale (cerrada en 23e4c2b2; drawer de origen 1c3132aa). Prioridad del overlord: cupo 1. La guarda sldb.store.source_read (unreadable_reason + read_source_text con O_NOFOLLOW; eje lectura_de_fuentes) ya protege la lectura del índice de aristas y el diagnóstico de documento de stores check. Quedan otras lecturas de documentos trackeados que la saltean.

REPRODUCCIÓN (coordinador, sldb main 7b9b1e6d; log runs/subagents/20261111-repro-secrest/repro.log y script audit_run.py con un audit hook de 'open'): un desk de prueba con dos tareas trackeadas, una reemplazada por un symlink a /dev/shm/outside-secret2/secreto-externo.md, fuera de la raíz. 'sldb stores check' y 'sldb stores update' abren el archivo de afuera (y fallan con 'Unexpected: 2 validation errors for TaskCodeDoc' al parsear su contenido).

CAUSA (lecturas sin la guarda, a confirmar y completar por grep de read_text/open sobre rutas de documentos trackeados): src/sldb/api/stores/index_refresh.py:82, scan_rewrite_loss.py:21, scan_structural_noise.py:33, src/sldb/store/ops.py:28, section_rebuild.py:73, semantic_doc_tags.py:26, edge_rebuild.py:67 (read_payload), y la extracción de campos que siguen a track/update.

ARREGLO (r1-r5):
r1 (un solo punto de apertura): toda lectura del texto de un documento trackeado (o por trackear desde un path del store) pasa por sldb.store.source_read: primero unreadable_reason(root, path) y después read_source_text(path). Un documento fuera de la raíz o symlink no se lee: el comando lo nombra con el hallazgo existente (store/path-outside-root o store/symlink-not-read) y sigue con los demás. Nada de 'Unexpected' por leer afuera.
r2 (track): 'sldb docs track' de un path que es symlink o resuelve fuera de la raíz se rechaza con error claro antes de abrir el archivo.
r3 (inventario): el informe trae la tabla de cada lectura de documento trackeado en src/ (archivo:línea, antes y después). El grep final de read_text/open sobre rutas de documentos trackeados fuera de source_read queda vacío o con cada excepción justificada (por ejemplo, archivos que no son documentos: store.yaml, pyproject).
r4 (tests de regresión, tests/store/): con el audit hook de 'open' en un subproceso, sobre un store con un documento trackeado symlink saliente: stores check, stores update, stores build, build --check y docs update no abren el archivo de afuera y nombran el hallazgo. docs track de un symlink se rechaza sin abrirlo. Los tests de seguridad existentes (test_live_stale_security.py) siguen verdes.
r5 (límites): tests/test_clean_code_rules.py obligatorio (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites). Un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml. Los grados medidos de unidad se actualizan con comentario fechado si cambian.

VALIDACIÓN: el worker corre los tests que toca, todos los de tests/store y tests/api que pasan por las lecturas cambiadas (grep), test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Tests con audit hook en subproceso: check/update/build/build --check/docs update no abren el symlink saliente y nombran el hallazgo
- docs track de un symlink se rechaza sin abrirlo
- test_live_stale_security y tests de store/api tocados en verde
- test_clean_code_rules y check.sh --fast
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

r1-r5 hechos con causa raíz escrita, inventario en el informe y tests verdes; CHANGELOG y docs.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-seguridad-resto-toda-lectura-de-un-documento-trackeado-pasa-por-la-guarda-de-raíz-y-symlinks-stores: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

