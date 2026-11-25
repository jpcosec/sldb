FILE:desk/tasks/task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam.md
---
sldb:
  by: agent
  at: '2026-11-16T05:14:49Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md
depends_on: []
pills: []
files:
- docs/versionado-y-colaboracion.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
---

# Decisión de JP: cómo se resuelve un conflicto de git en los índices derivados de .sldb (store_index.yaml y models/*.yaml)

## Rationale

_Explain why this task exists or the business driver behind it._

.sldb/core/store_index.yaml (store_hash) y .sldb/core/models/<Modelo>.yaml (roster_hash, documents_count) son los niveles del Merkle derivados de los shards de documents/ (documents_hash._hash_b, hashing.hash_model_layer, ops.cascade_store_hash). Cualquier escritura reescribe esas líneas, así que dos ramas que tocan documentos distintos siempre chocan en store_hash aunque los shards se mezclen limpios. sldb stores update arranca con load_store_index (src/sldb/store/io/__init__.py:79), que falla con marcadores de conflicto; en a3514755 se quitaron a mano. No hay .gitattributes ni merge driver. Hueco 2 de la nota: stores build sin store.yaml. Pasa en cada rebase de mepu y en cada integración de SLDB_1. Cambia qué se versiona en git, por eso es del dueño. Origen: desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md.

## Goal

_Describe the concrete result this task must produce._

JP elige una opción y queda escrita en docs/versionado-y-colaboracion.md, sección "Conflictos en los índices derivados", con la fecha; se crea con deskops add task la tarea de código que la implementa.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones con su costo: (a) sldb stores update reconstruye store_index.yaml y models/*.yaml desde los shards cuando no se pueden leer (marcadores de conflicto): un comando resuelve el conflicto, git sigue versionando los derivados; (b) un merge driver de git declarado en .gitattributes que regenera esos archivos durante el merge (automático pero requiere configurar git en cada clon); (c) dejar de versionar los derivados y regenerarlos al leer (sin conflictos; cambia la regla de que .sldb/core va en git, ver el atom atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past). Recomendación del coordinador: (a), por ser local a sldb y reversible. Registrar el recibo owner (dispose accepted de JP), escribir la sección y crear la tarea de código con tests en tests/store/test_update_fault_tolerance.py y tests/store/test_merkle_shards.py. No entra: implementar; el hueco 2 (stores build sin store.yaml) entra en la tarea de código si JP elige (a) o (b).

Precisiones (preflight-1): la sección conserva las tres opciones con su costo y marca la elegida. Si JP elige (a) o (b), la tarea de código que se crea incluye en su scope el hueco 2 (stores build sin store.yaml) con su propio test, y su done_when lo nombra.
Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la nota, docs/versionado-y-colaboracion.md y el atom citado. 2) Pedir la decisión a JP. 3) Escribir la sección. 4) Crear la tarea de código con deskops add task y references a esta nota.

## Validation

_List the checks required before this task can close._

- grep -n 'Conflictos en los índices derivados' docs/versionado-y-colaboracion.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción y la fecha; recibo owner aceptado por JP; la tarea de código existe en desk/tasks; commit del doc.

FILE:desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 'Atomize: break the work into the smallest possible child tasks.'
- 'Dedupe: merge overlapping items.'
- 'Clean: delete legacy content that the work makes obsolete (with deskops retire,
  closeout or drawer remove, never by hand).'
- 'Audit existing work before claiming anything is done: check git history for relevant
  commits, verify artifacts exist where specified, and run tests to confirm the current
  state.'
- Resolve contradictory end states between the desk and the repo.
- Bind the pills the task depends on (the task's pills field or deskops bind).
- Keep the Board current; deskops maintains it, so use deskops verbs instead of editing
  it.
- 'Execute with explicit boundaries: scope, touched files and validation targets stated
  in the task.'
- 'After each step, run the context audit: is every aspect of the task covered by
  a pill, are the bound pills still accurate, update or retire the stale ones, and
  bind new ones as needed.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Execution ritual

## Purpose

_Explain why this ritual exists._

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for sldb.

## Trigger

_State when this ritual should start._

Before starting any task, and after each step while implementing it.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-execution gate: ask whether any aspect of the task is ambiguous or not covered by its task file, pills and atoms. If not, proceed. If so, create or request the missing context first; do not proceed until the task is unambiguous.
- The Board (desk/tasks/Board.md) is the single entry point for active work: read it before starting any task.

## Validation

_List the checks that prove the ritual was performed correctly._

- Scope, touched files and validation targets are explicit in the task.
- Every desk reference points at durable repo context: task files, pills, atoms, drawer notes, inbox messages, source files, tests, docs and commits.

## Failure Modes

_List common mistakes this ritual prevents._

- Proceeding with an ambiguous task without creating or requesting the missing context.
- Creating implementation artifacts instead of referencing existing pills.
- Referencing surfaces below the current layer.
- Desk documents pointing at chat memory or other non-durable context.
- Trusting the task file over the code: the task file describes intent; git history is truth.

## Completion

_Describe what completion looks like._

The task's change is implemented within its stated scope and the testing ritual can start.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# Ordered prose steps; not document references
steps:
- 'Invalidate: check whether existing tests are broken by the change; update or delete
  the ones that no longer describe the behavior.'
- 'Verify: add new tests where the change needs them.'
- 'Test: run the relevant test or validation suite, smallest first, then the full
  suite when shared behavior changed. All required checks must pass.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Testing ritual

## Purpose

_Explain why this ritual exists._

No task is complete without testing. Run the smallest relevant validation first, then broaden coverage when sldb changes shared behavior.

## Trigger

_State when this ritual should start._

When the implementation of a task is done, before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- All required checks pass: the test suite, plus stores check, tools/check.sh and tools/check_claims.py when the change touches the store, the gates or documented claims.

## Failure Modes

_List common mistakes this ritual prevents._

- Skipping tests to get it done.
- Declaring a check green from truncated output (a pipe through tail hides the exit status).

## Completion

_Describe what completion looks like._

Every required check passes on the final change.

FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- Update the CHANGELOG when the change is user-visible or release-relevant.
- 'Run the context audit: check the task''s pills, update stale ones, and retire the
  ones whose knowledge now lives in code or docs.'
- 'Close the task with deskops closeout (commit, or supersede/retire when it was already
  resolved): the task leaves the Board in the same atomic commit as its evidence.
  Completed tasks are not kept on the Board.'
- 'Commit atomically, only when the execution ritual is complete. Commit when a phase
  or slice objective is fully checked (a concise scoped message), for a critical bug
  fix mid-phase (fix(<scope>): <description>), or for chores such as dependencies
  or config (chore(<scope>): <description>). A slice that is not done is not a commit:
  work in progress is not committed.'
- 'Write commit messages as <type>(<scope>): <description>, with type one of feat,
  fix, docs, refactor, chore, test, perf, and scope the smallest accurate repo area,
  component, command or workflow surface.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Closeout ritual

## Purpose

_Explain why this ritual exists._

Close a sldb task only after validation passes, the board is updated, and the final change is ready to commit.

## Trigger

_State when this ritual should start._

When the testing ritual passes for a task.

## Preconditions

_List the conditions that must hold before running the ritual._

- Pre-completion audit, git history: the commits match the completed work; on a mismatch, correct the commit history or update the task state to reflect reality.
- Pre-completion audit, artifacts: every specified output exists at the specified location; implement the missing ones.
- Pre-completion audit, tests: all pass; fix failing tests first.
- Pre-completion audit, clean tree: every untracked file is either gitignored or tracked; clean up a dirty tree before declaring done.
- Trust the code, not the task file: the task file describes intent, git history is truth.

## Validation

_List the checks that prove the ritual was performed correctly._

- deskops closeout verify reports the tests, commit and atom gates as passing, and the tree is clean.

## Failure Modes

_List common mistakes this ritual prevents._

- Marking a task complete without auditing git history.
- Committing with untracked files (gitignore or track them first).
- Force-pushing to hide failures.
- Committing work in progress.

## Completion

_Describe what completion looks like._

The closing commit exists, the task is off the Board, and the tree is clean.

FILE:desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 'Compile: rebuild when applicable (bundles, dist).'
- 'Audit: run the relevant tests and quality checks.'
- 'Regress: fix any test failure.'
- 'Flow: move the pill knowledge that is still needed into code or docs, capture phase-level
  learning into an atom, and retire the redundant pills.'
- 'Advance: clear the Board for the next phase and move on.'
# e.g., layer:workflow, system:sldb
tags:
- workspace:desk
---

# Phase ritual

## Purpose

_Explain why this ritual exists._

Close the active phase only when every task on the sldb board is complete, capture any phase-level learning into an atom, and clear the board for the next phase.

## Trigger

_State when this ritual should start._

When every task in a phase or delivery slice is done.

## Preconditions

_List the conditions that must hold before running the ritual._

- 

## Validation

_List the checks that prove the ritual was performed correctly._

- Tests and quality checks pass and no pill repeats what code or docs already say.

## Failure Modes

_List common mistakes this ritual prevents._

- 

## Completion

_Describe what completion looks like._

The Board holds only the next phase's tasks.

FILE:desk/atoms/atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past.md
---
id: atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
title: The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git
  history is the past
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-layout
- topic:journal
---

# The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git history is the past

## Answer

An sldb store is two sibling directories at the repo root: .sldb/ holds store.yaml and core/ (store_index, models, documents) and is versioned in git; .sldb_cache/ holds everything derived (edges, sections, semantic, graphs, caches, locks), is git-ignored and is rebuilt by stores build. There is no journal: the past of a store is asked of git history (sldb docs history). stores check fails with stores/core_ignored when core/ or store.yaml are ignored and alerts with stores/cache_not_ignored when the cache line is missing; stores migrate-layout moves an old .sldb/runtime/ into .sldb_cache/. Owner decision of 2026-10-29.

FILE:docs/versionado-y-colaboracion.md
# Versionado y colaboración en sldb serve

Investigación previa al protocolo de edición concurrente (modelo ProseMirror collab):
una autoridad central que acepta/rebasa según versión. Este documento responde con
evidencia del código actual; no implementa el protocolo.

## 0. Estado del transporte hoy (2026-09-21, rama main)

- Lectura: `GET /health /schema /graph /document?id= /document/ir?id= /edges/* /graph/* /models /lint /semantic-export`.
- Escritura (todos bajo `SAVE_LOCK`, optimistic-lock por payload): `POST /save` (single + batch),
  `POST /docs/create|track|untrack`.
- `/save` usa control optimista por `expected`: el cliente manda el payload que cree que hay
  (`save_plan.update_target`: `existing.payload != expected -> 409`). Detecta el conflicto pero
  no lo resuelve: el segundo cliente debe recargar y rehacer su edición.

## 1. Qué hay hoy (inventario con evidencia)

### Hashes del store (`src/sldb/store/hashing.py`, `store/ops.py`, `store/documents_hash.py`)

| hash | firma | donde vive | cuando rota |
|---|---|---|---|
| `store_hash` (alias deprecado `hash_a`) | root de todo el store: SHA-256 de `[{name, model_hash}]` ordenado (`hash_models_layer`) | store index | cualquier write en cualquier modelo |
| `model_hash` (alias deprecado `hash_b`) | por modelo: SHA-256 de `[{name, source_hash, content_hash}]` ordenado (`hash_document_entries`, order-independent) | models index | cualquier write de cualquier doc del modelo |
| `source_hash` (alias deprecado `hash_c`) | contenido: SHA-256 del texto markdown (`hash_text`) | documento shard | cualquier reescritura del archivo |
| `content_hash` (alias deprecado `hash_d`) | campos: SHA-256 del JSON del payload extraído, claves ordenadas (`hash_payload`/`hash_fields`) | documento shard | solo cuando cambian los campos |

Los cuatro valores conservan su nombre viejo (`hash_a`..`hash_d`) como alias de lectura:
un store viejo sigue cargando y la primera escritura, o `sldb stores migrate-hashes`,
reescribe las claves nuevas. Los valores no cambian con el renombre.

`hash_d` es **función pura del payload**: `hash_payload(codec.extract(model, markdown))`.
Dos prints del mismo payload → mismo `hash_d`; un cambio de campo lo rota siempre. Se calcula en
`ops.track_document` y en `payload_save_steps.write_rendered_document`.

### Journal: retirado el 2026-11-04

El journal (un YAML por write en `.sldb/runtime/journal/`, encadenado por hash) fue retirado:
`.sldb/core/` se versiona entero y el pasado del árbol es la historia de git de sus shards
(`sldb docs history <doc>`, `git log -- .sldb/core/`). Ninguna escritura lo produce,
`sldb stores migrate-layout` borra el que un store tenía y `sldb journal show` imprime el aviso
([architecture/journal-authority.md](architecture/journal-authority.md)).

### Pasos de una escritura (`payload_save_steps.py` + `payload_save.py`)

`save_document_payload`: render (`render_checked`: render + roundtrip obligatorio) →
`write_rendered_document` (escribe `.md`, recalcula `hash_c`/`hash_d` al shard) →
`save_document_indexes` (bajo `store_lock`: shard, `hash_b`, semantic/sections/edges rebuild,
`cascade_hash_a`) → `record(...)` al journal con todo el before/after.

`payload_diff.changed_paths`/`field_label` ya nombran los campos cambiados entre dos payloads
(eso alimenta `entry.field` del journal). `payload_path_writing` ya tiene `deep_get/deep_set/deep_delete`.

## 2. Respuestas con evidencia

### (a) ¿Existe un «número de versión por documento» que sirva como «la versión que el cliente tiene»?

**No existe ningún contador ni versión entera por documento.** No hay campo version en
`DocumentEntry`, ni en `RuntimeDocument`, ni en el documento shard.

**El token que cumple el rol sin inventar nada es `hash_d`** (la firma de los campos):

- Es una función pura del payload → dos clientes con el mismo payload tienen la misma versión;
  el `expected` de hoy (comparación de payloads) coincide exactamente con comparar `hash_d`.
- Ya vive en el documento shard, ya rota en cada write, ya está _before/after_ en el journal.
- El cliente no necesita calcularlo: el servidor lo expone y el cliente lo devuelve tal cual.
- `hash_c` también sirve (firma del contenido) pero es más débil: depende del markdown como bytea,
  no de los campos; un re-render con otro template lo rota sin cambio semántico. `hash_d` es la
  firma semántica y la que alinea con la semántica actual de `/save`.

### (b) ¿El journal permite INVERTIR una escritura o solo auditarla?

**Hoy solo audita.** Evidencia:

- `verify_chain` solo valida la cadena; `read_entries` solo lista. No existe
  función de replay ni de `apply` inverso.
- Para `save_document_payload` la entrada **sí** trae `previous_value` (el payload completo
  anterior) y `hash_d_before`; un single-step undo es *posible a mano* (re-save de
  `previous_value`), pero nada lo ejecuta.
- Para `create_document`/`track_document_file`/`untrack_document` **no alcanza**: `create` y
  `track` no registran payload previo, `untrack` registra solo hashes before (el contenido del
  shard borrado no está en el journal; solo sobrevive el `.md` en disco).
- El journal es opcional (`SLDB_JOURNAL_OFF=1`): no puede ser fuente de verdad del estado.

Conclusión: el journal es **log de auditoría** (quién, qué, antes/después, encadenado y
verificable); habilita undo de un solo paso solo para saves completos, reconstruyendo
manualmente desde `previous_value`, pero no reconstruye estados arbitrarios del store.

### (c) ¿Qué falta para que `/save` acepte `{doc, base_version, changes}`?

Ya existe casi todo; faltan tres piezas pequeñas en el transporte:

1. **Leer la versión actual del doc en el handler de save**: `doc_hashes(store_path, model, doc)`
   (shard) da `hash_d` barato — de hecho hoy se podría comparar `base_version` contra el
   `payload` ya cargado por `load_runtime_documents`. Necesita: comparar
   `base_version != current_hash_d` y en ese caso responder 409 **con el doc completo actual**
   (`serialize_document` + `version`), que ya existe tras esta ronda.
2. **Aplicar `changes` como parches de campos**: el transporte puede resolver `changes`
   = lista de `{op: set|delete, path, value}` contra el payload base del cliente usando
   `deep_set`/`deep_delete`, y luego escribir con `save_document_payload` (render+roundtrip
   ya garantizado). El `field` del journal ya se deduce con `payload_diff`.
3. **Responder la versión resultante**: `hash_d_after` del shard (o del journal del write),
   para que el cliente rebase sin recargar. Hoy `/save` responde `{ok, doc}` sin versión.

Nada del motor del store cambia: sigue siendo `save_document_payload` + journal. El modo
actual `{doc, payload}` (sin `base_version`) debe seguir funcionando (compatibilidad).

## 3. Implementado en esta ronda (solo aditivo)

- `sldb.api.documents.serialize_document` (contrato compartido) ahora emite
  `"version": <hash_d del documento>` — leído del shard vía `api.journal.doc_hashes`.
  Única clave nueva; shape existente intacta.
- Como consecuencia, la versión aparece en:
  - `GET /graph` → cada documento trae `version`.
  - `POST /docs/create|track` (doc recién escrito) y `POST /docs/untrack`
    (versión capturada antes de borrar el shard; bug de orden detectado y corregido por test).
- `GET /document` / `GET /document/ir` **no** incluyen `version`: su envelope lo serializa
  `_flat()` en `src/sldb/cli/serve/document_routes.py`, archivo de otro agente en curso
  (fuera de mi alcance). El cliente del protocolo la toma de `/graph` o de la respuesta de
  los writes; pendiente de coordinar con el dueño de esa ruta.
- Tests: `tests/test_serve.py` +25 (lifecycle completo con versión, rotación de `version`
  tras un `/save`, contratos de error 400/404/409/422).

## 4. Propuesta concreta de protocolo (vuelta siguiente)

```jsonc
// Cliente -> servidor
POST /save
{ "doc": "atom-x",
  "base_version": "<hash_d que el cliente tiene>",
  "changes": [ {"op": "set", "path": "title", "value": "..."},
               {"op": "delete", "path": "obsolete" } ] }

// Servidor, si base_version == hash_d actual del doc (acepta)
200 { "ok": true, "doc": { "...": "...", "version": "<hash_d_after>" } }

// Servidor, si difiere (rebasa)
409 { "ok": false, "error": "Conflicto. Recarga sobre la versión vigente.",
      "doc": { "id": ..., "model_name": ..., "path": ..., "version": "<hash_d actual>",
               "payload": { ... }, "semantic_tags": [...] } }
```

Reglas propuestas:

- El cliente **nunca mergea solo**: ante 409 muestra el payload vigente (va en el cuerpo del
  409) y la UI decide rebasar manualmente (o re-aplicar sus cambios encima y reintentar con la
  nueva `base_version`).
- `changes` se resuelve contra el payload **base del cliente** (no contra el del servidor):
  evita dependencia de orden de llegada; el servidor valida el resultado final con el modelo.
- Tolerancia de reloj nula (no hay timestamps): el `base_version` ES el token de orden.
- Modo legacy `{doc, payload}` sin `base_version` se mantiene (equivalente a `changes=[]`
  con `expected=payload` actual).
- `hash_c` no se usa para el conflicto; queda para detectar ediciones *fuera de banda* del
  `.md` (cambio de hash_c sin cambio de hash_d) en un futuro aviso, no bloqueo.

Trabajo pendiente detectado (fuera de alcance): decidir con el dueño de `document_routes.py`
si el envelope de `/document` debe emitir `version` para que un solo endpoint alimente al
cliente; y que `/save` devuelva la versión resultante (la vuelta siguiente lo necesita).

## 5. Validación real

- `python3 -m pytest tests/test_serve.py -q` → **25 passed**.
- `python3 -m pytest tests/ -q` → **4 failed, 952 passed**; los 4 fallos son **pre-existentes**
  a esta ronda (idénticos a la baseline anterior): `selfdoc/test_preflight.py::test_invalid_existing_document_prevents_any_sync`,
  `test_clean_code_rules[sldb/selfdoc/python_relation_registry.py]`,
  `test_clean_code_rules[sldb/cli/commands/selfdoc.py]`, `test_cli_v2::test_find_supports_physical_and_semantic`.
- Clean-code gate sobre los archivos tocados: OK.
- curl real contra `AgentsKBs/knowledge_psp` (servidor propio en `:8311`, código nuevo;
  el de `:8310` corre un snapshot anterior):
  - `GET /graph` → 168 documentos, cada uno con `version` (ej.
    `atom-antonia-aplicacion -> 272e83a3…c1258ac`).
  - `GET /document?id=atom-antonia-bienvenida` → envelope `{id, model_name, path, payload, semantic_tags, ir}`
    **sin** `version` (ruta de otro agente, ver §3).

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'Conflictos en los índices derivados' docs/versionado-y-colaboracion.md

