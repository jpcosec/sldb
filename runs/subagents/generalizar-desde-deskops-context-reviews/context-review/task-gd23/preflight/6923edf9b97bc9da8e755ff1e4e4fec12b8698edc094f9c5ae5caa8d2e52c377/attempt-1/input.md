FILE:desk/tasks/task-gd23-selectores-de-documento-id-prefijo-glob-modelo-where-como-api-de-sldb.md
---
id: task-gd23-selectores-de-documento-id-prefijo-glob-modelo-where-como-api-de-sldb
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
- src/sldb/api/documents/select_documents.py
- src/sldb/api/__init__.py
- src/sldb/store/query_engine/structural_queries.py
- src/sldb/cli/parsers/docs1.py
- src/sldb/cli/parsers/docs2.py
- src/sldb/cli/commands/docs.py
- src/sldb/cli/serve/docs_routes.py
- src/sldb/cli/serve/routes.py
- tests/api/test_select_documents.py
- tests/store/test_queries_expanded.py
- tests/test_linked_structural.py
- tests/test_serve.py
- docs/architecture/selectors.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD23: Selectores de documento (id, prefijo, glob, modelo, where) como API de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD23 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG1. Depende de: nada. Gates requeridos: G_GO04: Payload proyectado al grafo (grafo-operable GO04) cerrado en main de sldb (pending).

## Goal

_Describe the concrete result this task must produce._

sldb.api.select_documents(store, selector, *, expect='many'|'one') con claves ref, prefix, path_glob, model (con herencia), where (sobre la facet payload de GO04, sin Validator.extract) e include_linked, combinadas por conjunción, orden por ruta relativa, error de ambigüedad con candidatos; glob_structural y find_structural pasan por ella sin cambiar su salida; CLI sldb docs select con envelope; GET /docs/select; docs/architecture/selectors.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/documents/select_documents.py (nuevo), src/sldb/api/__init__.py, src/sldb/store/query_engine/structural_queries.py, src/sldb/cli/parsers/docs*.py, src/sldb/cli/commands/docs*.py, src/sldb/cli/serve/docs_routes.py y routes.py, tests, docs/architecture/selectors.md, CHANGELOG.md. Fuera: el lenguaje de predicados (GO05, solo se consume), nombres del caso deskops en src/sldb/, borrar el resolve_selector de deskops (lo hace CC35), superficies no modeladas (GD21).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD23). SCOPE: Función sldb.api.select_documents(store, selector, *, expect="many"|"one") → lista ordenada de {export_id, model, name, path}. Selector = mapa (o string corto equivalente para la CLI) con claves combinables por conjunción: ref (nombre, Model:name, ruta o alias, como doc_status, api/stores/doc_status.py:18), prefix (prefijo de nombre: con expect="one", exacto primero y si no hay, prefijo único; ambigüedad = error que lista los candidatos, la regla de deskops desk_paths.py:24 resolve_selector), path_glob (fnmatch sobre la ruta relativa a la raíz, con ** recursivo), model (model <= X con herencia), where (predicado del lenguaje de sldb evaluado sobre la facet payload de GO04, sin Validator.extract; con GO05 acepta caminos sin cambio de API), include_linked (default false). Orden estable: ruta relativa. expect="one" con cero resultados = error de documento desconocido existente de sldb; con más de uno = error de ambigüedad con candidatos. Solo documentos trackeados (las superficies no modeladas son nodos del grafo de proyecto de GD21, no documentos). glob_structural y find_structural (store/query_engine/structural_queries.py:12,18) pasan a ser casos de select_documents y la CLI query los llama por ahí, sin cambiar su salida. CLI: sldb docs select [--ref R] [--prefix P] [--path-glob G] [--model M] [--where W] [--one], con envelope. sldb serve: GET /docs/select con los mismos parámetros. Doc en docs/architecture/selectors.md.

ACCEPTANCE: En un store temporal con documentos de dos modelos (uno hereda del otro) en dos carpetas: --prefix único resuelve con --one y uno ambiguo falla listando candidatos; exacto gana a prefijo; --path-glob "sub/**/*.md" devuelve solo los de la subcarpeta; --model Base incluye al heredero; --where status = "open" filtra con cero llamadas a Validator.extract (contadas); la combinación de claves es conjunción; --one sin resultados da el error existente de documento desconocido; los goldens de sldb query glob/find no cambian; GET /docs/select responde igual que la CLI; CHANGELOG; docs/architecture/selectors.md; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/documents/select_documents.py, src/sldb/api/__init__.py, src/sldb/store/query_engine/structural_queries.py, src/sldb/cli/parsers/docs*.py, src/sldb/cli/commands/docs*.py, src/sldb/cli/serve/docs_routes.py, src/sldb/cli/serve/routes.py, tests/, docs/architecture/selectors.md, CHANGELOG.md

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Las revisiones en frío las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`; nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de sldb aparte del de grafo-operable (otras áreas: edges, documents, serve, stores). Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor sobre el resultado integrado. Un nodo no cierra con tests rojos ni saltados.
3. Toda capacidad nueva entra con: función pública en `sldb.api` (reexportada en `sldb/api/__init__.py`), comando CLI con envelope JSON, ruta de `sldb serve` cuando el consumidor la necesita, pruebas, entrada en `CHANGELOG.md` y doc en `docs/architecture/`. Nada queda solo en el código.
4. Genericidad: ningún nombre del caso deskops (TaskDoc, Board, ritual, pill, atom, closeout) aparece en `src/sldb/` ni en sus tests, salvo como dato en fixtures. Un grep lo comprueba en la aceptación de cada nodo.
5. Compatibilidad: ninguna salida existente de la CLI ni de `sldb serve` cambia (goldens existentes verdes); lo nuevo es aditivo. Si un nodo necesita cambiar un contrato existente (p. ej. `/save` pasa a ser atómico), lo nombra en su aceptación y en el CHANGELOG.
6. Ante un contrato ausente de un nodo GO no cerrado, el nodo registra la hipótesis en su TaskDoc, implementa la parte que no depende de él y no inventa la API de grafo-operable.
7. Cada nodo, al cerrar, manda nota a deskops (`deskops message send --to deskops --kind suggestion`) con la función, el comando y la ruta nuevos y el código de deskops que quedan sin motivo (tabla de arriba); así se satisface el gate `G_GDxx` del plan de deskops.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06):
q1 (gate): requiere G_GO04 (GO04 promovido en ritual-execution, no cerrado). El despacho espera a que el supervisor lo marque; si GO05 no cerró, where acepta el lenguaje que GO04 deja (regla 6, hipótesis en este TaskDoc).
q2 (archivo de test): tests/api/test_select_documents.py es nuevo; los goldens de query glob/find son los de tests/store/test_queries_expanded.py y tests/test_linked_structural.py.
q3 (base): commit base 6b80df36 de main de sldb.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_select_documents.py
- TMPDIR=/dev/shm pytest -q tests/store/test_queries_expanded.py
- TMPDIR=/dev/shm pytest -q tests/test_linked_structural.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb docs select --prefix P --one --format json sobre el store temporal del test

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con documentos de dos modelos (uno hereda del otro) en dos carpetas: --prefix único resuelve con --one y uno ambiguo falla listando candidatos; exacto gana a prefijo; --path-glob "sub/**/*.md" devuelve solo los de la subcarpeta; --model Base incluye al heredero; --where status = "open" filtra con cero llamadas a Validator.extract (contadas); la combinación de claves es conjunción; --one sin resultados da el error existente de documento desconocido; los goldens de sldb query glob/find no cambian; GET /docs/select responde igual que la CLI; CHANGELOG; docs/architecture/selectors.md; nota de cierre a deskops.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-gd23: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

