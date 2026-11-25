FILE:desk/tasks/task-gd22-referencias-entrantes-buscar-y-reescribir.md
---
id: task-gd22-referencias-entrantes-buscar-y-reescribir
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
- task-gd24-transacción-multi-documento-en-sldb-api-y-save-atómico-absorbe-doc-io-doctransaction
pills: []
files:
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/referrer.py
- src/sldb/api/edges/rewrite_references.py
- src/sldb/api/edges/rewrite_report.py
- src/sldb/api/edges/rewrite_values.py
- src/sldb/api/edges/rewrite_mentions.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/edges.py
- src/sldb/cli/commands/edges.py
- src/sldb/cli/commands/edges_rewrite.py
- src/sldb/cli/serve/edges_routes.py
- src/sldb/cli/serve/edges_rewrite_routes.py
- src/sldb/cli/serve/routes.py
- tests/api/test_referrers.py
- tests/api/test_rewrite_references.py
- tests/test_serve.py
- docs/architecture/references.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD22: Referencias entrantes - buscar y reescribir

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD22 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG1. Depende de: ['GD21', 'GD24']. Gates requeridos: G_PROJECT_GRAPH: Grafo de proyecto declarado y servido por sldb (satisfied); G_WRITE_API: Transacción y referencias entrantes en sldb.api (satisfied).

## Goal

_Describe the concrete result this task must produce._

sldb.api.referrers(store, target) devuelve las referencias entrantes (campos escalares, elementos de listas y menciones en superficies no modeladas) desde el índice y el grafo de proyecto de GD21; sldb.api.rewrite_references(store, target, replacement | None, *, transaction=None) las reescribe o quita dentro de una transacción de GD24 (todo o nada) y devuelve un RewriteReport; CLI sldb edges referrers y sldb edges rewrite --to | --remove [--dry-run] con envelope; GET /edges/referrers y POST /edges/rewrite; docs/architecture/references.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/edges/ (referrers, rewrite_references y auxiliares nuevos), src/sldb/api/__init__.py, src/sldb/cli/parsers/edges.py, src/sldb/cli/commands/edges*.py, src/sldb/cli/serve/edges_routes.py, edges_rewrite_routes.py (nuevo) y routes.py, tests, docs/architecture/references.md, CHANGELOG.md. Fuera: editar src/sldb/api/documents/payload_save_steps.py; borrar prosa (una mención con replacement None se informa en skipped); el código de deskops que esto reemplaza (lo retira deskops).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD22). SCOPE: Función sldb.api.referrers(store, target) → lista de Referrer {source (export_id o ruta de superficie no modelada), field (nombre del campo, o null para una mención), index (posición en un campo lista, o null), location (ruta:línea para una mención), origin (schema | mention)}, construida con edges_to del índice (api/edges/edge_reading.py:47; el campo sale de metadata.field, store/edge_index/declared_references.py:68) más ProjectGraph.edges_to de GD21 para menciones; target acepta export_id, Model:name, ruta trackeada o id de nodo del grafo de proyecto. Función sldb.api.rewrite_references(store, target, replacement | None, *, transaction=None) → RewriteReport {changed: [{source, field|location, before, after}], skipped: [{source, motivo}]}: para un campo escalar reemplaza el valor (o lo vacía si replacement es None); para un campo lista reemplaza el elemento (o lo quita, sin dejar huecos ni duplicados); para una mención reescribe el texto que el MentionPattern capturó, con límite de palabra, en la línea registrada (replacement None = la mención se deja y se informa en skipped, nunca se borra prosa); conserva la forma del valor original (p. ej. prefijo tipo:id si el campo lo usa); escribe dentro de sldb.api.transaction de GD24 (la suministrada o una propia), así que todo o nada. Valores de campos __doc_anchors__ (si GO07 ya cerró): se reescribe a doc:Model:name sin @sha256 para que sldb lo repinee al guardar; si GO07 no cerró, esos campos no existen y no hay caso. CLI: sldb edges referrers TARGET y sldb edges rewrite TARGET --to NUEVO | --remove [--dry-run], con envelope (dry-run devuelve el RewriteReport sin escribir). sldb serve: GET /edges/referrers?target= y POST /edges/rewrite {target, replacement|null, dry_run}. Doc en docs/architecture/references.md.

ACCEPTANCE: En un store temporal con un documento A referenciado por B (campo escalar), C (campo lista con otros dos valores) y una superficie no modelada D (mención en prosa), referrers(A) devuelve los tres con field/index/location correctos; rewrite_references(A, A2) deja B y C apuntando a A2 (C conserva el orden y los otros valores) y reescribe la mención de D; --remove vacía B, quita el elemento de C y deja D en skipped; un fallo inyectado al escribir C revierte B (todo o nada, por GD24); --dry-run no cambia ningún byte (hash de los archivos antes y después); la operación no recorre el disco con el índice fresco (contado); POST /edges/rewrite y la CLI producen el mismo reporte; CHANGELOG; docs/architecture/references.md; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/api/edges/referrers.py, src/sldb/api/edges/rewrite_references.py, src/sldb/api/__init__.py, src/sldb/cli/parsers/edges.py, src/sldb/cli/commands/edges.py, src/sldb/cli/serve/edges_routes.py, src/sldb/cli/serve/routes.py, tests/, docs/architecture/references.md, CHANGELOG.md

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
q1 (gates): G_PROJECT_GRAPH (ad679a8d) y G_WRITE_API (fe36893f) están satisfied; GD21 y GD24 cerrados: ProjectGraph.edges_to (src/sldb/api/edges/project_graph/project_graph.py:60) y sldb.api.transaction existen en main.
q2 (GO07): GO07 está cerrado (anclas a documentos con hash de contrato): los campos __doc_anchors__ existen; su valor se reescribe a doc:Model:name sin @sha256 para que sldb lo repinee al guardar (caso cubierto por un test).
q3 (GO08 y on_write): la reescritura de un documento trackeado pasa por transaction.update (save_document_payload), así que las reglas on_write de GO08 y la familia de GD27 se evalúan; un rechazo revierte el lote entero.
q4 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.
PRECISIONES DEL PREFLIGHT (review-task-gd22-preflight-1, 2026-11-06):
q5 (menciones): una mención es lo que captura un MentionPattern de la configuración project_graph del store (GD21: src/sldb/api/edges/project_graph/mention_pattern.py, LineMentions y SectionMentions); el fixture declara su propio patrón (p. ej. un regex de identificadores tipo card:card-a). rewrite_references reescribe solo el texto capturado, en la línea que registró la arista (location ruta:línea), respetando límite de palabra; si en esa línea el texto ya no está, la mención va a skipped con motivo.
q6 (resolución de target): primero como documento trackeado con la misma regla que doc_status (name, Model/name, Model:name o ruta trackeada; ambiguo = error con candidatos); si no resuelve, como id de nodo del grafo de proyecto (kind:identity); si tampoco, SLDBDocumentTargetError. El export_id de un documento es Model:name.
q7 (--remove en un campo escalar): el valor pasa a null (None) y se guarda por transaction.update; si el modelo no admite null en ese campo, la validación del modelo lo rechaza y no se escribe nada del lote (error con el campo). En un campo lista se quita el elemento (sin huecos ni duplicados).
q8 (sin recorrer disco): el test hace una primera llamada para calentar el memo de GD21 y después cuenta con monkeypatch os.walk, os.scandir y Path.rglob durante referrers y rewrite_references --dry-run: deben ser cero.
q9 (fallo inyectado): el test hace fallar la escritura de C dentro de la transacción (monkeypatch del update de la transacción para el ref de C, o un model_validator del modelo de C que rechaza el valor nuevo) y comprueba que B queda con sus bytes, su entrada y su índice originales (hash).
q10 (HTTP igual a la CLI): como en GD21 y GD23, el cuerpo de POST /edges/rewrite y GET /edges/referrers es el mismo JSON que la CLI con --format json (igualdad de datos, sin envelope); parámetros faltantes o inválidos son 400.
q11 (--to y --remove): son mutuamente excluyentes y uno es obligatorio (sin ninguno o con los dos, error de uso, exit 2). En POST /edges/rewrite, replacement es obligatorio en el cuerpo: null = quitar; ausente = 400.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_every_command_has_a_handler.py
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout (regla 4)
- sldb edges referrers TARGET y sldb edges rewrite TARGET --to NUEVO --dry-run --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con un documento A referenciado por B (campo escalar), C (campo lista con otros dos valores) y una superficie no modelada D (mención en prosa), referrers(A) devuelve los tres con field/index/location correctos; rewrite_references(A, A2) deja B y C apuntando a A2 (C conserva el orden y los otros valores) y reescribe la mención de D; --remove vacía B, quita el elemento de C y deja D en skipped; un fallo inyectado al escribir C revierte B (todo o nada, por GD24); --dry-run no cambia ningún byte (hash de los archivos antes y después); la operación no recorre el disco con el índice fresco (contado); POST /edges/rewrite y la CLI producen el mismo reporte; CHANGELOG; docs/architecture/references.md; nota de cierre a deskops.

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

FILE:src/sldb/cli/parsers/edges.py
"""`sldb edges`: the edge index (typed nodes and edges of the store) from the command line."""

from __future__ import annotations

import argparse


def add_edges_group(s: argparse._SubParsersAction) -> None:
    """Register `edges init|rebuild|show|check|unresolved`."""
    p = s.add_parser("edges", help="Typed nodes and edges of the store (the edge index).")
    sub = p.add_subparsers(dest="edges_command", required=True)
    _store_args(sub.add_parser("init", help="Register RelationTypeDoc/RelationDoc and track the builtin relation types."))
    _store_args(sub.add_parser("rebuild", help="Bring the edge index current; only what moved is rewritten."))
    _read_args(sub.add_parser("check", help="Validate every edge against its relation type."))
    _show_args(sub.add_parser("show", help="Edges from (or --to) a document or node."))
    unresolved = sub.add_parser("unresolved", help="Declared references that name no document.")
    unresolved.add_argument("--format", choices=("text", "json"), default="text")
    _read_args(unresolved)


def _show_args(show: argparse.ArgumentParser) -> None:
    show.add_argument("node", help="Export id `Model:name`, or a node id `sldb://<kind>/...`")
    show.add_argument("--to", action="store_true", help="Edges pointing at the node instead of leaving it")
    show.add_argument("--relation", help="Only edges of this relation type")
    show.add_argument("--holds-for", metavar="DOC", help="Only edges whose condition holds on this document's fields (name, path or Model/name)")
    show.add_argument("--pythonpath", help="Project path (to read the --holds-for document)")
    show.add_argument("--evidence", action="store_true", help="Add metadata.evidence: the target's hash, the source's contract, and the engine or actor")
    _read_args(show)


def _store_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--pythonpath", help="Project path")


def _read_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--store", help="Store path")
    p.add_argument("--local", action="store_true", help="Leave the linked stores out")
    p.add_argument("--exclude-tag", action="append", default=[], help="Leave out documents carrying this tag (repeatable)")

FILE:src/sldb/cli/commands/edges.py
"""`sldb edges` handlers: thin printing wrappers over `sldb.api`'s edge index functions."""

from __future__ import annotations

import json
from typing import Any

from sldb.cli.commands.edges_unknown_node import unknown_node_message
from sldb.api import check_edges, edges_from, edges_holding, edges_to, init_relations, open_store, rebuild_edges, runtime_document, unresolved_references


class EdgesCLI:
    """Noun-first surface of the edge index."""

    def run(self, args: Any) -> int:
        """Dispatch `edges init|rebuild|show|check|unresolved`; 0 on success, 1 when a check fails."""
        handler = {"init": self._init, "rebuild": self._rebuild, "show": self._show, "check": self._check, "unresolved": self._unresolved}[args.edges_command]
        return handler(args)

    def _init(self, args: Any) -> int:
        print(f"Initialized relations: {init_relations(args.store, args.pythonpath).summary()}")
        return 0

    def _rebuild(self, args: Any) -> int:
        report = rebuild_edges(args.store, args.pythonpath)
        print(f"Edges: {report.docs_written} shard(s) written, {report.docs_reused} reused, {report.models_walked} model(s) walked")
        return 0

    def _show(self, args: Any) -> int:
        if args.holds_for and args.to:
            raise SystemExit("--holds-for reads the edges leaving the node; it does not combine with --to")
        edges = self._edges(args)
        if not edges and (unknown := unknown_node_message(args)):
            raise SystemExit(unknown)
        edges = _with_evidence(args, edges) if args.evidence else edges
        print(json.dumps([e.model_dump() for e in edges], indent=2, ensure_ascii=False))
        return 0

    def _edges(self, args: Any) -> list:
        if args.holds_for:
            doc = runtime_document(open_store(args.store, mode="readonly").store_path, args.pythonpath, args.holds_for)
            return edges_holding(args.store, args.node, dict(doc.payload), args.relation, not args.local, args.exclude_tag, _export_id(doc))
        return (edges_to if args.to else edges_from)(args.store, args.node, args.relation, not args.local, args.exclude_tag)

    def _check(self, args: Any) -> int:
        """Exit 1 only on an error; a shard built from another `hash_c` is an alert."""
        report = check_edges(args.store, not args.local, args.exclude_tag)
        _report_findings(report)
        if report.linked_errors or report.linked_stale:
            print(f"note: linked stores: {len(report.linked_errors)} error(s), {len(report.linked_stale)} stale, theirs to fix (run `edges check` there, or this with --local to leave them out)")
        if report.untracked_builtins:
            print(f"note: builtin relation type(s) not tracked here, checked against sldb's own: {', '.join(report.untracked_builtins)} (`sldb edges init` tracks them)")
        print("Edges OK" if report.ok else f"{len(report.errors)} error(s), {len(report.stale)} stale")
        return 1 if report.errors else 0

    def _unresolved(self, args: Any) -> int:
        """A report, not a check: 0 whatever it finds."""
        found = unresolved_references(args.store, not args.local, args.exclude_tag)
        if args.format == "json":
            print(json.dumps([r.model_dump() for r in found], indent=2, ensure_ascii=False))
            return 0
        for r in found:
            print(f"{r.reason}: {r.source} .{r.field} -> {r.target}" + (f" ({r.target_export_id})" if r.target_export_id else ""))
        print(f"{len(found)} unresolved reference(s)")
        return 0


def _report_findings(report: Any) -> None:
    from sldb.cli import alert_sink
    from sldb.core.finding import alert, error

    stale = [alert("edges/stale", s, "the shard was built from another hash_c of the document", "sldb edges rebuild") for s in report.stale]
    alert_sink.report([error("edges/invalid", "edges", e) for e in report.errors] + stale)


def _export_id(doc: Any) -> str:
    """`Model:name` of a runtime document (`store:Model:name` behind a link): its `on_transition` rules run (GO08)."""
    prefix = "" if doc.store_name in ("local", "", None) else f"{doc.store_name}:"
    return f"{prefix}{doc.model_name}:{doc.name}"


def _with_evidence(args: Any, edges: list) -> list:
    from sldb.api.edges.edge_evidence import stamp_evidence

    return stamp_evidence(args.store, edges, not args.local)

FILE:src/sldb/cli/serve/edges_routes.py
"""GET /edges* routes: read-only views over the real edge index API.

`/edges?from=|to=` takes `include_linked` (`true` by default, as the output always was;
`false` leaves the linked stores out, as `edges_from(..., include_linked=False)` does).
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to
from sldb.api.edges.edge_serialization import serialize_edge_node_record, serialize_edge_node_records, serialize_edge_records
from sldb.cli.serve.params import query_params, require_param

_FLAGS = {"1": True, "true": True, "yes": True, "on": True, "0": False, "false": False, "no": False, "off": False}


def dispatch_edge(
    handler: BaseHTTPRequestHandler,
    store_path: Path,
) -> tuple[dict[str, Any], int]:
    route = urlparse(handler.path).path
    callback = EDGE_ROUTES.get(route)
    if callback is None:
        return {"ok": False, "error": f"Unknown route: {route}"}, 404
    return callback(handler, store_path)


def edge_list_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    params = query_params(handler)
    include_linked = _FLAGS.get(params.get("include_linked", "true").lower())
    if include_linked is None:
        return {"ok": False, "error": "Invalid parameter include_linked: expected true or false"}, 400
    return _edges_of(store_path, params, include_linked)


def _edges_of(store_path: Path, params: dict[str, str], include_linked: bool) -> tuple[dict[str, Any], int]:
    origin, target, relation = params.get("from") or None, params.get("to") or None, params.get("relation") or None
    if origin is not None:
        return edge_list(store_path, edges_from, origin, relation, include_linked)
    if target is not None:
        return edge_list(store_path, edges_to, target, relation, include_linked)
    return {"ok": False, "error": "Missing parameter: expected 'from' or 'to'"}, 400


def edge_list(store_path: Path, reader: Any, export_id: str, relation: str | None, include_linked: bool = True) -> tuple[dict[str, Any], int]:
    records = reader(store_path, export_id, relation, include_linked)
    return {"edges": serialize_edge_records(records)}, 200


def node_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    node_id, error = require_param(query_params(handler), "id")
    if error is not None:
        return error, 400
    record = edge_node(store_path, node_id)
    if record is None:
        return {"ok": False, "error": f"Unknown node: {node_id}"}, 404
    return {"node": serialize_edge_node_record(record)}, 200


def nodes_of_type_payload(handler: BaseHTTPRequestHandler, store_path: Path) -> tuple[dict[str, Any], int]:
    node_type, error = require_param(query_params(handler), "type")
    if error is not None:
        return error, 400
    records = edge_nodes_of_type(store_path, node_type)
    return {"nodes": serialize_edge_node_records(records)}, 200


EDGE_ROUTES = {
    "/edges": edge_list_payload,
    "/edges/node": node_payload,
    "/edges/nodes": nodes_of_type_payload,
}

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
Cold-bundle de la tarea task-gd22: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm pytest -q tests/api/test_rewrite_references.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/api/test_api_edges.py
- TMPDIR=/dev/shm pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_every_command_has_a_handler.py
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout (regla 4)
- sldb edges referrers TARGET y sldb edges rewrite TARGET --to NUEVO --dry-run --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

