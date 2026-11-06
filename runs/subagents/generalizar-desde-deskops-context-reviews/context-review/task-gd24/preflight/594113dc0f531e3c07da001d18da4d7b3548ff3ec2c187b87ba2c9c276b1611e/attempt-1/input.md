FILE:desk/tasks/task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction.md
---
id: task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction
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
- src/sldb/api/documents/transaction.py
- src/sldb/api/documents/apply_batch.py
- src/sldb/api/documents/move_document.py
- src/sldb/api/__init__.py
- src/sldb/store/io/rollback.py
- src/sldb/cli/serve/save_routes.py
- src/sldb/cli/serve/save_plan.py
- src/sldb/cli/commands/fields_mutate.py
- src/sldb/cli/commands/fields_save.py
- src/sldb/cli/commands/docs.py
- tests/api/test_transaction.py
- tests/api/test_write_paths_validate.py
- tests/test_serve.py
- tests/test_serve_auth.py
- tests/api/test_api_documents.py
- docs/architecture/transactions.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD24: Transacción multi-documento en sldb.api y /save atómico (absorbe doc_io.DocTransaction)

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD24 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG2. Depende de: nada. Gates requeridos: ninguno.

## Goal

_Describe the concrete result this task must produce._

sldb.api.transaction(store) anidable que escribe en el momento y revierte bytes, entradas y shards ante excepción; operaciones create, update (expected_source_hash, expected), delete, move, track, untrack, write_file y record; sldb.api.apply_batch con prevalidación; /save delega en apply_batch y es atómico (rolled_back: true, cambio de contrato en CHANGELOG, DA2); toda ruta de escritura valida contra el modelo (G4); docs/architecture/transactions.md. Produce G_WRITE_API.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/documents/transaction.py, apply_batch.py y move_document.py (nuevos), src/sldb/api/__init__.py, src/sldb/store/io/rollback.py, src/sldb/cli/serve/save_routes.py y save_plan.py, las rutas de fields update y docs update que el test por ruta delate, tests, docs/architecture/transactions.md, CHANGELOG.md. Fuera: editar src/sldb/api/documents/payload_save_steps.py (lo comparten GO07 y GO08); exponer write_file por HTTP; modo diferido (GP2); nombres del caso deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD24). SCOPE: Context manager sldb.api.transaction(store) → Transaction, anidable: una transacción interna sobre el mismo store se une a la externa y solo la más externa revierte (semántica de deskops doc_io.py:247-273, GP2). Escribe en el momento (lo escrito se lee dentro de la transacción) y, ante excepción, revierte todo: bytes de cada archivo tocado (restaurar o borrar si era nuevo), entradas del store (track/untrack al estado previo) y shards del índice de aristas y del índice de documentos, generalizando store/io/rollback.py:11 rollback_on_error de una operación a la transacción entera; después invalida las cachés (compose, runtime_cache). Un error durante el rollback no se traga: se re-levanta encadenado al original con la lista de rutas no restauradas. Operaciones de Transaction: create(model, name, payload, path=None) (path explícito permitido, dentro de la raíz del store; ausente = default_document_path como hoy), update(ref, payload, expected_source_hash=None, expected=None), delete(ref), move(ref, new_path) (mueve el archivo y re-trackea con el mismo nombre; las aristas se reconstruyen), track(path, model, name=None), untrack(ref), write_file(path, bytes, expected_sha256=None) (archivo no modelado; con expected_sha256 es guarda) y record(path) (registra un archivo que el llamante escribe por su cuenta, para que el rollback lo restaure). Guarda optimista (GP3): expected_source_hash compara con DocumentEntry.source_hash; expected (payload completo) se conserva por compatibilidad; una guarda que falla levanta ConflictError con ref, esperado y actual. Función sldb.api.apply_batch(store, changes) → BatchReport: prevalida todos los cambios (como prepare_batch de cli/serve/save_routes.py:46: round-trip, modelo, guardas) y los aplica en orden create → update → move → delete dentro de una transacción; cualquier falla revierte todo. /save (cli/serve/save_routes.py) delega en apply_batch: mismo formato de request y de respuesta exitosa, mismos 409/422; cambia que una falla a mitad de lote ya no deja completed parcial (500 con rolled_back: true); acepta además expected_source_hash y las acciones move, track, untrack (write_file no se expone por HTTP). No edita api/documents/payload_save_steps.py (lo comparten GO07 y GO08): llama a las funciones públicas de guardado y envuelve sus efectos; si GO08 cerró al promover, una regla on_write error dentro de un lote revierte el lote entero. Doc docs/architecture/transactions.md.

ACCEPTANCE: Un lote de tres cambios cuyo tercero falla (validación inyectada) deja bytes, entradas e índice idénticos a antes (hash de cada archivo tocado, sldb stores check PASS y edges show iguales antes y después); transacciones anidadas: la interna que termina bien y la externa que falla revierten ambas; dentro de la transacción un update se lee con el valor nuevo; move re-trackea con el mismo nombre y las aristas entrantes siguen resolviendo; write_file con expected_sha256 distinto falla sin escribir; expected_source_hash viejo da ConflictError y por HTTP 409; un error en el rollback se re-levanta con la ruta no restaurada; los tests existentes de /save pasan, salvo el caso de falla parcial, que cambia a rolled_back: true y se documenta en CHANGELOG como cambio de contrato (DA2); toda ruta de escritura (sldb fields update, sldb docs update, /save, apply_batch y transaction) valida el payload contra el modelo (G4): un modelo de prueba con un model_validator que rechaza un payload es rechazado por cada ruta, con un test por ruta, y el archivo, la entrada y el índice quedan como antes; si alguna ruta hoy no valida se arregla en este nodo; medición: tiempo de pared de un lote de 20 updates antes (save_routes actual) y después, en la Validation del TaskDoc; docs/architecture/transactions.md; nota de cierre a deskops. Produce G_WRITE_API.

OUTPUT_SCOPE: src/sldb/api/documents/transaction.py, src/sldb/api/documents/apply_batch.py, src/sldb/api/documents/move_document.py, src/sldb/api/__init__.py, src/sldb/store/io/rollback.py, src/sldb/cli/serve/save_routes.py, src/sldb/cli/serve/save_plan.py, las rutas de fields update y docs update que el test por ruta delate (sin editar api/documents/payload_save_steps.py), tests/, docs/architecture/transactions.md, CHANGELOG.md

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
q1 (decisiones): /save atómico es decisión del dueño (DA2) y la validación por toda ruta es G4; ya no son pendientes.
q2 (rutas de escritura): las cinco rutas son sldb fields update, sldb docs update, POST /save, apply_batch y transaction; el modelo de prueba (en tests/, con un model_validator que rechaza un valor) se usa en un test por ruta (tests/api/test_write_paths_validate.py, nuevo). Si una ruta no valida, se arregla en su módulo de CLI o de API sin tocar payload_save_steps.py; si el arreglo exigiera tocarlo, se registra como hipótesis y nota al coordinador de grafo-operable.
q3 (GO08): si GO08 no cerró al despachar, la parte 'una regla on_write error revierte el lote' queda fuera y se anota.
q4 (base): commit base 6b80df36 de main de sldb.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/test_serve_auth.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_documents.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb stores check PASS antes y después del lote fallido en el store temporal
- tiempo de pared de un lote de 20 updates por /save antes y después, registrado aquí

## Done When

_Name the observable condition that makes the task complete._

Un lote de tres cambios cuyo tercero falla (validación inyectada) deja bytes, entradas e índice idénticos a antes (hash de cada archivo tocado, sldb stores check PASS y edges show iguales antes y después); transacciones anidadas: la interna que termina bien y la externa que falla revierten ambas; dentro de la transacción un update se lee con el valor nuevo; move re-trackea con el mismo nombre y las aristas entrantes siguen resolviendo; write_file con expected_sha256 distinto falla sin escribir; expected_source_hash viejo da ConflictError y por HTTP 409; un error en el rollback se re-levanta con la ruta no restaurada; los tests existentes de /save pasan, salvo el caso de falla parcial, que cambia a rolled_back: true y se documenta en CHANGELOG como cambio de contrato (DA2); toda ruta de escritura (sldb fields update, sldb docs update, /save, apply_batch y transaction) valida el payload contra el modelo (G4): un modelo de prueba con un model_validator que rechaza un payload es rechazado por cada ruta, con un test por ruta, y el archivo, la entrada y el índice quedan como antes; si alguna ruta hoy no valida se arregla en este nodo; medición: tiempo de pared de un lote de 20 updates antes (save_routes actual) y después, en la Validation del TaskDoc; docs/architecture/transactions.md; nota de cierre a deskops. Produce G_WRITE_API.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-gd24: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

