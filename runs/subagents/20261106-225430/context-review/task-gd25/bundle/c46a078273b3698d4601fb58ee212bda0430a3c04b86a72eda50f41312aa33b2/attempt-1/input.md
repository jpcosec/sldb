FILE:desk/tasks/task-gd25-vistas-declaradas-viewdoc-servidas-por-sldb-serve.md
---
id: task-gd25-vistas-declaradas-viewdoc-servidas-por-sldb-serve
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gd21-grafo-de-proyecto-aristas-declaradas-y-nodos-fuente-desde-el-índice-de-sldb-declarado-por-datos
- task-gd23-selectores-de-documento-id-prefijo-glob-modelo-where-como-api-de-sldb
pills: []
files:
- src/sldb/models/notation/view_doc.py
- src/sldb/models/notation/view_param.py
- src/sldb/models/notation/view_section.py
- src/sldb/models/notation/view_section_parts.py
- src/sldb/models/notation/view_doc_checks.py
- src/sldb/api/views/__init__.py
- src/sldb/api/views/run_view.py
- src/sldb/api/views/list_views.py
- src/sldb/api/views/view_rows.py
- src/sldb/api/views/view_groups.py
- src/sldb/api/views/view_edges.py
- src/sldb/api/views/view_rules.py
- src/sldb/api/views/view_transitions.py
- src/sldb/api/views/view_revision.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/views.py
- src/sldb/cli/commands/views.py
- src/sldb/cli/parsers/public.py
- src/sldb/cli/dispatcher.py
- src/sldb/cli/serve/views_routes.py
- src/sldb/cli/serve/routes.py
- tests/api/test_views.py
- tests/api/test_view_doc.py
- tests/test_serve.py
- docs/architecture/views.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD25: Vistas declaradas (ViewDoc) servidas por sldb serve

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD25 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG3. Depende de: ['GD21', 'GD23']. Gates requeridos: G_GO05: Lenguaje de predicados unificado (GO05) cerrado en main de sldb (satisfied); G_GO06: RuleDoc, rules check y rules explain (GO06) cerrados en main de sldb (satisfied); G_GO08: Evaluación on_write/on_transition/on_check y edges_blocked (GO08) cerrados en main de sldb (satisfied).

## Goal

_Describe the concrete result this task must produce._

ViewDoc (el de SV01) tipa params y sections y valida al escribir; sldb.api.run_view(store, name, params) ejecuta las secciones (select de GD23, fields, edges, group_by con group_order, rules de GO06, transitions de GO08/GO09) y devuelve {view, params, revision, sections}; revision por hashes de lo leído; CLI sldb views run|list con envelope; GET /views y GET /views/<name> con ETag e If-None-Match → 304, sin tapar /views/projection* de SV02; sin punto de extensión en Python; docs/architecture/views.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/models/notation/view_doc.py y módulos nuevos de tipado en src/sldb/models/notation/, src/sldb/api/views/ (nuevo), src/sldb/api/__init__.py, src/sldb/cli/parsers/views.py y commands/views.py (nuevos) con su registro en public.py y dispatcher.py, src/sldb/cli/serve/views_routes.py (nuevo) y routes.py, tests, docs/architecture/views.md, CHANGELOG.md. Fuera: register_view_provider y campos computed (DA1); cambiar las rutas /views/projection* de SV02; nombres del caso deskops en src/sldb/.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD25). SCOPE: Modelo ViewDoc (GP4): es el ViewDoc de SV01 (plan absorber-spec2viz-y-modelos-ui, sldb.models.notation_models, decisión SV-D3), no un modelo nuevo: GD25 tipa sus campos opcionales params y sections como sigue y agrega la validación; si SV01 no está en main al promover GD25, GD25 espera. Una ViewDoc sin sections es de proyección de grafo (SV02, rutas /views/projection*) y run_view la rechaza nombrándola; el nombre projection queda reservado (una ViewDoc llamada projection es rechazada al escribirla) para que GET /views/<name> no tape las rutas de SV02. Campos: name, params (lista de {name, required, default}), sections (lista ordenada de Section). Section = {key, select (selector de GD23; admite {param} con la sintaxis de sustitución de where_subject), fields (lista de campos de la facet a devolver; * = todos los proyectados), edges (lista opcional de {relation, direction out|in, as} que agrega a cada fila los export_id vecinos por edges_from/edges_to o ProjectGraph.edges_from/to de GD21), group_by (campo opcional; las filas salen agrupadas en el orden de una lista declarada group_order o, si falta, por valor), rules (lista opcional de nombres de RuleDoc: cada fila lleva findings = resultado de eval de GO06 para esas reglas), transitions (opcional {from_field, relation}: cada fila lleva holding = edges_holding con effects y findings (GO08/GO09) y blocked = edges_blocked, partiendo del nodo cuyo id es el valor de from_field)}. Sin punto de extensión en Python (DA1): un hecho que sldb no calcula (p. ej. de git) lo escribe el consumidor como documento del store (en deskops, recibo ReviewDoc kind evidence) y la vista lo lee con select, edges o rules como cualquier otro documento. Validación al escribir una ViewDoc: selectores y where parsean, rules nombran RuleDocs existentes, params referenciados existen. Ejecución: sldb.api.run_view(store, name, params) → {view, params, revision, sections: {key: rows | groups}}; revision = sha256 de los source_hash ordenados de todos los documentos leídos más los content_hash de la ViewDoc y de las RuleDocs usadas (y, si hay grafo de proyecto, su firma). CLI: sldb views run NAME [--param k=v ...] y sldb views list, con envelope. sldb serve: GET /views (lista) y GET /views/<name>?k=v con ETag = revision e If-None-Match → 304. Doc docs/architecture/views.md con un ejemplo neutral de tablero (estados como columnas, tarjetas por campo) sin nombres de deskops.

ACCEPTANCE: En un store temporal con un modelo Item (status, owner, depends_on), un ciclo de vida de prueba (RitualDoc/RelationDoc de prueba o modelos propios) y una RuleDoc: una ViewDoc tablero con group_by status y group_order declarado devuelve las columnas en ese orden; edges agrega depends_on entrantes y salientes; rules agrega findings con la cláusula; transitions devuelve holding con effects y blocked con su finding para un Item bloqueado; un parámetro {owner} filtra; un documento de prueba que hace de recibo de un hecho externo, enlazado a un Item, aparece en la fila del Item por edges sin código del consumidor; grep de register_view_provider y computed en src/sldb/api/views/ vacío; sldb views run y GET /views/<name> devuelven el mismo payload; GET con If-None-Match igual devuelve 304 y tras escribir un Item la revisión cambia; editar la RuleDoc también cambia la revisión; una ViewDoc con selector que no parsea es rechazada al escribirla; una ViewDoc llamada projection es rechazada; run_view sobre una ViewDoc de proyección (sin sections) da error que la nombra; las rutas /views/projection* de SV02 siguen respondiendo igual (sus tests verdes); tiempo de pared de la vista tablero sobre 200 Items en caliente < 1 s en robocop2 (registrado en la Validation del TaskDoc); CHANGELOG; docs/architecture/views.md; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/models/notation_models.py (solo el tipado de params y sections de ViewDoc y su validación), src/sldb/api/views/, src/sldb/api/__init__.py, src/sldb/cli/parsers/views.py, src/sldb/cli/commands/views.py, src/sldb/cli/serve/views_routes.py, src/sldb/cli/serve/routes.py, tests/, docs/architecture/views.md, CHANGELOG.md

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
q1 (gates): G_GO05, G_GO06 y G_GO08 están satisfied; GO09 y GO10 también cerrados en main. GD21 (ProjectGraph.edges_from/to) y GD23 (select_documents) están en main.
q2 (ubicación de ViewDoc): el modelo vive en src/sldb/models/notation/view_doc.py; src/sldb/models/notation_models.py solo lo reexporta y no se edita. El OUTPUT_SCOPE del dag dice notation_models.py: se lee como el modelo ViewDoc donde esté.
q3 (params): hoy ViewDoc.params es dict con default {} (SV01 lo dejó reservado para GD25) y nada en src/ lo usa. GD25 lo tipa como lista de {name, required, default} según el contrato; un valor None o ausente sigue siendo vacío (los ViewDoc de proyección existentes no traen params). Si algún ViewDoc existente del repo o de los tests trae params como mapa, se reporta antes de cambiar el tipo.
q4 (grupo CLI views): no existe; se registra en src/sldb/cli/parsers/public.py y src/sldb/cli/dispatcher.py (como tags en GD27), y tests/test_cli_every_command_has_a_handler.py debe quedar verde sin editarse.
q5 (rules nombran RuleDocs existentes): es una invariante que cruza documentos; el principio del dueño la manda a regla, pero no hay predicado para ella. En GD25 se comprueba al ejecutar la vista (run_view da error que nombra la RuleDoc ausente) y no al escribir la ViewDoc; las validaciones de un solo documento (selectores y where que parsean, params referenciados que existen, nombre projection reservado) son validadores pydantic de ViewDoc. Hipótesis para el dueño.
q6 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.
PRECISIONES DEL PREFLIGHT (review-task-gd25-preflight-1, 2026-11-06):
q7 (rules existentes): manda q5. Al escribir una ViewDoc solo se validan las invariantes de un documento (selectores y where que parsean, params referenciados que existen, nombre projection reservado, sections bien formadas); que las rules nombren RuleDocs existentes se comprueba en run_view (error que nombra la RuleDoc ausente). El contrato dice "al escribir" para esa parte: queda como hipótesis para el dueño.
q8 (API de edges): para cada fila, los vecinos salen de edges_from/edges_to del índice (src/sldb/api/edges/edge_reading.py) con la relation pedida; si el store declara project_graph (GD21), se agregan también los de ProjectGraph.edges_from/edges_to para esa misma relation, sin duplicados (por export_id o id de nodo), en orden: primero los del índice y después los del grafo de proyecto, cada grupo ordenado.
q9 (firma del grafo de proyecto en revision): GD21 no expone su firma como valor (el memo guarda un objeto interno). revision = sha256 de: los source_hash ordenados de los documentos leídos, el content_hash de la ViewDoc y de las RuleDocs usadas y, si alguna sección usó ProjectGraph, shards_signature(store) (src/sldb/store/edge_index/shard_signature.py) en su forma serializada. No se edita project_graph_memo.py. Hipótesis: un cambio en una superficie no modelada que no mueve los shards no cambia revision.
q10 (forma de groups): con group_by, la sección devuelve groups = lista de {value, rows}, en el orden de group_order; los valores que no están en group_order van después, ordenados por valor; las filas sin el campo van en un grupo final con value null. Un valor de group_order sin filas aparece igual, con rows vacía (las columnas de un tablero no desaparecen). Sin group_by, la sección devuelve rows.
q11 (GET /views): devuelve {views: [{name, title, params, sections: [key...]}]} con las ViewDoc que tienen sections (las compuestas de GD25), ordenadas por name. Las de proyección (sin sections) siguen listadas en GET /views/projection de SV02, que no cambia. sldb views list emite lo mismo.
q12 (en caliente): el test o el script de medición crea el store con 200 Items, llama run_view una vez para calentar las cachés y mide la mediana de 5 llamadas seguidas en el mismo proceso; debe ser < 1 s en robocop2. La cifra y el comando van en el reporte de entrega y el coordinador los copia a la Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm pytest -q tests/api/test_view_doc.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_view_and_routes.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_models_and_builtins.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_payload_projection.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_every_command_has_a_handler.py
- grep -rn 'register_view_provider\|computed' src/sldb/api/views/ vacío
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout (regla 4)
- sldb views run NAME --format json sobre el store temporal del test (salida en el reporte de entrega) y tiempo de pared de la vista tablero sobre 200 Items en caliente (< 1 s), registrado aquí
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con un modelo Item (status, owner, depends_on), un ciclo de vida de prueba (RitualDoc/RelationDoc de prueba o modelos propios) y una RuleDoc: una ViewDoc tablero con group_by status y group_order declarado devuelve las columnas en ese orden; edges agrega depends_on entrantes y salientes; rules agrega findings con la cláusula; transitions devuelve holding con effects y blocked con su finding para un Item bloqueado; un parámetro {owner} filtra; un documento de prueba que hace de recibo de un hecho externo, enlazado a un Item, aparece en la fila del Item por edges sin código del consumidor; grep de register_view_provider y computed en src/sldb/api/views/ vacío; sldb views run y GET /views/<name> devuelven el mismo payload; GET con If-None-Match igual devuelve 304 y tras escribir un Item la revisión cambia; editar la RuleDoc también cambia la revisión; una ViewDoc con selector que no parsea es rechazada al escribirla; una ViewDoc llamada projection es rechazada; run_view sobre una ViewDoc de proyección (sin sections) da error que la nombra; las rutas /views/projection* de SV02 siguen respondiendo igual (sus tests verdes); tiempo de pared de la vista tablero sobre 200 Items en caliente < 1 s en robocop2 (registrado en la Validation del TaskDoc); CHANGELOG; docs/architecture/views.md; nota de cierre a deskops.

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

FILE:src/sldb/models/notation/view_doc.py
"""`ViewDoc` del vocabulario visual y la proyeccion."""

from __future__ import annotations

from pydantic import Field, field_validator
from sldb.models.notation.view_doc_template import VIEW_DOC_TEMPLATE
from sldb.models.notation.view_nodes import normalize_view_nodes
from sldb.models.structured_doc import StructuredNLDoc


class ViewDoc(StructuredNLDoc):
    """Una vista de la gramatica de proyeccion: que documentos y relaciones del store entran,
    en que direccion, y con que notacion y layout se dibujan.

    Es portable: solo nombra modelos, tipos de relacion y una notacion, nunca ids de nodo ni
    rutas de store, asi que la misma vista se evalua contra cualquier store que tenga esos
    modelos y relaciones. graph_ui la evalua (sldb.api.graph) y la crea y guarda por sldb.
    """

    __semantics__ = {
        "type": ["view"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["notation"]
    __template__ = VIEW_DOC_TEMPLATE

    id: str = Field(description="Nombre de la vista; nombre del documento (`ViewDoc:<name>`).")
    name: str = Field(description="Nombre de la vista, igual al id.")
    title: str = Field(description="Rotulo legible de la vista.")
    nodes: list[dict] = Field(
        default_factory=list,
        description="Union de entradas `{model, where}`: documentos de ese modelo que cumplen `where` (gramatica de `sldb find --where`; vacio = todos los del modelo). Lista vacia = todos los documentos.",
    )
    relations: list[str] = Field(default_factory=list, description="Nombres de tipos de relacion que se conservan entre esos nodos; vacio = todos.")
    direction: str = Field(default="both", description="`both`, `outgoing` o `incoming`, como `sldb.api.graph.RelationFilter.direction`.")
    notation: str = Field(default="", description="`NotationDoc:<name>` opcional; su `layout` da el estilo de la vista.")
    layout: dict = Field(
        default_factory=dict,
        description="Override del `layout` de la notacion, misma forma (`kind: graph`, `style: layered|rings`, `ring_field` para rings).",
    )
    params: dict = Field(
        default_factory=dict,
        description="Parametros opcionales de vista compuesta (GD25).",
    )
    sections: list = Field(
        default_factory=list,
        description="Secciones opcionales de vista compuesta (GD25).",
    )
    description: str = Field(default="", description="Para que sirve la vista.")

    @field_validator("nodes", mode="before")
    @classmethod
    def _nodes(cls, value):
        return normalize_view_nodes(value)

    @field_validator("direction")
    @classmethod
    def _direction(cls, value: str) -> str:
        if value not in ("both", "outgoing", "incoming"):
            raise ValueError(f"direction {value!r} must be both, outgoing or incoming")
        return value

    @field_validator("layout", mode="before")
    @classmethod
    def _layout(cls, value):
        value = {} if value is None else value
        style = value.get("style") if isinstance(value, dict) else None
        if style not in (None, "", "layered", "rings"):
            raise ValueError(f"layout.style {style!r} must be layered or rings")
        return value

    @field_validator("notation", mode="before")
    @classmethod
    def _absent_notation(cls, value):
        return "" if value is None else value

    @field_validator("params", mode="before")
    @classmethod
    def _absent_params(cls, value):
        return {} if value is None else value

    @field_validator("sections", mode="before")
    @classmethod
    def _absent_sections(cls, value):
        return [] if value is None else value

FILE:src/sldb/api/__init__.py
"""sldb's library API: the store, model and document operations the CLI performs, as functions.

Consumers (pron, deskops, graph_ui...) call these instead of instantiating `sldb.cli` command
classes with fake argparse namespaces. Each operation that names a store opens it the way a
CLI command does (`open_store`), returns a pydantic model instead of printing, and raises
`sldb.core.exceptions` errors instead of exiting. Layering: `sldb.cli` -> `sldb.api` ->
`sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`.
"""

from __future__ import annotations

from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.documents.apply_batch import apply_batch
from sldb.api.documents.batch_report import BatchReport
from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents.move_document import move_document
from sldb.api.documents.transaction import RollbackError, Transaction, transaction
from sldb.api.documents import document_ast, build_document_ir_json, leaf_paths, runtime_document, extract_document_payload, render_document_markdown, render_model_template
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.documents.select_documents import select_documents
from sldb.api.documents.selector import Selector
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.document_serialization import serialize_document
from sldb.api.documents.payload_path_reading import deep_get, ensure_list
from sldb.api.documents.payload_path_writing import deep_delete, deep_set
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.replace_text import replace_text
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.edges.check_edges import check_edges
from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to, load_edge_index
from sldb.api.edges.apply_effects import apply_effects
from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edges_blocked import edges_blocked
from sldb.api.edges.edges_holding import edges_holding
from sldb.api.edges.project_graph import ProjectGraph, ProjectGraphConfig, project_graph
from sldb.api.model_registry.remove_model import remove_model
from sldb.api.model_registry.inherit_model import inherit_model
from sldb.models.structured_doc import StructuredNLDoc
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)
from sldb.api.notations import (
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    save_projection_view,
    sync_notation,
    sync_palette,
)
from sldb.api.edges.unresolved_references import unresolved_references
from sldb.store.edge_index.unresolved_reference import UnresolvedReference
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_record, serialize_edge_records
from sldb.api.edges.init_relations import init_relations
from sldb.api.edges.rebuild_edges import rebuild_edges
from sldb.api.edges.relations_init_report import RelationsInitReport
from sldb.api.journal import journal, verify_journal
from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck
from sldb.api.model_drafts.draft_validation import promote_model_draft, validate_model_draft
from sldb.api.model_drafts.draft_validation_report import DraftValidationReport
from sldb.api.model_drafts.field_drafts import add_model_field, remove_model_field
from sldb.api.model_drafts.model_draft import ModelDraft
from sldb.api.model_drafts.model_source import ModelSource
from sldb.api.model_drafts.source_location import locate_model_source
from sldb.api.model_drafts.template_drafts import edit_model_template
from sldb.api.model_drafts.metadata_drafts import edit_model_metadata
from sldb.api.model_create.create_model import create_model
from sldb.api.model_create.field_decl import FieldDecl
from sldb.api.model_create.model_check import ModelCheck
from sldb.api.model_registry.add_model import add_model
from sldb.api.search import search
from sldb.api.semantic import add_semantic_equivalence, add_semantic_parent, remove_semantic_parent, semantic_tag
from sldb.api.tags import tag_check, tag_folder, tag_namespaces, tag_tree
from sldb.api.rules import on_check_findings, refuse_unknown_family, rules_check, rules_explain, rules_on_check, transition_findings
from sldb.api.where import where_matches
from sldb.core.exceptions import AmbiguousSelectionError, ConflictError, WherePredicateError
from sldb.api.model_registry.describe_model import describe_model
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.model_registry.model_description import ModelDescription
from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.model_registry.model_registration import ModelRegistration
from sldb.api.model_registry.registered_model import RegisteredModel
from sldb.api.model_registry.reindex_model import reindex_model
from sldb.api.schema.describe_field import describe_field, describe_model_fields
from sldb.api.schema.field_description import FieldDescription
from sldb.api.segments import CompositionPiece, CompositionSpec, DocumentSegments, FieldSegment, LiteralSegment, Segment, SourceRef, build_document_segments
from sldb.api.stores.doc_ref import split_doc_ref
from sldb.api.stores.doc_ref_status import DocRefStatus
from sldb.api.stores.doc_status import doc_exists, doc_status
from sldb.api.stores.tracked_documents import tracked_documents
from sldb.api.stores.ambiguous_document import AmbiguousDocument
from sldb.api.stores.build_store import build_store
from sldb.api.stores.scaffold_report import ScaffoldReport
from sldb.api.stores.scaffold_store import scaffold_store
from sldb.api.stores.seed import Seed
from sldb.api.stores.store_declaration import StoreDeclaration
from sldb.api.stores.tag_namespace import TagNamespace
from sldb.api.stores.resolve_indexed_document import indexed_model_bases, resolve_indexed_document
from sldb.api.stores.init_store import init_store
from sldb.api.stores.link_store import link_store
from sldb.api.stores.unlink_store import unlink_store
from sldb.api.model_registry.registration_query import is_model_registered, registered_models
from sldb.api.stores.linked_store import LinkedStore
from sldb.api.stores.migrate_hash_names import migrate_store_hash_names
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_check import check_store
from sldb.api.stores.store_fingerprint import store_fingerprint
from sldb.api.stores.store_links import store_links
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.api.stores.update_store_indexes import update_store_indexes
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.edge_rebuild_report import EdgeRebuildReport
from sldb.store.edge_index.node_ids import anchor_node_id, bare, doc_node_id, field_node_id, kind, model_node_id, relation_type_node_id, section_node_id, tag_node_id
from sldb.store.journal import JournalEntry, JournalVerifyReport
from sldb.store.models.edge_node_record import EdgeNodeRecord
from sldb.store.models.edge_record import EdgeRecord
from sldb.store.models.document_hashes import DocumentHashes
from sldb.store.models.store_fingerprint import StoreFingerprint
from sldb.api.corpus import (
    Corpus,
    CorpusEntry,
    FieldEntry,
    FieldHit,
    FieldProjection,
    Hit,
    IndexProjection,
    field_id,
    split_field_id,
)

__all__ = [
    "Corpus", "CorpusEntry", "FieldEntry", "FieldHit", "FieldProjection",
    "Hit", "IndexProjection", "field_id", "split_field_id",
    "CompositionPiece", "CompositionSpec", "DocumentSegments", "FieldSegment",
    "LiteralSegment", "Segment", "SourceRef", "build_document_segments",
    "DocumentHashes", "DocumentReference", "DraftDocumentCheck", "DraftValidationReport",
    "EdgeCheckReport", "EdgeIndex", "EdgeNodeRecord", "EdgeRebuildReport",
    "EdgeRecord", "FieldDecl", "FieldDescription", "JournalEntry",
    "JournalVerifyReport", "LinkedStore", "ModelCheck", "ModelDescription",
    "ModelDocumentSummary", "ModelDraft", "ModelFieldSummary", "ModelRegistration",
    "ModelSource", "RegisteredModel", "RelationsInitReport", "StoreFingerprint",
    "StoreLocation", "StoreUpdateReport", "add_model", "add_model_field",
    "create_model", "anchor_node_id", "bare", "check_doc_anchors", "check_edges", "check_store",
    "store_fingerprint", "create_document", "deep_delete", "deep_get", "deep_set",
    "delete_document", "describe_field", "describe_model", "describe_model_fields",
    "doc_node_id", "document_ast", "edge_node", "edge_nodes_of_type", "edges_from",
    "edges_to", "edit_model_metadata", "edit_model_template", "ensure_list", "extract_document_payload",
    "field_node_id", "init_relations", "init_store", "journal", "kind", "link_store", "unlink_store",
    "load_edge_index", "leaf_paths", "load_runtime_documents", "migrate_store_hash_names",
    "load_registered_model", "locate_model_source", "model_node_id", "open_store",
    "promote_model_draft", "rebuild_edges", "reindex_model", "relation_type_node_id",
    "remove_model_field", "render_document_markdown", "render_model_template",
    "resolve_model_ref", "runtime_document", "save_document_payload", "search",
    "section_node_id", "serialize_document", "serialize_edge_node_records",
    "serialize_edge_records", "tag_node_id", "track_document_file", "untrack_document",
    "update_store_indexes", "validate_model_draft", "verify_journal",
    "AmbiguousSelectionError", "Selector", "select_documents",
    "DocRefStatus", "doc_exists", "doc_status", "tracked_documents", "AmbiguousDocument", "indexed_model_bases", "resolve_indexed_document", "split_doc_ref", "store_links",
    "WherePredicateError", "apply_effects", "edges_blocked", "edges_holding", "effects_of", "on_check_findings", "refuse_unknown_family", "rules_check", "rules_explain", "rules_on_check", "transition_findings", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "BatchReport", "ConflictError", "RollbackError", "Transaction", "apply_batch", "move_document", "transaction",
    "ScaffoldReport", "Seed", "StoreDeclaration", "build_store", "scaffold_store",
    "ProjectGraph", "ProjectGraphConfig", "project_graph",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
    "TagNamespace", "add_semantic_equivalence", "add_semantic_parent", "remove_semantic_parent", "semantic_tag",
    "replace_text", "tag_check", "tag_folder", "tag_namespaces", "tag_tree",
]

FILE:src/sldb/cli/parsers/public.py
from __future__ import annotations
import argparse
from .stores import add_stores_group
from .models1 import add_models_group
from .predicates import add_predicates_group
from .rules import add_rules_group
from .docs1 import add_docs_group
from .fields import add_fields_group
from .sections import add_sections_group
from .edges import add_edges_group
from .graph import add_graph_group
from .journal import add_journal_group
from .semantic import add_semantic_group
from .anchors import add_anchors_group
from .notations import add_notations_group
from .tags import add_tags_group

def add_public_group_commands(s: argparse._SubParsersAction) -> None:
    add_stores_group(s)
    add_models_group(s)
    add_predicates_group(s); add_rules_group(s)
    add_docs_group(s)
    add_fields_group(s)
    add_sections_group(s)
    add_edges_group(s)
    add_graph_group(s)
    add_journal_group(s)
    add_semantic_group(s); add_anchors_group(s); add_notations_group(s); add_tags_group(s)

FILE:src/sldb/cli/dispatcher.py
from __future__ import annotations
from typing import Any
from sldb.cli.parser import build_parser
from sldb.cli.commands.help_texts import SHORT_ARGPARSE_HELP
from sldb.cli.singular_handlers import singular_handlers
from sldb.cli.subcommand_errors import parse_reporting_subcommand

class CLI:
    def __init__(self):
        self.handlers = {}
        self._load_1()
        self._load_2()
        self._load_3()
        self._load_edges()
        self.handlers.update(singular_handlers())

    def _load_1(self):
        from sldb.cli.commands.basic import BasicCLI
        from sldb.cli.commands.init import InitCLI
        from sldb.cli.commands.help import HelpCLI
        from sldb.cli.commands.faq import FAQCLI
        from sldb.cli.commands.inbox import InboxCLI
        from sldb.cli.commands.explore import ExploreCLI
        self.handlers.update({"extract": BasicCLI().extract, "render": BasicCLI().render, "validate": BasicCLI().validate})
        self.handlers.update({"init": InitCLI().init, "example": InitCLI().example, "help": HelpCLI().run})
        self.handlers.update({"faq": FAQCLI().run, "inbox": InboxCLI().run, "explore": ExploreCLI().run})

    def _load_2(self):
        from sldb.cli.commands.ast import ASTCLI
        from sldb.cli.commands.find import FindCLI
        from sldb.cli.commands.stores import StoresCLI
        from sldb.cli.commands.models import ModelsCLI
        from sldb.cli.commands.predicates import PredicatesCLI
        from sldb.cli.commands.docs import DocsCLI
        from sldb.cli.commands.journal import JournalCLI
        self.handlers.update({"ast": ASTCLI().run, "find": FindCLI().run, "stores": StoresCLI().run})
        self.handlers.update({"models": ModelsCLI().run, "predicates": PredicatesCLI().run, "docs": DocsCLI().run, "journal": JournalCLI().run})

    def _load_3(self):
        from sldb.cli.commands.selfdoc import SelfdocCLI
        from sldb.cli.commands.fields import FieldsCLI
        from sldb.cli.commands.sections import SectionsCLI
        from sldb.cli.commands.serve import ServeCLI
        from sldb.cli.commands.lint import lint_cli
        from sldb.cli.commands.semantic import SemanticCLI
        self.handlers.update({"fields": FieldsCLI().run, "sections": SectionsCLI().run, "semantic": SemanticCLI().run})
        self.handlers.update({"serve": ServeCLI().run, "lint": lint_cli})
        self.handlers["selfdoc"] = SelfdocCLI().run
        self._load_addresses()

    def _load_edges(self):
        from sldb.cli.commands.anchors import AnchorsCLI
        from sldb.cli.commands.edges import EdgesCLI
        from sldb.cli.commands.graph import GraphCLI
        from sldb.cli.commands.notations import NotationsCLI
        from sldb.cli.commands import rules, tags
        self.handlers.update({"edges": EdgesCLI().run, "anchors": AnchorsCLI().run, "graph": GraphCLI().run, "notations": NotationsCLI().run, "rules": rules.RulesCLI().run, "tags": tags.TagsCLI().run})

    def _load_addresses(self):
        """The raw address surface: `legacy ls|get|glob|find|recover|compose`.

        Addresses are `st.{Model}.doc.field` (structural), `se.tag` (semantic) and
        `gse.tag` (global semantic). The singular top-level aliases (`ls`, `get`,
        `glob`, `raw-find`, `recover`, `compose`) are the pre-redesign spelling and
        route to the same handler.
        """
        from sldb.cli.commands.legacy import LegacyCLI
        legacy = LegacyCLI()
        self.handlers["legacy"] = legacy.run
        for alias in ("ls", "get", "glob", "raw-find", "recover", "compose"):
            self.handlers[alias] = self._alias_to_legacy(legacy, "find" if alias == "raw-find" else alias)

    @staticmethod
    def _alias_to_legacy(legacy, name: str):
        def _run(args):
            args.legacy_command = name
            return legacy.run(args)
        return _run

    def run(self, argv: Any = None) -> int:
        if self._check_help(argv): return 0
        args = self._parse_args(argv)
        if isinstance(args, int): return args
        return self._dispatch(args)

    def _check_help(self, argv: Any) -> bool:
        if argv in (["-h"], ["--help"]): print(SHORT_ARGPARSE_HELP); return True
        return False

    def _parse_args(self, argv: Any) -> Any:
        parser = build_parser()
        try: return parse_reporting_subcommand(parser, argv)
        except SystemExit as e: return e.code if isinstance(e.code, int) else (0 if e.code is None else 1)

    def _dispatch(self, args: Any) -> int:
        handler = self.handlers.get(args.command)
        if not handler: print(f"Unknown command: {args.command}"); return 2
        return handler(args)

FILE:src/sldb/cli/serve/routes.py
from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sldb.api import serialize_document  # re-export: data contract moved to sldb.api; kept for backwards compatibility
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.health import health_payload
from sldb.cli.serve.docs_create_route import dispatch_docs_or_create
from sldb.cli.serve.docs_select_routes import dispatch_docs_select
from sldb.cli.serve.edges_documents_routes import dispatch_edges
from sldb.cli.serve.document_routes import DOCUMENT_ROUTES, dispatch_document
from sldb.cli.serve.corpus_routes import corpus_rank
from sldb.cli.serve.find_routes import dispatch_find
from sldb.cli.serve.graph_routes import dispatch_graph
from sldb.cli.serve.lint_routes import dispatch_lint
from sldb.cli.serve.models_routes import dispatch_models
from sldb.cli.serve.ast_routes import dispatch_ast
from sldb.cli.serve.fields_routes import dispatch_fields
from sldb.cli.serve.project_graph_routes import dispatch_project_graph
from sldb.cli.serve.render_routes import dispatch_render
from sldb.cli.serve.responses import read_json_body, send_json, send_common_headers
from sldb.cli.serve.save_routes import save_request
from sldb.cli.serve.schema import store_schema
from sldb.cli.serve.sections_routes import dispatch_sections
from sldb.cli.serve.similar_routes import similar_payload
from sldb.cli.serve.segments_routes import extract_segments_response
from sldb.cli.serve.graph_payload import graph_documents, graph_payload  # noqa: F401 - graph_documents re-exported
from sldb.cli.serve.stores_routes import dispatch_stores
from sldb.cli.serve.notations_routes import dispatch_notations, dispatch_projection_views
from sldb.store.export import export_semantic_payload


def dispatch(
    handler: BaseHTTPRequestHandler,
    method: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    if method == "GET":
        return dispatch_get(handler, route, store_path, project_root, pythonpath)
    if method == "POST":
        return dispatch_post(handler, route, store_path, project_root, pythonpath)
    return {"ok": False, "error": "Method not allowed"}, 405


def dispatch_get(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    handlers = {"/health": lambda *_: health_payload(store_path, project_root, pythonpath), "/schema": lambda *_: store_schema(store_path, pythonpath).model_dump(mode="json"), "/graph": lambda *_: graph_payload(store_path, pythonpath), "/semantic-export": lambda *_: export_semantic_payload(store_path, project_root, resolve_model_ref, pythonpath)}
    if route in handlers:
        return handlers[route](route), 200
    return _nested_get(handler, route, store_path, project_root, pythonpath)


def _nested_get(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    if route == "/edges" or route.startswith("/edges/"): return dispatch_edges(handler, store_path, pythonpath)
    if route.startswith("/graph/"): return dispatch_graph(handler, store_path)
    if route.startswith("/project-graph/"): return dispatch_project_graph(handler, store_path)
    if route in DOCUMENT_ROUTES: return dispatch_document(handler, route, store_path, project_root, pythonpath)
    if route == "/docs/select": return dispatch_docs_select(handler, store_path)
    if route == "/models" or route.startswith("/models/"): return dispatch_models(handler, "GET", route, store_path, project_root, pythonpath)
    if route == "/lint": return dispatch_lint(handler, store_path, project_root, pythonpath)
    if route == "/notations" or route.startswith("/notations/"): return dispatch_notations(handler, "GET", route, store_path, project_root, pythonpath)
    if route.startswith("/views/projection"): return dispatch_projection_views(handler, "GET", route, store_path, project_root, pythonpath)
    return _dispatch_reader(route, handler, store_path, project_root, pythonpath)


def _dispatch_reader(route: str, handler: BaseHTTPRequestHandler, store_path: Path, project_root: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    if route == "/stores" or route == "/stores/check": return dispatch_stores(handler, route, store_path, project_root, pythonpath)
    if route == "/corpus/rank": return corpus_rank(handler, store_path, pythonpath)
    if route == "/similar": return similar_payload(handler, store_path)
    if route == "/fields": return dispatch_fields(handler, store_path, project_root, pythonpath)
    if route == "/sections": return dispatch_sections(handler, store_path, project_root, pythonpath)
    if route == "/ast": return dispatch_ast(handler, store_path, project_root, pythonpath)
    if route == "/find": return dispatch_find(handler, store_path, project_root, pythonpath)
    if route == "/extract" or route == "/render": return dispatch_render(handler, route, store_path, project_root, pythonpath)
    return {"ok": False, "error": f"Unknown route: {route}"}, 404





def dispatch_post(
    handler: BaseHTTPRequestHandler,
    route: str,
    store_path: Path,
    project_root: Path,
    pythonpath: str,
) -> tuple[dict[str, Any], int]:
    if route.startswith("/models/"): return dispatch_models(handler, "POST", route, store_path, project_root, pythonpath)
    if route == "/docs" or route.startswith("/docs/"): return dispatch_docs_or_create(handler, route, store_path, project_root, pythonpath)
    if route == "/extract/segments": return extract_segments_response(read_json_body(handler), store_path, pythonpath)
    if route.startswith("/notations/"): return dispatch_notations(handler, "POST", route, store_path, project_root, pythonpath)
    if route.startswith("/views/projection"): return dispatch_projection_views(handler, "POST", route, store_path, project_root, pythonpath)
    if route != "/save": return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return save_request(read_json_body(handler), store_path, project_root, pythonpath)


def handle_options(handler: BaseHTTPRequestHandler, cors: bool) -> None:
    if not cors:
        send_json(handler, 404, {"ok": False, "error": "CORS disabled"}, cors)
        return
    handler.send_response(204)
    send_common_headers(handler, 0, cors)
    handler.end_headers()

FILE:instruccion
Cold-bundle de la tarea task-gd25: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm pytest -q tests/api/test_view_doc.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_view_and_routes.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_models_and_builtins.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_payload_projection.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_every_command_has_a_handler.py
- grep -rn 'register_view_provider\|computed' src/sldb/api/views/ vacío
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout (regla 4)
- sldb views run NAME --format json sobre el store temporal del test (salida en el reporte de entrega) y tiempo de pared de la vista tablero sobre 200 Items en caliente (< 1 s), registrado aquí
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

