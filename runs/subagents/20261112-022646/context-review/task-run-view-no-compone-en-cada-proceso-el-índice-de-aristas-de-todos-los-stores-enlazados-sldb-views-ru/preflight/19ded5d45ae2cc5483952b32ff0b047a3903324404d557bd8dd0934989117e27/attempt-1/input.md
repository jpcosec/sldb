FILE:desk/tasks/task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru.md
---
sldb:
  by: agent
  at: '2026-11-12T02:26:09Z'
  authority: generated
  via: create_document
id: task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru
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
- src/sldb/api/edges/
- src/sldb/store/edge_index/
- src/sldb/store/io/
- tests/
- docs/architecture/views.md
- CHANGELOG.md
- contracts/layers.toml
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# run_view no compone en cada proceso el índice de aristas de todos los stores enlazados: sldb views run board y deskops view board en menos de 1 s con el store construido (H11)

## Rationale

_Explain why this task exists or the business driver behind it._

H11 de la nota de sldb 9c08039a (hallada por CC34 de deskops), meta de CC52 de deskops. run_view carga el índice de aristas con todos los stores enlazados en cada proceso aunque las secciones del board solo seleccionen documentos locales, y ese índice no persiste entre procesos. En el desk real de deskops, deskops view board tardó 38,4 s, el 95 % en run_view.

## Goal

_Describe the concrete result this task must produce._

Con el store construido, sldb views run board y deskops view board, en un proceso nuevo cada vez, tardan menos de 1 s sobre el desk de deskops con sus stores enlazados; en frío (sin caché de disco) no tardan más que hoy; el resultado y la revision de la vista no cambian.

## Scope

_State what is in scope and what is out of scope._

En alcance: cómo run_view y load_edge_index obtienen el índice de aristas (qué stores y qué shards lee, y si algo de ese trabajo persiste entre procesos), el costo por shard, tests, docs de vistas y CHANGELOG. Fuera: H12 (el mensaje cuando el store no está construido), H13 (la revision depende de cachés del proceso), la ViewDoc de deskops y el contrato de la vista; cualquier cambio en el resultado de una vista.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: nota de inbox 9c08039a (H11). Corre después de la tarea de H1-H3 (stores check no aborta), que toca el mismo índice de aristas en sldb.

REPRODUCCIÓN (coordinador, con caché frío y con el store construido; runs/subagents/20261112-repro-h11/repro.log). Layout en /dev/shm: deskops origin/main d120766d y sus stores enlazados (sldb b965c62d, spec2viz, scion; pron no tiene store), cada uno en un worktree; sldb stores build del store de deskops rc 0; XDG_CACHE_HOME vacío. deskops view board, proceso nuevo cada vez: 9,4 s y 9,7 s. Perfil de sldb.api.run_view en un proceso nuevo: 10,89 s, de los cuales 8,90 s en load_edge_index (run_view.py:72, edge_reading.py:14), 8,86 s en compose_edge_index, cuatro _merge_store, 5067 llamadas a _cached_shard (7,49 s) y 4606 yaml.load (6,06 s). El loader ya es libyaml: lo caro es construir los objetos de miles de shards en cada proceso. A la escala real (~10 000 shards) el informe de CC34 midió 38,4 s.

CAUSA (a confirmar): run_view arma su estado con load_edge_index con los stores enlazados incluidos, sin mirar qué documentos pueden seleccionar las secciones de la vista, y el índice compuesto vive solo en la memoria del proceso.

CAMBIO (h1-h5), el worker mide cada opción antes de elegir y lo dice en el informe:
h1: un benchmark reproducible (script que arma el layout y mide cada corrida), commiteado, que da los números de esta tarea con caché frío y caliente.
h2 (menos trabajo): run_view solo lee los shards de los stores que alguna sección puede seleccionar; un store enlazado se lee solo si una sección o un filtro de la vista necesita sus documentos. El criterio sale de la definición de la vista, no de una lista fija.
h3 (persistir): si h2 no alcanza para menos de 1 s, el índice compuesto (o las contribuciones por store) se guarda en disco, con clave por los hashes de los índices de cada store, y el proceso siguiente lo lee entero. Un store que cambió invalida solo lo suyo. No hay estado compartido nuevo entre procesos que pueda quedar viejo: la clave lo evita.
h4 (costo por shard): solo si h2 y h3 no alcanzan, bajar el costo de construir los objetos de cada shard.
h5: el resultado y la revision de una vista salen iguales antes y después, con los mismos datos; un test lo fija. Un store enlazado cambiado se nota en la siguiente corrida. tests/test_clean_code_rules.py es obligatorio (80 líneas efectivas por archivo, 10 de lógica por función, sin subir límites; un archivo nuevo fuera de una carpeta con eje necesita eje en contracts/layers.toml, y los grados medidos salen de tools/check.sh --fast, no de mezclar números). Docs de vistas y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de sldb de a un archivo desde /dev/shm, test_clean_code_rules y tools/check.sh --fast. Los 7 pasos del workflow de sldb los corre el coordinador. Las reproducciones y las mediciones van siempre con caché frío además del caliente.

## Validation

_List the checks required before this task can close._

- Benchmark commiteado: sldb views run board y deskops view board en proceso nuevo, con el store construido, menos de 1 s sobre el layout de la reproducción
- En frío (sin caché de disco) no más lento que hoy, con el número en el informe
- Test: el resultado y la revision de la vista salen iguales antes y después con los mismos datos; un store enlazado cambiado se nota en la siguiente corrida
- test_clean_code_rules (obligatorio) y tools/check.sh --fast
- suite completa de sldb de a un archivo desde /dev/shm en verde
- 7 pasos del workflow de sldb en clon limpio

## Done When

_Name the observable condition that makes the task complete._

h1-h5 hechos, con las mediciones antes y después en el informe, tests verdes y la suite completa en verde; docs y CHANGELOG actualizados.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-run-view-no-compone-en-cada-proceso-el-índice-de-aristas-de-todos-los-stores-enlazados-sldb-views-ru: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

