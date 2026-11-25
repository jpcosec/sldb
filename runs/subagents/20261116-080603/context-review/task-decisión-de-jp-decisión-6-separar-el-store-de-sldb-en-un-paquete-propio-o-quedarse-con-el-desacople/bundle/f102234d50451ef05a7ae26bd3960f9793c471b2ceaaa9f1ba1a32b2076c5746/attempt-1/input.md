FILE:desk/tasks/task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople.md
---
sldb:
  by: agent
  at: '2026-11-16T07:56:17Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-pill-standards-md-es-un-documento-modelado.md
files:
- docs/architecture/store-extraction-proposal.md
- desk/STANDARDS.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md
---

# Decisión de JP (decisión 6): separar el store de sldb en un paquete propio o quedarse con el desacople interno

## Rationale

_Explain why this task exists or the business driver behind it._

El desacople del store dentro de sldb está hecho (beb8a99c): el store depende del resto de sldb solo por tres costuras (src/sldb/store/exceptions.py, src/sldb/store/runtime_codec.py, src/sldb/store/model_contract.py) y tests/test_store_seams.py lo hace cumplir. Separarlo en un paquete propio solo tiene sentido si el dueño decide que el store sea un motor genérico de documentos tipados para sldb, deskops, knowledge y repopackage. Esa es la decisión 6, pendiente según desk/STANDARDS.md:19. Spec: docs/architecture/store-extraction-proposal.md. Origen: drawer desk/drawer/tasks/task-separar-el-store-en-un-paquete-propio-espera-la-decisi-n-6.md.

## Goal

_Describe the concrete result this task must produce._

JP toma la decisión 6: (a) separar: se crea la tarea de refactor que inyecta las tres costuras y crea el paquete con su pyproject y su suite; o (b) quedarse con el desacople interno. La decisión queda escrita en docs/architecture/store-extraction-proposal.md, sección "Decisión 6", con fecha, y desk/STANDARDS.md:19 deja de decir que está pendiente (vía la CLI que corresponda o en el commit del doc si STANDARDS.md no es un documento modelado).

## Scope

_State what is in scope and what is out of scope._

Entra: presentar la decisión con el estado (costuras listas, test verde) y la recomendación del coordinador: (b) hasta que un segundo consumidor necesite el store sin sldb. Registrar el recibo owner (dispose accepted de JP), escribir la sección y crear la tarea si es (a). No entra: mover código.

Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.
Precisiones (preflight-1): desk/STANDARDS.md no es un documento modelado por deskops (no está en el store), así que se edita en el mismo commit que el doc: la línea que dice que la decisión 6 está pendiente pasa a decir "Decisión 6 (AAAA-MM-DD, JP): <opción>; ver docs/architecture/store-extraction-proposal.md". La recomendación es insumo para JP, no decisión por defecto.

Referencia kimun (solo lectura, github jpcosec/kimun main b14a30f): kimun es un solo producto (doc v2 de kimun 08-distribucion.md:11, "kernel SLDB v2 y modelos", un binario y un jar; deps.edn con un solo :paths) desacoplado por anillos que un script hace cumplir (doc v2 de kimun 03-estandares-de-codigo.md:10-17, bb lint / scripts/check_rings.clj). La separación que kimun planea no es "el store como motor genérico de documentos", sino base frente a grafo: "el grafo es un paquete aparte de la base" (05-estado.md:120, decisión 43). Y "kimun no tiene consumidores en código" (12-ecosistema-y-pendientes.md:71). Recomendación para que JP confirme: (b), quedarse con el desacople interno, que sldb ya hace cumplir con tests/test_store_seams.py y contracts/layers.toml. Se reabre si aparece un segundo consumidor que necesite el store sin sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/architecture/store-extraction-proposal.md y desk/STANDARDS.md. 2) Pedir la decisión. 3) Escribir la sección y actualizar STANDARDS.md. 4) Crear la tarea de refactor si es (a).

## Validation

_List the checks required before this task can close._

- grep -n 'Decisión 6' docs/architecture/store-extraction-proposal.md
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la decisión y la fecha; STANDARDS.md ya no la da por pendiente; recibo owner aceptado por JP; tarea de refactor creada si es (a); commit.

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

FILE:desk/contexts/pill-pill-standards-md-es-un-documento-modelado.md
---
sldb:
  by: agent
  at: '2026-11-16T07:55:57Z'
  authority: generated
  via: create_document
# pill-xxx
id: pill-pill-standards-md-es-un-documento-modelado
status: active
summary: STANDARDS.md es un documento modelado
# e.g., language:python, library:pydantic
tags:
- topic:context-review
---

# Pill: STANDARDS.md es un documento modelado

## What

_Define the context or guardrail this pill carries._

Las respuestas del bundle-1 de la tarea: precisiones de implementación que la revisión en frío pidió y que el contrato deja abiertas.

## Why

_Explain why this context matters for safe execution._

La revisión cold-bundle (bundle-1) mostró que sin estas precisiones el ejecutor tendría que inventar estos detalles.

## When

_Describe when an agent should apply this pill._

Al ejecutar la tarea, antes de tocar código.

## Where

_Name the files, surfaces, or scope this pill applies to._

desk/STANDARDS.md, docs/architecture/store-extraction-proposal.md

## How

_Describe the correct way to apply this guidance._

desk/STANDARDS.md está trackeado en el store de sldb y su regla 4 dice que se edita con sldb fields update, no a mano. La línea de la decisión 6 se cambia con sldb fields update sobre el campo que la contiene. Si JP elige (a), la tarea de refactor no inyecta costuras nuevas (el desacople ya está, beb8a99c): crea el paquete y mueve el store detrás de las costuras existentes. La sección del doc se titula exactamente '## Decisión 6'.

## How Not

_Describe the shortcut or failure mode to avoid._

No ampliar el alcance del contrato ni contradecir sus Precisiones; si el código real no cuadra con lo que dice este pill, se detiene y se reporta en result-summary.md.

FILE:docs/architecture/store-extraction-proposal.md
<!-- Traído desde graph_ui/desk/drawer/STORE_EXTRACTION_PROPOSAL.md el 2026-10-18: es el spec de la task de sldb desk/drawer/tasks/task-extract-store-into-generic-typed-document-engine-document-codec-plugins.md. PROJECTION_LAYERING_SPEC.md vive ahora en graph_ui/docs/reference/history/ (graph_ui a196455). -->

# Store genérico — infraestructura de documentos tipados, agnóstica de dominio

Estado: draft. Propone extraer `sldb/src/sldb/store/` a un **store genérico**
donde sldb deja de ser dueño y pasa a ser el primer cliente. El store no sabe
qué es un documento, cómo se serializa ni de qué dominio es: eso lo aportan
consumidores vía plugins (`Document` protocol + `Codec`).

Contexto: `PROJECTION_LAYERING_SPEC.md` (núcleo sldb+kgdb e instancias),
`RELATION_MODEL_LAYER_SPEC.md` (modelo de relación). Este documento redefine
la pieza más baja: el store como infraestructura común de todo el ecosistema.

---

## 0. Tesis

El store no es "la capa baja de sldb". Es un **motor genérico de documentos
tipados**: indexa, consulta y hashea documentos cuyo *tipo* y *formato* define
el consumidor. sldb, repopackage, deskops, knowledge son todos clientes del
mismo store. "Sirve para todo" precisamente porque no sabe para qué se usa.
<!-- gone -->
```
STORE (core agnóstico):  índice + query + hash + integridad + lock
        ▲  inyectan plugins
   ┌────┴───────────────────────────────┐
 sldb        repopackage      deskops      knowledge
 {NL doc,    {contract,       {workflow,   {atom,
  Markdown}   YAML}            models}      Markdown}
```

---

## 1. Qué debe saber el store (y qué NO)

### 1.1 El core SABE de

| Responsabilidad | Qué hace |
|---|---|
| **Indexado** | catálogo de stores/modelos/documentos/secciones + DAG semántico |
| **Consulta** | queries semánticas y estructurales sobre el índice (no globbing) |
| **Hashing por capas** | hash de texto, de campos normalizados y de índice → drift trazable |
| **Integridad / lock** | consistencia del índice, locking de escritura |
| **Persistencia** | leer/escribir el catálogo y localizar documentos |

### 1.2 El core NO SABE de

- **Qué es un documento** — hoy `StructuredNLDoc`; debe ser un protocolo.
- **Cómo se serializa** — hoy Markdown reversible; debe ser un codec plugin.
- **De qué dominio es** — conversacional, workflow, repos: irrelevante al core.

Regla: el core no menciona formato ni dominio en ninguna firma pública.

---

## 2. Los plugins que aporta cada consumidor

### 2.1 `Document` (protocolo)

Reemplaza el acoplamiento directo a `StructuredNLDoc`. El core opera contra
una interfaz mínima: identidad, tags semánticos, payload de campos, path.
Cada consumidor provee su tipo concreto.

### 2.2 `Codec` (render/extract)

Reemplaza el render Markdown embebido. Un codec sabe:

- `extract(raw) -> fields` — de la representación serializada a campos tipados.
- `render(fields) -> raw` — de campos a la representación serializada.

Consumidores y sus codecs:

| Consumidor | Document | Codec |
|---|---|---|
| **sldb** | `StructuredNLDoc` | Markdown reversible (marcadores `⸢rev•⸥`) |
| **repopackage** | `IntegrationContract`, `ComposableUnit` | YAML |
| **deskops** | task / pill / ritual / atom | Markdown / materializador |
| **knowledge** | ConversationStep, DomainAtom… | Markdown reversible |

El hashing semántico (`hash_fields`) funciona para todos: opera sobre los
campos extraídos por el codec, no sobre el formato. Por eso separa "cambió el
significado" de "cambió el formato" en cualquier consumidor.

### 2.3 `resolve_model_ref` (ya inyectable)

Ya se pasa como callable en `load_runtime_documents(..., resolve_model_ref)`.
Es el patrón correcto que debe generalizarse a `Document` y `Codec`.

---

## 3. Estado actual y acoplamientos a romper

- Ubicación: `sldb/src/sldb/store/` (~1857 LOC, subestructura cohesionada:
  `query_engine/`, `models/`, `io/`, `diagnostics_models/`).
- Entrada: ~20 comandos CLI + 2 no-CLI (`links/`) + ecosistema externo vía
  `load_runtime_documents`. **Alta entrada → es núcleo, no hoja.**

### 3.1 Acoplamientos que lo atan a sldb (a cortar)

| Acoplamiento | Usos | Acción |
|---|---|---|
| `sldb.cli.store_context.get_store_context` | 1 (facade) | **inversión de dependencia**: inyectar contexto, no importarlo |
| `sldb.cli.model_utils.resolve_model_ref` | 1 lazy (diagnostics) | inyectar callable (patrón ya existe) |
| `sldb.models.structured_doc.StructuredNLDoc` | 2 | abstraer a protocolo `Document` |
| `sldb.runtime.validation.extract_model_data` | 3 | abstraer a interfaz `Codec.extract` |
| `sldb.core.exceptions` | 10 | mover al core del store (excepciones propias) |

Los dos primeros son inversión de dependencia (store→cli, mala). Los dos
siguientes son la **generalización** (sacar tipo y formato del core). El
último es trivial.

---

## 4. Plan

1. **Cortar `store → cli`** (get_store_context, resolve_model_ref): inyección
   en vez de import.
2. **Abstraer `Document`**: reemplazar referencias a `StructuredNLDoc` por un
   protocolo. sldb registra su `StructuredNLDoc` como implementación.
3. **Abstraer `Codec`**: sacar `extract_model_data` / render Markdown del core
   a una interfaz. sldb aporta el codec Markdown-reversible.
4. **Excepciones propias** del store (dejar de importar `sldb.core.exceptions`).
5. **Mover** `store/` → paquete/carpeta núcleo independiente.
6. **Reapuntar** CLI y `links/` como clientes.
7. **sldb queda como primer cliente**: `{StructuredNLDoc + codec Markdown}`.

---

## 5. Riesgo

- Extracción pura (mover + invertir 2 imports): **bajo**.
- Generalización (Document + Codec): **medio** — toca firmas públicas
  (`load_runtime_documents`, `hashing`, `facade`), pero el patrón de inyección
  ya existe en el código.
- No es "mover una carpeta": es "extraer + generalizar el core para que deje
  de mencionar formato y dominio".

---

## 6. Por qué esto cierra el hilo del núcleo

- **sldb** = store + plugin `{StructuredNLDoc, Markdown}`. Deja de ser dueño.
- **repopackage** = store + plugin `{IntegrationContract, YAML}` → deja de
  reimplementar YAML + `sha256(json.dumps)` + solver ad-hoc sobre archivos
  sueltos (hoy tiene su propia persistencia paralela; ver §7).
- **kgdb** (hoy la capa de grafo de sldb, `sldb.store.graph`) = consume el store para ensamblar el grafo, agnóstico del codec.
- **deskops / spec2viz / knowledge** = store + sus tipos.

El store se vuelve la infraestructura común que `PROJECTION_LAYERING_SPEC.md §7`
pone al centro del ecosistema radial. sldb+kgdb como núcleo se refina: **el
verdadero núcleo es el store genérico**; sldb es la primera instancia de
consumo (NL + Markdown), kgdb el ensamblador de grafo sobre él.

---

## 7. repopackage: cliente latente que reimplementa el store

repopackage hoy **no usa el store** (cero imports de sldb en `src/`). En su
lugar reimplementa un subconjunto pobre:

| Necesidad | repopackage hoy | store genérico |
|---|---|---|
| Modelos tipados | Pydantic a mano (`IntegrationContract`…) | `Document` protocol |
| Persistencia | `yaml.load`/`dump` con `open()` | io + lock + codec YAML |
| Consulta del grafo | `solver.py` recorre YAML | `query_engine` |
| Hash de estado | `hashlib.sha256(json.dumps(...))` | `hashing` por capas |

El `nldb_example/` (un `StructuredNLDoc` de referencia) es la punta de una
integración ya prototipada pero nunca conectada. repopackage es el caso donde
**la ausencia de un store genérico obligó a reinventarlo**: es el mejor
argumento a favor de esta extracción.

---

## 8. Preguntas abiertas

- ¿`Document` y `Codec` son protocolos (duck typing) o clases base abstractas?
- ¿El registro de tipos/codecs es global (un registry por proceso) o por store?
- ¿El paquete se llama `store` genérico, o toma nombre propio para no arrastrar
  la marca sldb?
- ¿El modelo de relación (`RELATION_MODEL_LAYER_SPEC.md`) es un `Document` más,
  o el store necesita primitiva de arista nativa?
- ¿kgdb consume el store directamente, o vía un export intermedio como hoy?
- Migración de repopackage: ¿portar sus modelos a `Document`+codec YAML es un
  cambio incremental o un rewrite?

FILE:desk/STANDARDS.md
# SLDB Desk Standards

## Purpose

This desk exists to make the repo's current operational state explicit, queryable, and durable without mixing every workflow decision directly into generic SLDB infrastructure.

The desk should explain what the repo is trying to deliver next, what local execution rules apply, and what decisions or pills future work should inherit before more code changes happen.

## Task Rules

1. Todo trabajo no trivial tiene una task antes o durante la ejecución.
2. Si la ejecución depende de una decisión de arquitectura local o de una regla recurrente, se escribe una pill o un átomo en vez de confiar en la memoria del chat.
3. Los documentos del desk se crean, editan, cierran y retiran con el CLI de deskops (add, edit, advance, closeout, issue close, drawer remove, retire), no a mano; deskops mantiene el Board y el store.
4. Los documentos que modela este desk (SPEC.md, STANDARDS.md) se editan con sldb fields update.
5. Mantener sldb genérico: si un comportamiento es semántica de workflow del desk, va a deskops.

## Current Priority

Sin deploys (tags, releases ni PyPI) hasta que la suite completa (sldb, deskops, spec2viz, graph_ui) esté lista y testeada en conjunto; la versión 0.1.13 espera en main sin tag. Las decisiones abiertas del dueño están en las notas del inbox y en la task del drawer que espera la decisión 6.

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio-o-quedarse-con-el-desacople: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'Decisión 6' docs/architecture/store-extraction-proposal.md
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py

