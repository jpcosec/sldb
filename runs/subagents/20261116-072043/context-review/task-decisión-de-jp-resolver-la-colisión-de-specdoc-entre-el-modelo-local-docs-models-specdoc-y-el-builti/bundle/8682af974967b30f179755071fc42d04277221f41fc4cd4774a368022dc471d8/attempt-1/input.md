FILE:desk/tasks/task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti.md
---
sldb:
  by: agent
  at: '2026-11-16T05:23:26Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261106-152834-unclear-specdoc-el-modelo-local-docs-models-specdoc-colisiona-con-el-builtin-sldb-models-notation-models-specdoc-tras-sv01.md
depends_on: []
pills: []
files:
- docs/architecture/notations-and-views.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decisión de JP: resolver la colisión de SpecDoc entre el modelo local docs.models:SpecDoc y el builtin de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Desde SV01 (6b80df36) sldb.models exporta un SpecDoc builtin (src/sldb/models/notation/spec_doc.py, exportado en sldb.api), pero el store de este repo sigue enlazando el nombre SpecDoc a docs.models:SpecDoc (.sldb/store.yaml, líneas 17-18; clase en docs/models.py:237). deskops doctor lo reporta como alerta y cualquier consumidor que resuelva SpecDoc por nombre (sldb serve, graph_ui, deskops view) puede recibir el modelo equivocado. La tarea task-los-specs-de-docs-architecture-spec2viz-se-construyen-con-specir-catalog-build-y-se-sincronizan-con está relacionada (mueve los specs de docs/architecture/spec2viz) pero no decide esto. Origen: desk/inbox/20261106-152834-unclear-specdoc-el-modelo-local-docs-models-specdoc-colisiona-con-el-builtin-sldb-models-notation-models-specdoc-tras-sv01.md.

## Goal

_Describe the concrete result this task must produce._

JP elige una opción y queda escrita en docs/architecture/notations-and-views.md, sección "SpecDoc local frente al builtin", con la fecha; se crea con deskops add task la tarea de código que la implementa.

## Scope

_State what is in scope and what is out of scope._

Entra: presentar las tres opciones de la nota con su costo: (a) renombrar el modelo local (por ejemplo a ArchitectureSpecDoc) y migrar sus documentos con sldb (costo bajo, sin cambio de semántica); (b) borrar el modelo local y migrar sus documentos al builtin (requiere que el builtin cubra sus campos; costo medio); (c) una regla explícita de precedencia local sobre builtin en la resolución por nombre (cambia sldb para todos los stores; costo alto). Recomendación del coordinador: (a). Registrar el recibo owner (el dispose accepted es de JP), escribir la sección y crear la tarea de implementación con archivos y validación (sldb stores build --check y deskops doctor sin la alerta). No entra: implementar la opción elegida en esta tarea.

Precisiones (preflight-1): las tres opciones son las de este contrato (la nota de origen las enumera igual). Conteo: `sldb stores check --store .sldb` no cuenta por modelo; se usa el índice: el documents_count de .sldb/core/models/SpecDoc.yaml (leerlo con sldb, por ejemplo sldb docs list --model SpecDoc si existe, o contando las entradas de ese modelo en la salida de `sldb docs list`). La tarea de implementación que se crea tiene como validación `TMPDIR=/dev/shm sldb stores build --check --store .sldb` y `TMPDIR=/dev/shm deskops doctor --root sldb` sin la alerta "SpecDoc: another class under the name of the model".
Protocolo de decisión (vale para todo el contrato): el coordinador del desk de sldb le pregunta a JP por el canal de coordinación (herdr o el supervisor), con las opciones, costos y recomendación de este contrato copiados tal cual. La respuesta se registra con `deskops review record <esta tarea> --kind owner --reason "JP <AAAA-MM-DD>: <opción y motivo>" --root sldb`; el dispose accepted lo hace JP con `deskops review dispose <id del recibo> --verdict accepted --reason ... --root sldb`; nada se ejecuta ni se cierra sin ese recibo aceptado. "La fecha" es la de la respuesta de JP, en ISO (AAAA-MM-DD). La sección del documento tiene esta forma: un encabezado "## <nombre de la sección>", una línea "Decisión (AAAA-MM-DD, JP): <opción>", una línea "Motivo: <motivo>" y la lista de las opciones consideradas con su costo. Una tarea que la decisión crea se escribe con deskops add task --root sldb con el contrato completo (title, why, goal, scope, implementation_path, files, validation, done_when) y references a la nota o ítem de origen de esta tarea. El commit del documento lo hace el coordinador con deskops closeout commit; nadie hace push salvo el integrador.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer docs/models.py (clase SpecDoc, línea 237), src/sldb/models/notation/spec_doc.py y .sldb/store.yaml 10-25. 2) Contar documentos del modelo local con sldb docs list o sldb stores check. 3) Pedir la decisión a JP con el conteo. 4) Escribir la sección y crear la tarea de código.

## Validation

_List the checks required before this task can close._

- grep -n 'SpecDoc local frente al builtin' docs/architecture/notations-and-views.md

## Done When

_Name the observable condition that makes the task complete._

La sección existe con la opción elegida y la fecha; recibo owner aceptado por JP; la tarea de implementación existe en desk/tasks; commit del doc.

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

FILE:docs/architecture/notations-and-views.md
# Notaciones, Vocabularios Visuales y Vistas de Proyección en SLDB

## 1. Contexto y Justificación

Históricamente, los modelos de especificación visual de diagramas y proyección (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) y el motor de carga y validación de notaciones y paletas residían en la biblioteca `spec2viz`.

Esta separación causaba una dependencia circular y obligatoria hacia `spec2viz` en el ecosistema (por ejemplo, `graph_ui` o stores que alojan diagramas y vistas portables). Si `spec2viz` no estaba instalado en el entorno donde se ejecutaba `sldb` o un store se servía remotamente vía `sldb serve`, las operaciones sobre diagramas o la carga de modelos registrados degradaban o requerían adaptadores ad-hoc.

La absorción en `sldb` (iniciada en el nodo SV01 del plan `absorber-spec2viz-y-modelos-ui`) centraliza en `sldb` el vocabulario visual, las paletas, las 8 notaciones builtin y la capacidad de resolver referencias legacy sin depender de `spec2viz`.

---

## 2. Modelos de Vocabulario Visual (`sldb.models.notation_models`)

Los 7 modelos son subclases de `StructuredNLDoc` (`sldb.models.structured_nl_doc.StructuredNLDoc`) y se reexportan tanto en `sldb.models` como en `sldb.api`:

1. **`SpecDoc`**: Representa una especificación de diagrama completa como documento del almacén. Sus elementos hijos se vinculan mediante referencias hacia `SpecNodeDoc`, y apunta opcionalmente a una `NotationDoc`.
2. **`SpecNodeDoc`**: Elemento individual de un diagrama (nodo, componente, estado, clase, participante, actor). Declara contención (`__containment__`: su campo contains admite hijos `SpecNodeDoc`) y referencias (`spec`, `refs`, `atom_refs`).
3. **`NotationDoc`**: Define una notación visual (tipo de diagrama, nivel `types`/`instances`/`both`, layout, marcadores, lista de `GlyphDoc` y `LinkDoc`, y paleta opcional).
4. **`GlyphDoc`**: Mapeo declarativo de un modelo del store (con predicado `where` opcional) a una forma visual primitiva (`shape`), compartimentos, etiquetas (`label`, `keyword`, `label_style`), y estilo (`kind`, `fill`, `stroke`, `icon`).
5. **`LinkDoc`**: Mapeo de una relación del store (arista o modelo reificado) a su representación gráfica (`line`, terminales `source_end` / `target_end`, rótulos y color).
6. **`PaletteDoc`**: Definición de paleta de colores (`backgrounds` e `ink` por tema claro/oscuro), catálogo de iconos y tokens de estilo semánticos por `kind`.
7. **`ViewDoc`**: Vista de proyección declarativa y portable sobre el grafo del almacén (`nodes`, `relations`, `direction`, `notation`, `layout`).

### Convergencia con GD25 en `ViewDoc` (SV-D3)
`ViewDoc` conserva los campos de proyección de grafo y añade soporte para vistas compuestas mediante dos campos opcionales, tipados por GD25 (`docs/architecture/views.md`):
- `params: list[ViewParam]` (`sldb.models.notation.view_param`): lista de `{name, required, default}`, referenciados como `{name}` en el `select` de las secciones.
- `sections: list[ViewSection]` (`sldb.models.notation.view_section`): lista ordenada de `{key, select, fields, edges, group_by, group_order, rules, transitions}`.

Ambos campos valen `[]` cuando se omiten, son `null` o vienen vacíos (`{}` o `[]`) en documentos existentes, así que los `ViewDoc` de proyección de SV02 se leen, extraen y renderizan igual que antes. Una `ViewDoc` sin `sections` es de proyección de grafo (`/views/projection*`); con `sections` es una vista compuesta que evalúa `sldb.api.run_view`.

---

## 3. Resolución y Retrocompatibilidad de Referencias (SV-D2)

Para garantizar compatibilidad inmediata con almacenes creados previamente cuyas configuraciones `.sldb/store.yaml` o `.sldb/core/store_index.yaml` registran modelos bajo el prefijo legacy:

```python
from sldb.api import resolve_model_ref

model = resolve_model_ref("spec2viz.sldb_models:NotationDoc")
# Retorna sldb.models.notation_models.NotationDoc
```

En `sldb.api.model_registry.model_reference`, cualquier referencia que utilice el módulo `spec2viz.sldb_models` se redirige transparentemente al módulo canónico `sldb.models.notation_models`.

---

## 4. Motor de Notaciones y Paletas (`sldb.notations`)

El submódulo `sldb.notations` expone:

- **Paletas (`palette.py`)**:
  - `PaletteSpec`, `ThemeColor`, `IconSet`, `KindStyle`.
  - Carga y validación semántica (`check_palette`) con verificación estricta de contraste WCAG:
    - Contraste gráfico WCAG 1.4.11 $\ge 3:1$ entre trazo y fondo por tema.
    - Contraste de texto WCAG 2.2 AA $\ge 4.5:1$ entre tinta y relleno por tema.
  - Resolución de colores (`resolve_color`) admitiendo tokens de paleta, pares `{light, dark}` o hex `#rrggbb`.
  - Paleta builtin `default` en `sldb/notations/palettes/default.yml`.

- **Notaciones (`notation.py`)**:
  - `NotationSpec`, `GlyphSpec`, `LinkSpec`, `MarkerSpec`.
  - Validación de formas primitivas (`SHAPES`), terminales (`TERMINALS`), tipos de diagrama (`DiagramType`) y relaciones esperadas por tipo (`KNOWN_RELATIONS`).
  - Las 8 notaciones builtin incluidas en `sldb/notations/builtin/`:
    - `uml-class.yml` (class)
    - `statechart.yml` (state)
    - `component.yml` (component)
    - `deployment.yml` (deployment)
    - `uml-sequence.yml` (sequence)
    - `activity.yml` (activity)
    - `component-view-matrix.yml` (component_view_matrix)
    - `reflection.yml` (reflection)

- **Resolución de Estilo (`styling.py`)**:
  - `resolve_style(glyph, kind, spec_kinds, palette)`: Resuelve propiedades visuales (`fill`, `stroke`, `icon`) aplicando la precedencia estricta:
    $$\text{Glifo de la notación} > \text{Spec kinds} > \text{Paleta de la notación}$$
  - `resolve_line_color(link, palette)`: Resuelve el color de línea en función de la paleta.

---

## 5. Resolvedor de Vistas y Vistas de Proyección (`sldb.api.notations`)

A partir de SV02, `sldb.api` provee los intérpretes canónicos del contrato de notación y de vistas proyectivas sin depender de librerías externas:

### 5.1 Resolvedor de Vistas (`notation_view.py`)
- `resolve_view(store, spec_ref, pythonpath=None)`:
  - Lee el `SpecDoc` del store, valida su coincidencia con `NotationDoc.diagram_type` y resuelve los nodos, aristas y leyendas.
  - Retorna `{spec, title, diagram_type, notation, palette, level, layout, nodes, links, fragments, skipped, legend}`.
- `resolve_documents(store, notation_ref, doc_refs, *, relation_refs=None, spec_style=None, pythonpath=None)`:
  - Aplica la notación a cualquier conjunto de documentos del store sin requerir un `SpecDoc`.
  - Casado de glifos por modelo + evaluación de predicado `where` sobre el payload aplanado (`flatten()`).
  - Extracción de compartimentos con rutas punto (`data.attributes`, `data.methods`).
  - Interpolación de plantillas `{campo}` y estereotipos `keyword` (`«{kind}»`) sin dejar variables huérfanas.
  - Detección y agrupamiento de fragmentos UML consecutivos (`fragments_of()`) por operador `data.group`.
  - Generación de leyenda completa (`glyphs`, `links`, `kinds`).

### 5.2 Vistas de Proyección (`projection_view.py`)
- `evaluate_projection_view(store, view_or_ref, pythonpath=None)`:
  - Evalúa la consulta de nodos (`[{model, where}]`) y aristas (`RelationFilter(relations, direction)`) sobre el grafo del almacén.
  - Si la vista especifica una `notation`, invoca `resolve_documents` y adjunta estilo para nodos (`styled_nodes`), aristas (`edge_styles`), `ink` de paleta por tema y `legend`.
- `list_projection_views(store, pythonpath=None)`:
  - Lista todos los `ViewDoc` registrados en el almacén.
- `save_projection_view(store, name, view, pythonpath=None, actor=None)`:
  - Guarda o actualiza un `ViewDoc` en el almacén bajo `sldb/views/<name>.md`.

### 5.3 Sincronización al Almacén (`notation_sync.py`)
- `sync_palette(store, name_or_path="default")`:
  - Escribe el `PaletteDoc` correspondiente en `sldb/palettes/` y registra modelos si hiciera falta.
- `sync_notation(store, name_or_path)`:
  - Escribe `NotationDoc`, `GlyphDoc`, `LinkDoc` y sus `RelationTypeDoc` asociados en `sldb/notations/<name>/`, además de su paleta vinculada.

---

## 6. Superficie CLI y HTTP Serve

### 6.1 CLI (`sldb notations`)
Disponible con envelope JSON (`sldb --envelope notations ...`):
- `sldb notations list [--views]`: Lista las notaciones y paletas builtin y registradas en el store (o las vistas proyectivas si se indica `--views`).
- `sldb notations sync [--notation <name|path>] [--palette <name|path>]`: Sincroniza notaciones o paletas en el store.
- `sldb notations view <spec> [--projection]`: Resuelve la vista de un `SpecDoc` o evalúa una proyección (`--projection`).
- `sldb notations resolve --notation <notation> --docs <Model:name ...>`: Resuelve un conjunto arbitrario de documentos bajo una notación.

### 6.2 HTTP Serve (`sldb serve`)
- `GET /notations`: Lista notaciones y paletas builtin y del store.
- `GET /notations/view?spec=<spec_ref>`: Resuelve un `SpecDoc`.
- `POST /notations/resolve`: Resuelve un conjunto de documentos `{notation, docs, [relations], [style]}`.
- `GET /views/projection`: Lista los `ViewDoc` del store.
- `GET /views/projection/evaluate?view=<ref>`: Evalúa una vista proyectiva por referencia.
- `POST /views/projection/evaluate`: Evalúa una vista proyectiva pasada en el body JSON.
- `POST /views/projection/save`: Guarda un `ViewDoc` `{name, view}`.

FILE:instruccion
Cold-bundle de la tarea task-decisión-de-jp-resolver-la-colisión-de-specdoc-entre-el-modelo-local-docs-models-specdoc-y-el-builti: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -n 'SpecDoc local frente al builtin' docs/architecture/notations-and-views.md

