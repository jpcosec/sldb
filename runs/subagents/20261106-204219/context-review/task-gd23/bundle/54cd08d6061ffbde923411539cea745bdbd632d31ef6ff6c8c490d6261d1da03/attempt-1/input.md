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

PRECISIONES DEL PREFLIGHT (review-task-gd23-preflight-1, 2026-11-06):
q4 (arranque): el ejecutor NO arranca mientras G_GO04 esté pending; despacha el coordinador cuando el supervisor lo marca. El contrato de la facet payload es el que GO04 deja en main (TaskDoc task-go04-..., precisiones p2-p6: FacetFilter(facet="payload", conditions=[FieldCondition(...)])).
q5 (where): la gramática es la de docs/architecture/rules-language.md (GO02), evaluada por el evaluador que haya en main al despachar; si GO05 no cerró, where acepta solo comparaciones de campo (campo op valor con =, !=, <, >, in, combinadas con and/or/not) traducidas a FacetFilter de GO04, y lo que el parser rechace es error de where con el texto de error del parser. No se inventan operadores.
q6 (CLI): no hay string corto: la CLI usa solo los flags --ref, --prefix, --path-glob, --model, --where, --one (y --include-linked); el selector como mapa es la forma de la API y de GET /docs/select (mismos nombres como query params).
q7 (ref y alias): ref acepta exactamente lo que doc_status (src/sldb/api/stores/doc_status.py:18) acepta: name, Model/name o Model:name, ruta trackeada, opcionalmente con prefijo alias: de un store enlazado (split_doc_ref de api/stores/doc_ref.py); no hay tabla de alias nueva.
q8 (include_linked): false = solo documentos del store dado; true = también los de los stores enlazados por stores add (los mismos que doc_status resuelve con alias:), y cada fila lleva export_id con el prefijo alias:. No sigue aristas.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_select_documents.py
- TMPDIR=/dev/shm pytest -q tests/store/test_queries_expanded.py
- TMPDIR=/dev/shm pytest -q tests/test_linked_structural.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb docs select --prefix P --one --format json sobre el store temporal del test
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, límite de clases por archivo; cuenta como test de los archivos tocados aunque output_scope no lo nombre)
- git fetch y rebase sobre origin/main antes de integrar (main trae SV01, SV02, SV04 en 6ba8bb20 y GO04 en d7eefdeb); en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con documentos de dos modelos (uno hereda del otro) en dos carpetas: --prefix único resuelve con --one y uno ambiguo falla listando candidatos; exacto gana a prefijo; --path-glob "sub/**/*.md" devuelve solo los de la subcarpeta; --model Base incluye al heredero; --where status = "open" filtra con cero llamadas a Validator.extract (contadas); la combinación de claves es conjunción; --one sin resultados da el error existente de documento desconocido; los goldens de sldb query glob/find no cambian; GET /docs/select responde igual que la CLI; CHANGELOG; docs/architecture/selectors.md; nota de cierre a deskops.

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
from sldb.api.documents.create_document import create_document
from sldb.api.documents.delete_document import delete_document
from sldb.api.documents import document_ast, build_document_ir_json, leaf_paths, runtime_document, extract_document_payload, render_document_markdown, render_model_template
from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.documents.document_reference import DocumentReference
from sldb.api.documents.document_serialization import serialize_document
from sldb.api.documents.payload_path_reading import deep_get, ensure_list
from sldb.api.documents.payload_path_writing import deep_delete, deep_set
from sldb.api.documents.payload_save import save_document_payload
from sldb.api.documents.track_document_file import track_document_file
from sldb.api.documents.untrack_document import untrack_document
from sldb.api.edges.check_edges import check_edges
from sldb.api.edges.edge_check_report import EdgeCheckReport
from sldb.api.edges.edge_reading import edge_node, edge_nodes_of_type, edges_from, edges_to, load_edge_index
from sldb.api.edges.apply_effects import apply_effects
from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edges_holding import edges_holding
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
from sldb.api.rules import refuse_unknown_family, rules_check, rules_explain
from sldb.api.where import where_matches
from sldb.store.query_engine.where_parse import WherePredicateError
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
    "DocRefStatus", "doc_exists", "doc_status", "tracked_documents", "AmbiguousDocument", "indexed_model_bases", "resolve_indexed_document", "split_doc_ref", "store_links",
    "WherePredicateError", "apply_effects", "edges_holding", "effects_of", "refuse_unknown_family", "rules_check", "rules_explain", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
]

FILE:src/sldb/store/query_engine/structural_queries.py
from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from sldb.store.query_engine.structural import _model_scope_docs
from sldb.store.graph.language.predicate_documents import document_matcher
from sldb.store.query_engine.store_prefix import split_store, with_store


def glob_structural(
    store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
) -> list[str]:
    """Matches structural addresses against a glob pattern."""
    return StructuralQueryEngine.glob_structural(store_path, pattern, resolve_model_ref, pythonpath)

def find_structural(
    store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
) -> list[str]:
    """Finds documents matching a structural scope and filter."""
    return StructuralQueryEngine.find_structural(store_path, address, where, resolve_model_ref, pythonpath)

class StructuralQueryEngine:
    """Engine for processing glob and find queries on structural nodes."""

    @classmethod
    def glob_structural(
        cls, store_path: Path, pattern: str, resolve_model_ref, pythonpath: str | None = None
    ) -> list[str]:
        """Matches structural addresses against a glob pattern."""
        store, pattern = split_store(pattern)
        match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}\.([^.]+)(?:\.(.+))?", pattern)
        if not match:
            return []
        model_name, recursive_flag, doc_pattern, field_pattern = match.groups()
        docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        return cls._glob_docs(docs, doc_pattern, field_pattern, base_scope)

    @classmethod
    def _glob_docs(cls, docs, doc_pattern: str, field_pattern: str | None, base_scope: str) -> list[str]:
        results: list[str] = []
        for doc in docs:
            if not fnmatch.fnmatch(doc.name, doc_pattern):
                continue
            if field_pattern is None:
                results.append(f"{base_scope}.{doc.name}")
                continue
            cls._glob_fields(doc, field_pattern, base_scope, results)
        return sorted(results)

    @classmethod
    def _glob_fields(cls, doc, field_pattern: str, base_scope: str, results: list[str]) -> None:
        for field_name in sorted(doc.payload.keys()):
            if fnmatch.fnmatch(field_name, field_pattern):
                results.append(f"{base_scope}.{doc.name}.{field_name}")

    @classmethod
    def find_structural(
        cls, store_path: Path, address: str, where: str, resolve_model_ref, pythonpath: str | None = None,
    ) -> list[str]:
        """Finds documents matching a structural scope and filter."""
        store, address = split_store(address)
        match = re.fullmatch(r"st\.\{([^{}+]+)(\+)?\}", address)
        if not match:
            return []
        return cls._find_docs(match, store_path, where, resolve_model_ref, pythonpath, store)

    @classmethod
    def _find_docs(cls, match, store_path: Path, where: str, resolve_model_ref, pythonpath: str | None, store: str | None = None) -> list[str]:
        model_name, recursive_flag = match.groups()
        docs = _model_scope_docs(store_path, model_name, bool(recursive_flag), resolve_model_ref, pythonpath, store)
        base_scope = with_store(store, f"st.{{{model_name}{'+' if recursive_flag else ''}}}")
        predicate = document_matcher(where)  # once per query; unparseable predicates raise
        return sorted(
            f"{base_scope}.{doc.name}"
            for doc in docs
            if predicate(doc, resolve_model_ref, pythonpath)
        )

FILE:src/sldb/cli/parsers/docs1.py
from __future__ import annotations
import argparse
from sldb.cli.output_format import add_format
from .docs2 import _add_docs_part2

def add_docs_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("docs", help="Tracked document workflows.", epilog="Note: `recover` and `compose` work on explicit Markdown links and transclusions.")
    sub = p.add_subparsers(dest="docs_command", required=True)
    _create(sub); _track(sub); _update(sub); _untrack(sub); _delete(sub); _show(sub); _exists(sub)
    _add_docs_part2(sub)

def _create(s):
    a = s.add_parser("create", help="Create and track document.")
    a.add_argument("--model", required=True)
    a.add_argument("-o", "--output", required=True)
    a.add_argument("payload", help="Data file or inline YAML/JSON")
    a.add_argument("--name", help="Doc name")
    a.add_argument("--store", help="Store path")
    a.add_argument("--pythonpath", help="Project path")

def _track(s):
    t = s.add_parser("track", help="Track existing doc.")
    t.add_argument("path", nargs="?", help="Document path")
    t.add_argument("--glob", help="Track every file matching this pattern (already tracked ones are skipped), e.g. 'docs/**/*.md'")
    t.add_argument("--model", required=True)
    t.add_argument("--name", help="Doc name")
    t.add_argument("--store", help="Store path")
    t.add_argument("--pythonpath", help="Project path")
    t.add_argument("--force", action="store_true")

def _update(s):
    u = s.add_parser("update", help="Update doc content.")
    u.add_argument("doc", help="Doc name or path")
    u.add_argument("payload", help="Data file or inline YAML/JSON")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")
    add_format(u)

def _untrack(s):
    rm = s.add_parser("untrack", help="Remove a tracked doc from the store, keeping its file.")
    rm.add_argument("doc", help="Doc name or tracked path")
    rm.add_argument("--store", help="Store path")
    rm.add_argument("--pythonpath", help="Project path")

def _delete(s):
    d = s.add_parser("delete", help="Untrack a doc AND delete its Markdown file.")
    d.add_argument("doc", help="Doc name or tracked path")
    d.add_argument("--store", help="Store path")
    d.add_argument("--pythonpath", help="Project path")
    d.add_argument("--yes", action="store_true", help="Do not ask for confirmation")

def _show(s):
    sh = s.add_parser("show", help="Show document AST and payload.")
    sh.add_argument("doc", help="Doc name or Model/DocName or tracked path; 'alias:ref' for a directly linked store")
    sh.add_argument("--store", help="Store path")
    sh.add_argument("--pythonpath", help="Project path")
    sh.add_argument("--format", choices=("json", "yaml"), default="json")

def _exists(s):
    e = s.add_parser("exists", help="Check that a doc reference resolves, here or in a linked store, without importing it.",
                     epilog="Exit codes: 0 ok, 1 missing, 2 ambiguous, 5 link-missing or link-broken.")
    e.add_argument("ref", help="Doc name, Model/DocName or tracked path; 'alias:ref' for a directly linked store")
    e.add_argument("--store", help="Store path")
    e.add_argument("--format", choices=("text", "json"), default="text")

FILE:src/sldb/cli/parsers/docs2.py
from __future__ import annotations
import argparse

def _add_docs_part2(sub):
    _recover(sub); _list(sub); _compose(sub); _explore(sub); _history(sub)

def _history(s):
    h = s.add_parser("history", help="The document's committed versions from git: who signed each one and which fields moved.", epilog="Example:\n  sldb docs history roadmap --since 2026-10-01 --format json")
    h.add_argument("doc", help="Doc name or Model/DocName or tracked path")
    h.add_argument("--since", help="Only versions committed at or after this ISO date")
    h.add_argument("--store", help="Store path")
    h.add_argument("--pythonpath", help="Project path")
    h.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _recover(s):
    r = s.add_parser("recover", help="Resolve [[links]] and report their targets.", epilog="Example:\n  sldb docs recover roadmap --store .sldb")
    r.add_argument("doc", nargs="?", help="Doc name or path")
    r.add_argument("--all", action="store_true", help="Check every tracked document")
    r.add_argument("--glob", help="Also check files matching this pattern, e.g. 'docs/**/*.md'")
    r.add_argument("--fail-on-custom", action="store_true", help="With --all/--glob: exit 1 also for predicates missing from the store")
    r.add_argument("--store", help="Store path")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    r.add_argument("--depth", type=int, default=1)
    r.add_argument("--links-only", action="store_true")
    r.add_argument("--include-transclusions", action="store_true")

def _list(s):
    l = s.add_parser("list", help="List tracked documents.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _compose(s):
    c = s.add_parser("compose", help="Expand ![[transclusions]] into composed Markdown.")
    c.add_argument("doc", help="Doc name or path")
    c.add_argument("--store", help="Store path")
    c.add_argument("-o", "--output", default="-", help="Output path or - for stdout")
    c.add_argument("--format", choices=("markdown", "json", "yaml"), default="markdown")
    c.add_argument("--render-links", action="store_true", help="Turn [[x]] into Markdown links relative to the output file")

def _explore(s):
    e = s.add_parser("explore", help="Search tracked docs, repo docs, and docstrings.")
    e.add_argument("term", help="Search term or regex")
    e.add_argument("--source", choices=("all", "docs", "docstrings"), default="all")
    e.add_argument("--regex", action="store_true")
    e.add_argument("--docs-root", default="docs", help="Docs directory to scan")
    e.add_argument("--code-root", default="src", help="Python source directory to scan")
    e.add_argument("--max-results", type=int, default=20)
    e.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    e.add_argument("--store", help="Store used to anchor relative source roots")

FILE:src/sldb/cli/commands/docs.py
"""Docs CLI commands module."""
from __future__ import annotations
import json
from typing import Any
import yaml
from sldb.cli.commands.doc import DocCLI
from sldb.cli.commands.docs_exists import docs_exists
from sldb.cli.commands.docs_history import docs_history
from sldb.cli.commands.explore import ExploreCLI
from sldb.cli.commands.links import LinkCLI
from sldb.cli.graph_ops import ast_for_target
from sldb.cli.store_context import get_store_context
from sldb.api.stores.indexed_documents import indexed_documents

class DocsCLI:
    """Plural docs surface for the redesigned CLI."""

    def __init__(self) -> None:
        self._doc = DocCLI()
        self._explore = ExploreCLI()
        self._links = LinkCLI()

    def run(self, args: Any) -> int:
        """Run appropriate docs subcommand.
        Args:
            args (Any): CLI args.
        Returns:
            int: Exit code.
        """
        cmd = args.docs_command
        if cmd in {"create", "track", "update", "untrack", "delete"}:
            args.doc_command = {"create": "add"}.get(cmd, cmd)
            return self._doc.run(args)
        return self._run_subcommand(cmd, args)

    def _run_subcommand(self, cmd: str, args: Any) -> int:
        handlers = {"list": self.list, "show": self._show, "exists": docs_exists, "history": docs_history, "recover": self._links.recover, "compose": self._links.compose, "explore": self._explore.run}
        if cmd in handlers:
            return handlers[cmd](args)
        raise SystemExit(f"Unknown docs command: {cmd}")

    def _show(self, args: Any) -> int:
        payload = ast_for_target(args.store, args.pythonpath, f"docs/{args.doc}")
        print(yaml.safe_dump(payload, sort_keys=False) if args.format == "yaml" else json.dumps(payload, indent=2))
        return 0

    def list(self, args: Any) -> int:
        """List tracked documents in the store.
        Args:
            args (Any): CLI args.
        Returns:
            int: Exit code.
        """
        sp, _root = get_store_context(args.store, mode="readonly")
        docs = indexed_documents(sp)
        return self._render_docs(args.format, {"store": str(sp), "documents": docs}, docs, sp)

    def _render_docs(self, fmt: str, payload: dict[str, Any], docs: list[dict[str, str]], sp: Any) -> int:
        if fmt == "json": print(json.dumps(payload, indent=2))
        elif fmt == "yaml": print(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
        elif not docs: print(f"No tracked documents in {sp}")
        else:
            print(f"Tracked documents in {sp}:")
            [print(f"- {i['name']} ({i['model']}) -> {i['path']}") for i in docs]
        return 0

FILE:src/sldb/cli/serve/docs_routes.py
"""POST /docs/create|track|untrack: document lifecycle over the native sldb API.

All store logic comes from sldb.api, under the same lock /save uses.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from sldb.api import create_document, serialize_document, track_document_file, untrack_document
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.serve.responses import read_json_body
from sldb.cli.serve.save_plan import ID_PATTERN, bad, default_document_path
from sldb.cli.serve.save_routes import SAVE_LOCK
from sldb.core.exceptions import SLDBError, SLDBValidationError
from sldb.store.query import load_runtime_documents


def dispatch_docs(handler, route, store_path, project_root, pythonpath):
    request = read_json_body(handler)
    with SAVE_LOCK:
        return _ACTION_ROUTES.get(route, lambda *_: ({"ok": False, "error": f"Unknown route: {route}"}, 404))(request, store_path, project_root, pythonpath)


def create_action(request, store_path, project_root, pythonpath):
    name = request.get("name")
    if invalid_name(name) is not None or find_document(store_path, pythonpath, name) is not None:
        return invalid_name(name) or bad(f"Ya existe el documento {name}.", 409)
    target, error = create_probe(request, name, store_path, project_root, pythonpath)
    if error is not None:
        return error
    return run_and_serialize(lambda: create_document(store_path, request.get("model"), target, request.get("payload"), name=name, pythonpath=pythonpath), name, store_path, pythonpath)


def track_action(request, store_path, project_root, pythonpath):
    name = request.get("name")
    invalid = invalid_name(name) if name is not None else None
    if invalid is not None:
        return invalid
    target, doc_name, error = track_probe(request, name, store_path, project_root, pythonpath)
    if error is not None:
        return error
    return run_and_serialize(lambda: track_document_file(store_path, request.get("model"), target, name=doc_name, pythonpath=pythonpath), doc_name, store_path, pythonpath)


def untrack_action(request, store_path, project_root, pythonpath):
    name = request.get("name")
    doc = find_document(store_path, pythonpath, name) if isinstance(name, str) else None
    if doc is None:
        return bad(f"Doc '{name}' not found.", 404)
    response = {"ok": True, "doc": serialize_document(doc)}
    try:
        untrack_document(store_path, name, pythonpath=pythonpath)
    except SLDBError as exc:
        return bad(str(exc), 404)
    return response, 200


def create_probe(request, name, store_path, project_root, pythonpath):
    if not isinstance(request.get("payload"), dict):
        return None, bad(f"Contenido inválido: {name}.", 422)
    target = resolve_path(request.get("path"), request.get("model"), name, store_path, project_root, pythonpath)
    conflict = None if target is not None and not target.exists() else bad(f"El archivo de {name} ya existe; elige otro ID.", 409)
    return target, conflict or registration_error(store_path, request.get("model"), pythonpath)


def track_probe(request, name, store_path, project_root, pythonpath):
    target = resolve_path(request.get("path"), request.get("model"), name, store_path, project_root, pythonpath)
    if not isinstance(request.get("path"), str) or target is None or not target.is_file():
        return None, None, bad(f"El archivo {request.get('path')} no existe.", 404)
    doc_name = name or target.stem
    if find_document(store_path, pythonpath, doc_name) is not None:
        return None, None, bad(f"Ya existe el documento {doc_name}.", 409)
    return target, doc_name, registration_error(store_path, request.get("model"), pythonpath)


def run_and_serialize(operation, name, store_path, pythonpath):
    try:
        operation()
    except (SLDBValidationError, ValidationError) as exc:
        return bad(str(exc), 422)
    except SLDBError as exc:
        return bad(str(exc), 404)
    doc = find_document(store_path, pythonpath, name)
    return {"ok": True, "doc": serialize_document(doc)}, 200


def invalid_name(name):
    if isinstance(name, str) and ID_PATTERN.fullmatch(name):
        return None
    return bad("El ID nuevo solo admite letras, números, guiones y guiones bajos.", 400)


def registration_error(store_path, model, pythonpath):
    try:
        load_registered_model(store_path, model, pythonpath)
    except SLDBError as exc:
        return bad(str(exc), 404)
    return None


def resolve_path(raw, model, name, store_path, root, pythonpath):
    if raw is None:
        docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
        return default_document_path(model, name, docs, root)
    if not isinstance(raw, str):
        return None
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def find_document(store_path, pythonpath, name):
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    return next((doc for doc in docs if doc.name == name), None)


_ACTION_ROUTES = {"/docs/create": create_action, "/docs/track": track_action, "/docs/untrack": untrack_action}

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
from sldb.cli.serve.edges_documents_routes import dispatch_edges
from sldb.cli.serve.document_routes import DOCUMENT_ROUTES, dispatch_document
from sldb.cli.serve.corpus_routes import corpus_rank
from sldb.cli.serve.find_routes import dispatch_find
from sldb.cli.serve.graph_routes import dispatch_graph
from sldb.cli.serve.lint_routes import dispatch_lint
from sldb.cli.serve.models_routes import dispatch_models
from sldb.cli.serve.ast_routes import dispatch_ast
from sldb.cli.serve.fields_routes import dispatch_fields
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
    if route in DOCUMENT_ROUTES: return dispatch_document(handler, route, store_path, project_root, pythonpath)
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

FILE:tests/store/test_queries_expanded.py
import pytest
from sldb.store.query import (
    list_structural,
    get_structural,
    glob_structural,
    find_structural,
    list_semantic,
    glob_semantic,
    get_global_semantic,
)
from sldb.models.structured_doc import StructuredNLDoc
from pydantic import Field


class MockModel(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•content⸥"
    title: str = Field(description="Title")
    content: str = Field(description="Content")


def mock_resolve_model_ref(model_ref, pythonpath=None):
    return MockModel


@pytest.fixture
def populated_store(tmp_path):
    store_path = tmp_path / ".sldb"
    store_path.mkdir()
    (store_path / "core").mkdir()

    # Create a minimal store structure
    (store_path / "core" / "store_index.yaml").write_text("models: []\nstores: []\n")
    (store_path / "semantic_index.yaml").write_text("tags: {}\ndocuments: {}\n")
    (store_path / "semantic_dag.yaml").write_text("equivalences: {}\n")

    return store_path


def test_structural_list_root(populated_store):
    res = list_structural(populated_store, "st", mock_resolve_model_ref)
    assert isinstance(res, list)


def test_structural_list_invalid_address(populated_store):
    res = list_structural(populated_store, "invalid", mock_resolve_model_ref)
    assert res == []


def test_get_structural_invalid_address(populated_store):
    res = get_structural(populated_store, "invalid", mock_resolve_model_ref)
    assert res is None


def test_glob_structural_invalid_pattern(populated_store):
    res = glob_structural(populated_store, "invalid", mock_resolve_model_ref)
    assert res == []


def test_find_structural_invalid_address(populated_store):
    res = find_structural(
        populated_store, "invalid", "title='x'", mock_resolve_model_ref
    )
    assert res == []


def test_semantic_list_root(populated_store):
    # This will trigger rebuild_semantic_indexes because semantic_index is empty
    res = list_semantic(populated_store, "se", mock_resolve_model_ref)
    assert res == []


def test_glob_semantic_empty(populated_store):
    res = glob_semantic(populated_store, "se.*", mock_resolve_model_ref)
    assert res == []


def test_get_global_semantic_empty(populated_store):
    res = get_global_semantic(populated_store, "gse.type", mock_resolve_model_ref)
    assert res == []


class BaseDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title")


class ChildDoc(BaseDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•child_field⸥"
    child_field: str = Field(description="Child field")


def test_model_inheritance_query(tmp_path, monkeypatch):
    # Setup a store with a base and child model
    project_root = tmp_path
    store_path = project_root / ".sldb"
    store_path.mkdir()
    (store_path / "core").mkdir()

    # Mocking necessary files for store to function
    (store_path / "core" / "store_index.yaml").write_text("models: []\nstores: []\n")
    (store_path / "semantic_index.yaml").write_text("tags: {}\ndocuments: {}\n")
    (store_path / "semantic_dag.yaml").write_text("equivalences: {}\n")

    # In a real scenario we'd use CLI to add these, but we can simulate the runtime list
    from sldb.store.query import RuntimeDocument

    doc1 = RuntimeDocument(
        store_name="local",
        store_path=store_path,
        model_name="BaseDoc",
        model_type=BaseDoc,
        name="doc1",
        path="doc1.md",
        payload={"title": "Base"},
        semantic_tags=["type.base"],
    )
    doc2 = RuntimeDocument(
        store_name="local",
        store_path=store_path,
        model_name="ChildDoc",
        model_type=ChildDoc,
        name="doc2",
        path="doc2.md",
        payload={"title": "Child", "child_field": "x"},
        semantic_tags=["type.child"],
    )

    import sldb.store.query

    # Inject the two documents for this test only; a bare assignment here leaked into
    # every later test that loads runtime documents.
    monkeypatch.setattr(sldb.store.query, "load_runtime_documents", lambda *args, **kwargs: [doc1, doc2])

    # Test recursive listing (st.{BaseDoc+})
    res = list_structural(store_path, "st.{BaseDoc+}", lambda *a: BaseDoc)
    assert "doc1" in res
    assert "doc2" in res

    # Test non-recursive listing (st.{BaseDoc})
    res = list_structural(store_path, "st.{BaseDoc}", lambda *a: BaseDoc)
    assert "doc1" in res
    assert "doc2" not in res

FILE:tests/test_linked_structural.py
"""Store-qualified structural addresses: `B:st.{Model+}.doc` reads a linked store the way
`st.…` reads the local one, and results from a linked store carry the prefix back."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as sldb_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.query import find_structural, get_structural, glob_structural, list_structural

MODEL_SRC = (
    "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
    "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
    "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
)


def _store(root: Path, names: list[str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "linkfix_models.py").write_text(MODEL_SRC)
    assert sldb_main(["stores", "init", "--path", str(root)]) == 0
    assert sldb_main(["models", "add", "linkfix_models:NoteDoc", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    for name in names:
        (root / f"{name}.md").write_text(f"# {name}\n\nbody of {name}\n")
        assert sldb_main(["docs", "track", str(root / f"{name}.md"), "--model", "NoteDoc", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    return root


def test_a_linked_store_is_reached_by_prefix_and_answers_with_it(tmp_path: Path):
    a = _store(tmp_path / "a", ["alpha"])
    b = _store(tmp_path / "b", ["beta", "gamma"])
    assert sldb_main(["stores", "add", str(b / ".sldb"), "--name", "b", "--store", str(a / ".sldb")]) == 0
    sp = a / ".sldb"
    assert list_structural(sp, "st.{NoteDoc}", resolve_model_ref, str(a)) == ["alpha"]
    assert list_structural(sp, "b:st.{NoteDoc}", resolve_model_ref, str(a)) == ["beta", "gamma"]
    assert find_structural(sp, "b:st.{NoteDoc+}", 'body ~ "gamma"', resolve_model_ref, str(a)) == ["b:st.{NoteDoc+}.gamma"]
    assert find_structural(sp, "st.{NoteDoc+}", 'body ~ "gamma"', resolve_model_ref, str(a)) == []
    assert get_structural(sp, "b:st.{NoteDoc}.beta.body", resolve_model_ref, str(a)) == "body of beta"
    assert get_structural(sp, "local:st.{NoteDoc}.alpha.body", resolve_model_ref, str(a)) == "body of alpha"
    assert glob_structural(sp, "b:st.{NoteDoc}.*", resolve_model_ref, str(a)) == ["b:st.{NoteDoc}.beta", "b:st.{NoteDoc}.gamma"]
    assert find_structural(sp, "nope:st.{NoteDoc+}", "has(body)", resolve_model_ref, str(a)) == []

FILE:CHANGELOG.md
# Changelog

Version note (2026-09-13, updated 2026-10-18): `pyproject.toml` declares `0.1.12`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.13 — not released yet (no tag, not on PyPI)

- Anclas a documentos con hash de contrato (GO07, plan grafo-operable; `docs/architecture/anchoring.md` §6):
  - `StructuredNLDoc.__doc_anchors__` (nuevo atributo de clase): campos `str` o `list[str]` cuyos valores son vacíos o `doc:Model:name[@sha256:<64 hex>]`; la forma la valida un validador pydantic del modelo base (`sldb.models.doc_anchor_value`) y un valor malformado es `ValidationError` al escribir. `Provenance.from_` valida igual cada elemento que empieza por `doc:`; los demás (`code:...`) no cambian.
  - Al cargar un modelo (`resolve_model_ref`), `__doc_anchors__` que nombra algo que no es un campo `str`/`list[str]`, o un campo con el sufijo reservado `__anchor_state`, es `SLDBModelError` (`sldb.store.model_contract.doc_anchor_fields`).
  - `save_document_payload` pinnea: un ancla sin `@sha256` (en un campo `__doc_anchors__` o en `from:`) se guarda con el hash de contrato actual del destino (`contract_hash`, GO02 §5); un destino no trackeado deja el valor sin hash.
  - Cada ancla de un campo `__doc_anchors__` es una arista `references` con el nombre del campo hacia `Model:name` (sin el sufijo); `from:` no genera aristas.
  - `compose_edge_index` agrega en memoria `<campo>__anchor_state` (`intact` | `changed` | `lost`; lista alineada para `list[str]`) a la facet `payload`; no se escribe al shard y `EDGE_INDEX_VERSION` sigue en 5. El alias `anchor_state` del lenguaje también se lee al atravesar `^F` (desde el elemento alcanzado, que tiene el campo `F`).
  - `sldb.api.check_doc_anchors(store, pythonpath=None)` (también en `sldb.api.anchors`): alertas `anchors/doc_changed`, `anchors/doc_lost`, `anchors/provenance_changed`, `anchors/provenance_lost`; `sldb anchors check` las agrega (`doc_anchors` en la salida JSON, en `warnings` con `--envelope`), exit 0 si solo hay alertas. No hay `reconnected` para documentos.
- Transiciones como datos de la arista (GO09, plan grafo-operable; `docs/architecture/edges.md`):
  - Convención de `RelationDoc.attributes` para una transición: `sets` (mapa campo → escalar YAML o lista de escalares; `null` asignable) y `terminal` (booleano que sldb solo transporta); ausentes o `null` valen `sets = {}` y `terminal = false`; otras claves se conservan y no entran a los efectos. Es un validador pydantic de `RelationDoc` (`sldb.models.transition_attributes`): escribir un `RelationDoc` con `attributes` no mapa, `sets` no mapa, `terminal` no booleano o un valor de `sets` mapa o lista anidada se rechaza con `ValidationError`.
  - `EdgeRecord.effects` (nuevo, opcional): solo lo llena `edges_holding`, como `{sets, terminal}` con `{campo}` sustituido desde el sujeto (sintaxis de `where_subject`, escalar en su forma YAML: `true`/`false`, números, strings tal cual). Un `{campo}` ausente, `null` o no escalar hace que la arista no se cumpla. Con `effects = None` la clave no aparece en ningún dump: la salida de `edges_from`, `edges_to`, `sldb edges show` y los shards no cambia; `sldb edges show --holds-for` sí la muestra.
  - `sldb.api.effects_of(attributes, subject)` (la resolución) y `sldb.api.apply_effects(subject, effects, model)`: función pura que reemplaza o agrega las claves de primer nivel de `sets` en una copia del sujeto y valida el payload completo contra la clase `model` (levanta su `ValidationError`); nunca persiste.
- Reglas como documentos (GO06, plan grafo-operable; `docs/architecture/rules.md`):
  - `sldb.models.rule_doc.RuleDoc` (exportado en `sldb.models`): `subject` (`model <= X` o una conjunción de nivel superior de esos términos), `where` opcional, `condition`, `severity` (`error` | `alert`), `moment` (`on_write` | `on_transition` | `on_check`) y `message` opcional. Sus validadores pydantic rechazan una `condition` o un `where` que no parsean, un `subject` con otra forma y un valor fuera del vocabulario; escribir una RuleDoc cuyo `subject` nombra un modelo no registrado se rechaza con el error existente `Model 'X' not registered.` (`create_document`, `save_document_payload`, `sldb docs create|update`).
  - `sldb.api.rules` (`rules_check`, `rules_explain`, `explain_exit`, `refuse_unknown_family`; también en `sldb.api`): las reglas son las RuleDoc del store local, leídas de la proyección del índice y evaluadas con `GraphBackend.eval`.
  - CLI `sldb rules check [--subject DOC]`: cada resultado `false` es un `Finding` de core con la severidad de la regla y código `rules/<nombre>`; cada `incomplete`, un alert `rules/<nombre>/incomplete`. Sale 1 solo si hay algún error. Sin `--subject`, solo las reglas `on_check` sobre los documentos locales de su familia.
  - CLI `sldb rules explain RULE SUBJECT`: `data = {rule, subject, finding}` con el finding de eval (`node`, `holds`, `clause`, `seen`), también cuando se cumple; exit 0/1/2 por `holds` y 3 cuando la regla no aplica (`applies: false`, `reason: subject|where`, `detail`).
  - `contracts/layers.toml`: la arista `models → store` (el parser del lenguaje, importado de forma diferida por los validadores de `RuleDoc`) queda contada como R6 pendiente.
  - `docs/opsys/bridge_primitives/README.md`: la sección `Constraint` se marca como reemplazada por `RuleDoc`.
- Lenguaje de predicados unificado (GO05, plan grafo-operable; `docs/architecture/rules-language.md`):
  - `sldb.store.graph.language`: parser (`parse_predicate` → `Predicate`) y evaluador del lenguaje de GO02: `and`/`or`/`not` con paréntesis, caminos `campo`, `rel:<tipo>`, `^` y clausura `+` (pasos unidos por `.`), cuantificadores `any`/`all`/`none`, `count(...) cmp n`, sustitución `{campo}` desde el sujeto, `incomplete` (Kleene fuerte) en el borde de links y findings `{node, holds, clause, seen}`. `sldb.store.query_engine.rules` es la fachada de los tests de spec (52 verdes).
  - `GraphBackend.eval` evalúa caminos sobre el índice compuesto y, sin sujeto, el dominio entero (la proyección cargada, o todos los documentos). Al atravesar un campo `F` con `F__anchor_state` en el origen, cada elemento expone `anchor_state`.
  - API única: `where_matches`, `edges_holding`, `StructuredQuery` y `--where` evalúan con el lenguaje; nuevas `sldb.api.where.where_findings` (un store, sin re-extraer) y `where_records`.
  - CLI: `sldb find --where` acepta el lenguaje completo (caminos sobre el índice del store) y `--explain` agrega `findings` por documento evaluado. `sldb --envelope graph query` con filtros `FieldCondition` lleva un warning `deprecated/field-condition` que nombra el predicado de reemplazo; la salida no cambia.
  - Deprecados (GO10 los retira): `where_parse.compile_where`, `where_parse.where_parse` y construir `FieldCondition` emiten `DeprecationWarning`.
  - Cambios de resultado declarados (tabla de equivalencia, goldens en `tests/fixtures/where_goldens/`): `f != <número>` ya no cumple sobre un campo ausente; ordenar `None` o tipos mezclados da `false` en vez de `TypeError`; en `StructuredQuery`, `contains` sobre una cadena es subcadena e `is_null`/`is_not_null` tratan `""` como ausente.
- Transclusión de campos y segmentos ricos de diagramas y vistas en /document/segments (SV03):
  - `sldb.api.segments`:
    - `source_ref.py`: `SourceRef` incorpora el campo opcional `field: str | None = None`.
    - `composition_spec.py`: Soporta `ref: Literal["document", "field", "view", "spec"]`.
    - `composition_piece.py` y `field_segment.py`: incorporan los campos opcionales `projection: dict | None = None` y `table_data: dict | None = None`.
    - `field_ref_resolver.py`: `FieldRefResolver` resuelve referencias `Model:name#campo`, `docs/<Model>/<name>/<campo>` y `docs/<name>/<campo>` devolviendo `{model, doc, path, field, value, payload}`.
    - `segment_enrichment.py`: Enriquecimiento de segmentos con vistas resueltas (`resolve_view` / `evaluate_projection_view`) y tablas estructuradas (`table_data`).
    - `build_document_segments.py`: Inyecta `FieldRefResolver` en `render_with_spans` y enriquece los nodos con `projection` y `table_data`.
  - `sldb.models.structured_doc`: `StructuredNLDoc.compose_field` y `render_payload` aceptan `field_resolver`; cuando `ref == "field"`, resuelve campos remotos emitiendo `CompositionPiece` con `SourceRef(model, doc, path, field)`. Sin resolver inyectado, rinde vacío preservando la pureza del renderizador.
  - Documentación de arquitectura en `docs/architecture/segments-and-transclusion.md`.
  - Suite de tests en `tests/segments/test_field_transclusion_and_diagram_segments.py`.
- Visual notation and projection view resolver, store synchronization, CLI, and serve routes (SV02):
  - `sldb.api.notations`:
    - `notation_view.py`: `resolve_view` and `resolve_documents` resolving glyphs, compartments (`data.attributes`), template/keyword interpolation, edge ordering, UML fragments, and legends.
    - `projection_view.py`: `evaluate_projection_view`, `list_projection_views`, and `save_projection_view` evaluating node where-predicates, relation filters, layout, palette ink, and notation styling.
    - `notation_sync.py`: `sync_palette` and `sync_notation` writing `PaletteDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, and `RelationTypeDoc` into stores without intermediate YAML dependencies.
    - Re-exported in `sldb.api` and `sldb.api.notations`.
  - CLI: `sldb notations (list, sync, view, resolve)` with JSON output and envelope support (`sldb --envelope notations ...`).
  - HTTP serve routes in `sldb serve`: `GET /notations`, `GET /notations/view`, `POST /notations/resolve`, `GET /views/projection`, `GET|POST /views/projection/evaluate`, `POST /views/projection/save`.
  - Documentation updated in `docs/architecture/notations-and-views.md`.
  - Comprehensive test suite in `tests/notations/test_notation_view_and_routes.py`.
- Declaración y edición draft de containment, references, compositions, semantics y authority en modelos (SV04):
  - `sldb.api.create_model` y `ModelSource` aceptan `containment`, `references`, `compositions`, `semantics`, `authority`; validan que los campos referenciados existan y que las composiciones tengan marcador `⸢render•<name>⸥` en template (o lo generan en `default_template`), emitiendo las asignaciones correspondientes en el código Python generado.
  - `describe_model` y `ModelDescription` exponen `containment`, `references`, `compositions`, `semantics_map`, `authority`, `template`, `has_draft`, `draft_path`.
  - `sldb.api.edit_model_metadata` en `sldb.api.model_drafts` edita `__containment__`, `__references__`, `__compositions__`, `__semantics__` y `__authority__` en el `.draft.py` (`.py.temp`) mediante manipulación AST en `metadata_literals.py`, y sincroniza secciones de composiciones en el template.
  - `validate_template_contract` y `check_and_plan` validan coherencia de referencias/containment/compositions contra campos declarados y template, rechazando errores con `SLDBModelEditError`. `promote_model_draft(..., backfill=True)` re-renderiza documentos y reconstruye índices de modelo, semántico y de aristas.
  - Expuesto en CLI (`sldb models metadata edit`, `sldb models validate --promote --backfill`, y flags de creación) y HTTP serve (`POST /models/create`, `POST /models/metadata-edit`, `POST /models/promote` con `backfill`).
  - Documentación de arquitectura en `docs/architecture/model-authoring.md`.
- Visual vocabulary models, palettes and builtin notations absorbed from spec2viz (SV01):
  - 7 models in `sldb.models.notation_models` (re-exported in `sldb.models` and `sldb.api`):
    `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, and `ViewDoc`.
    `ViewDoc` adds optional `params: dict` and `sections: list` for GD25 convergence.
  - Submodule `sldb.notations` containing palette (`palette.py`), notation (`notation.py`),
    and styling (`styling.py`) engines, along with builtin `palettes/default.yml` and the 8 builtin
    notations in `builtin/` (`uml-class`, `statechart`, `component`, `deployment`, `uml-sequence`,
    `activity`, `component-view-matrix`, `reflection`).
  - `resolve_model_ref` maps legacy `spec2viz.sldb_models:<Model>` references to
    `sldb.models.notation_models:<Model>` for transparent backwards compatibility with existing stores.
  - Architecture documentation in `docs/architecture/notations-and-views.md`.
- Each document node of the edge index carries its projected payload (GO04): `EdgeNodeRecord`
  gains `payload` (top-level fields holding a scalar or a list of scalars; dicts and lists of
  non-scalars are left out; a model's `__indexed__` picks exactly those names), `field_hashes`
  (the entry's whole map), `source_hash` (hash_c) and `contract_signature` (sha256 of the model's
  field names and `__references__` / `__containment__` / `__compositions__` names), persisted in
  the shard; other nodes leave them empty. `EDGE_INDEX_VERSION` 4 -> 5: a version-4 shard reads
  as stale and is rebuilt on the next write or `stores build`. `EdgeIndex.stale` now also names
  a document whose Markdown was edited outside sldb and one built under another contract
  signature of its model (a new `__references__` entry). `StructuredQuery` filters on
  `FacetFilter(facet="payload", ...)` from the shard, with no re-extraction; a filter on a field
  no model projects raises `SLDBGraphArgumentError` naming it. An `__indexed__` name that is not
  a field or not scalar is `SLDBModelError` when the model loads. Existing queries answer as
  before. Edge index of this repo after `sldb stores build` (`du -sb` of the edges shards root,
  MB = 10^6; shards = `.yaml` files there; 2026-11-06): before (main 804f1ad4) 47.64 MB in
  3116 shards; after (wt/go04 on c1e50419, which tracks more documents) 58.54 MB in 3277 shards.
  `docs/architecture/graph-backend.md` documents the projection and what it leaves out.
- A bare id in a reference field that allows a model also names a document of one of its submodels
  (`depends_on: task-x` with `TaskDoc` allowed names `TaskCodeDoc:task-x`), read from `base_models`
  of the model nodes in the composed index (an inherited model's node takes them from its class, since
  its local index keeps none). The allowed model itself wins; several submodels with that
  name stay `ambiguous`. `resolve_indexed_document` also reads the bases of an inherited model from
  its owner store.
- `sldb.api.resolve_indexed_document(store_path, model, name)` finds `Model:name` when the document is
  tracked under a submodel of `Model` (`TaskDoc:task-x` finds `TaskCodeDoc:task-x`): an instance of a
  submodel is an instance of its bases, read from `base_models` in the model indexes, without importing
  any class. An exact match on the model wins; two submodels tracking the same name raise
  `AmbiguousDocument`. Consumers such as graph_ui resolve ids through it instead of comparing model names.
- The whole-graph analyses sit behind a `GraphBackend` seam (`load`, `eval`, `analyze`).
  `NetworkXBackend` wraps `sldb.store.graph.analysis` unchanged, so the six `sldb graph`
  analyses and the ten `api/graph/analyze.py` functions print the same output as before and
  can be given another backend by Python for tests. A store selects it with
  `graph_backend` in `.sldb/store.yaml`: absent means `networkx`; any other value fails on
  load with `graph_backend <value> no admitido; admitidos: ["networkx"]`. `eval` implements
  the GO02 subset without paths (finding shape in `rules-language.md` §4 and §6); a path
  raises `NotImplementedError` until GO05. `docs/architecture/graph-backend.md` fixes the
  seam: a future engine (Kùzu, Neo4j, Datalevin) enters behind it and the rules never see it.
- A project's declared-edge graph as a library (`sldb.api.edges.project_graph`): `ProjectGraph(root,
  ProjectGraphConfig)` reads the documents of configured surfaces and the files path rules
  classify as nodes, the schema edges and unresolved values of the project's own store from its
  cached composed edge index (`include_linked=False`), and from each document's text what its
  model does not declare (configured mapping fields, fenced YAML blocks, mentions under headings
  or on every line). `edges_from(node)` / `missing_from(node)` read one source alone and give
  what `extraction()` gives for it, so a reader asking about a few documents reads only those.
  The project owns only the configuration (deskops' desk is the first, `deskops/graph/desk_graph.py`).
  New `sldb.api.tracked_documents(store, refs)`: `doc_status` for many references from one read
  of the documents index.
- The store splits in two sibling directories: `.sldb/` (`store.yaml` and `core/`) is
  versioned whole, so that git holds the tree's past, and `.sldb_cache/` (edges, sections,
  semantic shards, graphs, locks; `.sldb/runtime/` until now) is regenerable and ignored
  (`docs/architecture/derived-store-boundary.md`; owner's decision, 2026-10-29).
  `sldb stores init` adds the line `.sldb_cache/` to the root `.gitignore` (idempotent, no
  other line touched); `sldb stores check` reports the error `stores/core_ignored` (exit 1)
  when git ignores `.sldb/core/` or `.sldb/store.yaml` and the alert `stores/cache_not_ignored`
  (exit 0) when the cache is not ignored; `stores build --check` leaves `.sldb_cache/` out of
  its copy. New `sldb stores migrate-layout [--store PATH] [--force]` moves the content of
  `.sldb/runtime/` to `.sldb_cache/` (refusing a non-empty cache unless `--force`, which
  deletes it first), deletes the journal without archiving it, removes `.sldb/runtime/` and
  rewrites the root `.gitignore`: only the lines whose pattern is `.sldb/core` or
  `.sldb/runtime` go, `.sldb_cache/` comes in, everything else stays verbatim. The
  `selfdoc python-sync` graph defaults to `.sldb_cache/graphs/python-source.graph.json`.
- The write journal is retired (2026-11-04): no write through `sldb.api` produces one, and
  `sldb journal show` (and `verify`) print `El journal fue retirado el 2026-11-04; el pasado
  del store se consulta con sldb docs history <doc>.` and exit 0. `sldb.api.journal()` answers
  `[]` and `verify_journal()` a valid, empty report, for importers; `SLDB_JOURNAL_OFF` is gone;
  the `actor` parameters stay (they still stamp a document's provenance where they did).
  `docs/architecture/journal-authority.md` records the decision: the tree is the authority
  and git is its memory.
- Edges can carry their evidence, on request: `sldb edges show --evidence` and
  `sldb.api.edges.edge_evidence.stamp_evidence` add `metadata.evidence` with `ref_hash` (the
  target's `content_hash`, a model's `model_hash`; for a section its document's, flagged
  `ref: document`, since sections have no hash of their own), `contract` (the source model's
  `contract_hash`) and `engine` (`{name, version}`) or, for an authored edge, `actor`
  (`relation_doc:<name>`). No timestamp. Computed on read, so the shards do not change, and
  `ref_hash` is the target's current hash: telling an edge went stale takes a caller that kept
  an earlier evidence to compare.
- `sldb --envelope <command> ...` prints one JSON value per run, `{ok, command, store,
  revision, data, warnings}` or `{ok: false, error: {type: "ns/name", message}, exit}`, and
  exits with a typed code: 0 ok, 1 missing, 2 ambiguous, 3 rejected input, 4 busy, 5 store or
  runtime failure, 6 usage, 70 unexpected (`docs/cli-envelope.md`). Opt-in: without the flag
  the CLI prints and exits as before, because callers parse that output today.
- `sldb stores declare` and `sldb stores build`. A store's source is `.sldb/store.yaml`: the
  models it registers (local, or inherited from a linked store), its links, its predicates,
  the generators that write derived documents (such as `selfdoc python-sync`), the paths
  they write, and `include` rules saying which file is tracked under which model and name.
  The index and the model and document indexes are rebuilt from it by `stores build`
  (idempotent); `stores build --check` rebuilds a scratch copy of the sources and fails when
  that copy does not pass `stores check`, a tracked document is not declared, or it tracks
  something other than the local store. `stores declare --write` writes the declaration the
  current index implies, to adopt the layout. Tracking or untracking a document through the
  API keeps the declaration current (a file outside the project is not declared), `stores
  check` notes a declared store whose `.sldb/core/` is versioned rather than ignored, and a
  declared file that is gone is reported by `build` as `missing`. `declare --write` writes
  the declaration the index implies: a model whose source is outside the project
  (sldb's own, from the installed package) is declared by `model_ref` alone, and a glob is
  written only for a folder with more than one tracked file, all of one model. Design:
  `docs/architecture/derived-store-boundary.md`.
- An inherited model whose owner uses a `src/` layout imports again. The import root was the
  owner's project root, so pron's models, which live under its `src/` directory, stayed unimportable in a
  store that inherits them; it is now the directory the owner's registered path puts the
  package in (`sldb.store.model_import_root`). sldb's own store inherits AnchorDoc,
  ProjectionDoc and MoveDoc from pron through a relative link (`../pron/.sldb`) instead of
  registering copies pinned to an absolute path that no longer existed.
- **Python 3.12 or newer is required** (`requires-python >=3.12`; it was `>=3.10`). Python
  3.10 reaches end of life this month, and the whole suite (sldb, deskops, spec2viz, graph_ui)
  moves to the same floor. CI tests 3.12 and 3.13. The compatibility code for 3.10 is gone:
  the `tomllib`/`tomli` fallback in the `tools/check_*.py` gates and the conditional `tomli`
  dev dependency. `uv.lock` is regenerated for the new floor.
- The pre-redesign singular groups `sldb store`, `sldb model` and `sldb doc` run again: they
  were parsed (and listed by `sldb doc --help`) but had no handler, so `sldb doc untrack`
  answered `Unknown command: doc`. The plural groups (`stores`, `models`, `docs`) remain the
  documented spelling.
- A change to a model's contract now rebuilds the edges of its documents. Adding
  `__reference_models__` to a model and running `stores update` used to reuse every document's
  edges shard (its hashes had not moved), so the new references never reached the index and
  `edges rebuild` walked nothing until the shards were deleted by hand. Each shard now records
  the contract it was built under; the first rebuild after upgrading rewrites every shard once.
- A store link can be removed or pointed elsewhere: `sldb.api.unlink_store(store, name)` /
  `sldb stores remove <name>`, and `link_store(..., replace=True)` / `stores add --replace`.
  Removing a link a model here is inherited from is refused (replace it instead). A link to a
  directory that is gone was only fixable by editing `store_index.yaml`; `stores check` now
  notes it (`broken_links` in `check_store`).
- A scalar list item reads back as written. An item whose text markdown reads as block syntax
  was lost or mangled on extract: `validation: ["```bash", "pytest", "```"]` came back as
  `["pytest"]` (so any rewrite of the document deleted the fence lines), and `# x`, `> x`,
  `- x`, `1. x`, `***`, `<b>` or a leading space lost their syntax. Such an item is now rendered
  with one leading backslash (a CommonMark escape) and extracted without it; only a value that
  opens its item (`- ⸢rev,list•x⸥`) is escaped. A hand-written item that already began with
  `\` before such syntax now reads without that backslash.
- Extracting and validating no longer re-parse the model's template each time: a template's
  recipes are computed once per template, `validate` renders once instead of twice, and the
  sections index reuses one markdown-it parser. On sldb's own store, extracting 153 documents
  went from ~420 ms to ~275 ms and their sections from ~205 ms to ~175 ms.
- The markdown AST keeps what a token carries beyond its text, in `SLDBNode.metadata`: a
  fence's language (`info`), its opening markup (`markup`) and its attributes.
- `sldb edges show <name>` with something that is no node of the index fails, and suggests the
  document's export id (`Did you mean PillDoc:pill-008?`), instead of printing `[]` as for a
  real node without edges.
- `models show`, `models template show` and `docs update` take `--format text|json|yaml`
  (`models show` keeps YAML as its default; the template comes wrapped as
  `{model, draft, path, template}`; `docs update` reports `{updated, model, path}`). An
  argument a subcommand does not know is reported with that subcommand's usage, not the
  root's.
- A model's `__family__` changed in the class reaches the store: `stores update` and
  `models update` re-read it (it was written only at `models add`).
- `sldb.api.registered_models(store)` and `is_model_registered(store, model)` (by name,
  `module:Class` or `module.Class`), and `sldb models check <model>...`, which reports each as
  registered or missing and exits 1 if any is missing.
- `stores check` notes ignore rules that break the store's split (`.sldb/core` ignored, or
  `.sldb/runtime` not ignored); `check_store` returns it as `gitignore_policy`.
- A registered model that does not import here no longer takes the store's AST down: it is
  listed with `resolved: false` and the error (a healthy model's entry is unchanged), so `models show` and `ast show` of the rest
  answer (in an environment without `pron`, `models show TaskDoc` failed).
- `models template show` (and every draft operation) finds a model's source by importing its
  `model_ref` when the recorded path is not a file here: a store copied without its models,
  an absolute path from another machine, or an inherited model, whose path is empty and
  failed with `Is a directory`. When neither works, the error names the model and the store.
- A template's literal paragraph (deskops' `_Describe the incoming message..._`) anchors only a
  paragraph with that text. A document written without the placeholder had its first real
  paragraph taken for it and dropped on extract, so any rewrite deleted it (the first
  paragraph of inbox notes; `why`, `goal` and `done_when` of a task). Documents that lacked
  the placeholder now extract more: `stores check` reports them as `data_mutation` until
  `sldb models update <Model>` re-extracts the model (`stores update` trusts a document whose
  text did not move). Headings still anchor by position.
- A document that ends before its template does keeps its last section: a field of a section
  the document does not have (`## When`, after a document that stops at `## Why`) no longer
  claims the last section's paragraph, which came out empty and was erased by any rewrite.
  Past a missing heading, only later headings end a section. The `purpose` of three of
  sldb's rituals came back (`models update RitualDoc`).
- `stores check` names the documents a rewrite would lose content from: blocks of the file
  that do not survive `render(extract(text))`, because the model does not read them (written
  by hand, or by an older template). Their hashes are consistent over the poor extraction, so
  nothing else showed it. Sections the template fills only with `render`/`py` markers are
  regenerated and not counted. `check_store` returns it as `rewrite_loss`.
- `stores check --quiet` prints the PASS/FAIL line alone, as documented: it printed the
  per-document notes too, and now also skips the scans behind them.
- A `data_mutation` over text that did not move (and an unchanged contract) is explained as
  what it is, sldb reading the same file differently after an upgrade, and points to
  `sldb models update <Model>`: `stores check` said `stores update` would accept it, but
  `stores update` trusts unchanged text and did nothing. It no longer asks for a decision.
- `stores check` says, for a document whose text disagrees with its index, where the indexed
  text sits in the file's git history: `stale` (an earlier committed version, with the commit:
  the index fell behind), `unmatched` (no committed version has it: an edit indexed and never
  committed, or damage), `orphan` (the file is gone) or `undetermined` (not a git work tree),
  with the `git log` command that shows it. The JSON report carries it as `history`.
- `sldb.store` imports the rest of sldb through three seams only: `store/exceptions.py`
  (errors), `store/runtime_codec.py` (extraction) and `store/model_contract.py` (what a model
  class declares, and the built-in relation types); it imports nothing from `sldb.api`, `cli`
  or `selfdoc`, and `tests/test_store_seams.py` keeps it so. `describe_field` and the field
  kinds moved to `sldb.models.field_schema` (still importable from `sldb.api.schema`), which
  closes the store → api edge R4 in `contracts/layers.toml`.
- `selfdoc python-check` and `python-sync` work again: a property with a setter (or an
  `@overload`) was two symbols with one document id, and both commands failed with "Python
  symbols collide". A name redefined in its scope is now one symbol.
- kgdb is part of sldb, and nothing invokes an external `kgdb` any more. `selfdoc python-sync`
  writes the source graph with sldb's own graph IO instead of running `kgdb ingest` (it failed
  once the separate package was gone). `--kgdb-command` and `--kgdb-output` were removed and
  are refused with a clear error; the graph goes to `--graph-output`, by default
  `.sldb/runtime/graphs/python-source.graph.json` (it was `.kgdb/python-source.graph.json`).
  `sldb.selfdoc.kgdb_sync` is now `sldb.selfdoc.source_graph_file` (`write_source_graph`), and
  the selfdoc report's `kgdb_stale` is `graph_stale`. The data contract
  `sldb_kgdb_semantic_export` keeps its name (see the entry on kgdb names below).
- Docstring metadata is parsed strictly (`sldb.selfdoc.docstring_metadata`, spec section 2):
  only an opening line exactly `---` starts it, a closing `---` is required, and the block is a
  YAML mapping with unique keys among `id` (required), `kind` and `tags` (`namespace:value`,
  deduplicated). Malformed metadata and an id declared twice are reported as `path:line:
  problem` in the selfdoc report's `metadata_errors`, and `selfdoc python-sync` writes nothing
  while any remain; they were silently ignored and the declaration lost its identity.
- The source graph gives every module and symbol node its `local_tags` and `effective_tags`,
  inherited along the lexical chain package -> module -> class/function -> nested declaration
  within the scan (spec section 3): `system:*` and `workspace:*` from the nearest declaration,
  `topic:*` as a union, any other tag local only; nothing through imports, base classes or
  siblings. Each effective tag names the declaration and `path:line` it comes from. Two
  `system:` (or `workspace:`) tags on one declaration are a metadata error.
- An import in the source graph follows explicit re-export chains to the definition
  (`from sldb.api import open_store` reaches `sldb.api.stores.open_store:open_store`), through
  module-level imports only, with the chain in the edge's `via`; `from pkg import submodule`
  reaches the submodule. A star import, a cycle or a module outside the scan stays
  unresolved. A relative import inside a package's `__init__.py` resolves against that
  package (it was resolved against the parent: `pkg.impl` for `pkg.inner.impl`).
- `stores check` reuses its per-document content scans (rewrite loss and structural noise)
  while a document's text, its model's contract and the sldb that reads it have not moved, in
  the user's cache directory; the rewrite-loss scan also reuses the extraction the check
  already has instead of extracting again. On sldb's store (2775 documents) a full check went
  from 43 s to 23 s cold and 7 s warm, with the same findings.
- The source graph keeps the condition an import lives under (`context`: `type_checking`,
  `conditional`, `try`), and marks an import a later same-scope binding shadows
  (`shadowed_at`); a reference after the shadowing no longer resolves to the import.
- `selfdoc python-check` reports, apart from errors and drift, the declarations without
  metadata (`undeclared`), the declared ones without an explanation (`unexplained`) and the
  annotation references nothing resolves (`unresolved_references`, which were dropped).
- A symbol document's `purpose` is generated from the first paragraph of its docstring when it
  is a placeholder or was generated before; an authored purpose is kept and listed in
  `purpose_conflicts` for a decision.
- `selfdoc python-sync` reports on what is on disk after writing: it reported the plans made
  before writing, so a sync that wrote everything returned 1.
- Deleting `.sldb/runtime/` and rebuilding brings the sections and semantic indexes back. The
  user cache (`~/.cache/sldb/runtime-cache-built/`) and the in-process dirty set vouched for
  shards that were gone, so a rebuild wrote only the edges and a graph snapshot lost
  `has_section` and `semantic_parent` (reported by graph-ui).
- The last kgdb names in sldb's public surface are sldb's now (kgdb merged into sldb):
  - `sldb.store.export.export_kgdb_semantic_payload` is `export_semantic_payload`;
  - the semantic export contract keeps its name, `sldb_kgdb_semantic_export` version 1, and so
    do its schema and fixture (`contracts/schemas/sldb_kgdb_semantic_export.schema.json`,
    `contracts/fixtures/sldb_kgdb_semantic_export.v1.json`). It is a frozen data identifier,
    like the `sldb://...` node ids: renaming a data contract breaks every reader of files
    already written, so a format change goes behind a new contract version, never a rename.
    Main wrote `sldb_semantic_export` for a while before release; an export under that name is
    still read, never written. `tests/store/test_export_contract_frozen.py` pins the contract,
    the ids and the keys of the store index and of the document entries. The reading function is `sldb_semantic_export_to_snapshot`;
  - `stores semantic-export --format kgdb` is `--format sldb`;
  - the `sldb serve` route `/kgdb/snapshot` is `/semantic-export`;
  - the store's tracked relation types moved from `kgdb/relation_types/` to
    `sldb/relation_types/`, where `edges init` already wrote the new ones.
- `stores init` fails cleanly: what a failed init wrote is removed, the message says where it
  failed and what to check (instead of `Unexpected: [Errno 13] ...`), and the exit code tells
  a caller what happened: 0 created or already there, 2 the place refused it (permissions),
  1 failed half-way. `init_store` raises `StoreInitError` (an `SLDBStoreError`).

## 0.1.12 - 2026-10-18 — declared references resolve bare ids and paths, and report what names nothing

- Declared references resolve bare ids and paths. A value of a `__references__` or
  `__containment__` field names its document as an export id, as the path a tracked document
  lives at, or as a bare id tried against the models the field allows — the new
  `__reference_models__ = {"field": ["Model", ...]}`, or the containment list; one match
  resolves, several are `ambiguous`. It is decided when the index is composed, so tracking the
  target later resolves it. What names nothing is reported, never an edge:
  `sldb.api.unresolved_references(store)` / `sldb edges unresolved` /
  `EdgeIndex.unresolved_references` (`UnresolvedReference`: source, model, field, target,
  target_export_id, relation, reason, source_path). A free reference field only reports export
  ids. `EDGE_INDEX_VERSION` is 4: shards rebuild. `__reference_models__` enters the contract
  hash only for a model that declares it.
- An edge sldb derives (structural, schema, alias) is checked against sldb's own definition of
  its builtin type, even where the store authored a type under that name (selfdoc's code
  `contains` / `references`).
- `edges check` of a store that links others fails only on its own edges: what only a linked
  store's edges commit (an owner's stale shards, its cardinality violations) is reported apart
  (`EdgeCheckReport.linked_errors`, `linked_stale`; a `note:` line in the CLI). Edges read
  from a linked store carry `metadata["from_store"]`.
- Inheriting a model into a store (`models inherit`, or `alias:Model` on first use) signs its
  empty roster, so `stores check` passes without a `stores update` first.
- A section no longer counts as the owner of a path: a bare composition or reference value
  equal to a heading path resolved to that section instead of a document.

## 0.1.11 - 2026-10-18 — models are defined once and inherited; a free `attributes` on relations

- `RelationDoc.attributes`: a free dict of the edge's own attributes (a multiplicity, a role, a
  transition's action), written in the frontmatter and copied to the index edge as
  `metadata["attributes"]`. A RelationDoc written before has none. Its contract moved: run
  `sldb stores update` in a store that tracks RelationDoc documents.
- `sldb.api.StructuredNLDoc`: the base class of models, from the public surface.
- `sldb.api.graph.query_snapshot(snapshot, query)`: a StructuredQuery over a GraphSnapshot held
  in memory, no store needed. `sldb.api.graph` also exports `Edge` and `SystemIdentity`.
- `models inherit` and the `stores check` note tell a copy by its class, not by the reference
  string: `deskops.models.atom:AtomDoc` is a copy of `deskops.models:AtomDoc` when the package
  re-exports it. A converted copy takes the owner's `model_ref`.
- `edges check` over linked stores: one edge that two stores both emit (a shared model's
  `has_field`) counts once for cardinality; `has_model` is many-to-many, since stores share a
  model they inherit; `links_to` is a builtin relation type. `sldb edges init` now also
  rewrites a tracked builtin relation type whose spec moved (`updated` in its report), and no
  longer writes a builtin over an authored relation type of the same name.
- Models are defined once, in the store that owns them, and inherited by the others.
  `sldb models inherit alias:Model` / `sldb.api.inherit_model` registers an inherited entry
  (`origin: <alias>`, no source path) or converts a local copy in place, keeping its documents,
  roster and signed contract. Using `alias:Model` as a model name now inherits instead of
  copying. An inherited model imports from the owner's project root, so no `--pythonpath` is
  needed and a moved owner is one link to update; with the owner unreachable the store keeps
  working on its own signature. `stores check` notes a local model under a name a linked store
  owns (a convertible copy, or an override to rename). The graph gains `links_to` between
  stores and `origin_store` on `has_model`. A store with no inherited models writes no
  `origin` key, so existing indexes do not change.
- `stores update` re-signs the roster of a model whose class does not import. It used to skip
  the model whole, so a stale roster (a merge that brought its shards in, say) stayed
  `roster stale` in `stores check`. Its documents are still not rehashed, it is still reported
  as skipped, and it keeps the contract it signed.
- `stores check` no longer reports a moved contract for a model with `extra="allow"` (deskops'
  TaskDoc) whose documents carry undeclared frontmatter keys. Such a key is still produced by
  the current class, so it is not a field the model dropped; the check only counts a key the
  current extraction of the same document no longer yields. `stores update` could never clear
  the old finding.
- A template whose frontmatter is one `dict` placeholder (`⸢rev,dict•frontmatter⸥`) declares
  every key: `docs track` and `docs create` no longer refuse a document's extra keys, which that
  dict carries back on re-render.
- `producer.version` in a semantic export is the real package version: read from the source
  checkout's `pyproject.toml`, else from the installed `structuredLanguageDB` metadata. It
  asked for a distribution named `sldb`, which never exists, and always fell back to `0.1.0`.
- `click` is an optional extra (`pip install structuredLanguageDB[click]`), imported only when
  `ClickScanner` is used; it was imported unconditionally without being declared.
- `sldb.examples.pandoc_cv` ships in the wheel, with its Markdown files.
- `tools/check_identity.py` reads `git ls-files -z`: a quoted non-ASCII path no longer shows
  up as a top-level entry named `"docs`.

## 0.1.10 - 2026-10-17 — references to a relation type reach it; a document by absolute path

- A `__references__` field that points at `RelationTypeDoc:<doc>` now lands on the
  `sldb://relation_type/<name>` node. The index stores relation types under that node, so the
  schema edge used to point at a document node that does not exist and was dropped silently
  while `doc_exists` said yes. `resolve_edges` moves that end to the relation-type node.
- `find_doc` (behind untrack and delete) accepts a document's absolute path as well as the path
  relative to the project root.
- Design notes for the surface in `docs/surface/`, with tests for the MachineDoc editor and an
  optimistic-lock client. The editor test compiles on Python 3.10/3.11 (no nested PEP 701
  f-string).

## 0.1.9 - 2026-10-16 — a dropped field is a contract move, and `stores update` fixes it

- A document whose `field_hashes` name a field its model no longer declares was signed under
  another contract. Any write of another document of the model re-stamps the model's contract,
  so the model looked unmoved: `stores check` blamed the untouched document (`data_mutation`,
  "confirm the change was intended") and `stores update` trusted its unchanged text and never
  re-extracted it, so the check stayed red. Now the model reads as `contract moved` (safe to
  run: `stores update`) and `stores update` re-extracts those documents.

## 0.1.8 - 2026-10-16 — a deleted model class no longer locks the store

- Derived-index rebuilds skip a model whose class does not import instead of raising; the
  semantic rebuild names it in `models_unresolved`, as the edge rebuild already did, and its
  documents keep their last tags. `untrack_document` (and every write that rebuilds) works
  while another registered model's class is gone.
- `sldb models remove <name> --with-documents` / `remove_model(..., untrack_documents=True)`:
  drops a model and its tracked documents without importing the class; the Markdown files stay.
- A write that raises halfway leaves no trace: `untrack_document` puts the document's shard,
  the models index and the store index back as they were; `remove_model` changes the registry
  first and deletes the model's files only once every rebuild succeeded.

## 0.1.7 - 2026-10-16 — `models remove`

- `sldb models remove <name>` / `sldb.api.remove_model(store, name)`: unregisters a model that
  tracks no documents, with its indexes and shards; the class is never imported, so a model
  whose code was deleted can go. A model that still tracks documents is refused (untrack them
  first). `stores check` already passes with such a model registered (0.1.5); its note now
  names the unimportable models with no documents as removable.

## 0.1.6 - 2026-10-16 — the graph as a state machine

- `--where` joins predicates with ` and ` (outside literals; no `or`, no parentheses), and
  `nonempty(f)` is `has(f)` that also rejects `[]` and `{}` (`has` keeps its meaning).
- `sldb.api.where_matches(expression, payload, subject=None)`: a `--where` predicate on a plain
  payload, tracked or not; `{field}` fills from `subject` (default: the payload). An unparseable
  part raises `WherePredicateError`, now exported from `sldb.api`.
- `sldb.api.edges_holding(store, node, subject, relation=None)`: the edges leaving a node whose
  condition (the edge's, else its type's) holds on the subject; `sldb edges show <node>
  --holds-for <doc>` is the same from the CLI. A self-loop is a valid edge (a terminal
  transition).

## 0.1.5 - 2026-10-16 — an unimportable model is named, not blamed on its documents

- `stores check`: when a model's class cannot be imported (a clean clone without the model's
  package, a consumer's CI with another `sldb` first on PATH), its fields cannot be
  re-extracted. Every document used to read as a `data_mutation` ("decide first", restore the
  file). Intact text now stands for intact fields, and the report names the unresolved models;
  changed text still fails. JSON: `models[].resolved`.
- CI: the structural gates pass (`legacy_contract` mapped to the `migracion` axis, unit coupling
  updated; the surface gate no longer compares the five-consumer total with a partial view),
  and `selfdoc check` passes (knowledge/ synced with the CLI, the store committed with it).

## 0.1.4 - 2026-10-16 — `fields update` leaves the store passing

- A field write (`fields update|append`, `sldb.api.save_document_payload`) rewrote the Markdown
  and the model's roster but not the document's record, so `stores check` failed with a
  `data_mutation` on the write sldb had just made. The shard cache handed out its own instance:
  the caller edited it in place and the save, comparing against the cache, saw no change and
  skipped the write. Loads now return a copy (`sldb.store.io.shards`), which also covers the
  semantic, sections and edges shards.

## 0.1.3 - 2026-10-16 — upgrading sldb no longer fails unchanged stores

Found on Governance's `pulse`, which installs sldb from git: both checks failed on a store whose
content had not changed.

- `stores check`: a model whose stored contract hash equals the formula sldb used before
  cecd97b (fields and template only) passes, with a note naming those models, instead of
  "contract moved" on every model. A class that really changed still fails. `stores update`
  re-seals the hash under the current formula. JSON: `models[].legacy_contract`.
- `edges check`: in a store that ran `edges init`, an edge sldb derives itself whose builtin
  type was added later (`composes`) is checked against the definition sldb ships and reported in
  `untracked_builtins`, not as an error. A store that never ran `edges init` still fails;
  authored edges still need a tracked type.

## 0.1.2 - 2026-10-16 — referencing documents of linked stores

- `stores add` links were recorded but no document lookup read them: `docs show
  alias:doc` answered `Unknown document target`. `docs show` (and `sections show|fields`,
  serve's document routes) now take `alias:ref` — name, `Model/name` or tracked path — and
  read only the store linked directly as `alias`. A bare ref still reads only the local store;
  a prefix that names no link leaves the ref whole, so existing refs resolve as before.
- Add `docs exists <[alias:]ref>` and `sldb.api.doc_status|doc_exists`: whether a reference
  resolves, from the indexes alone (no model import, nothing written). Exit 0 ok, 1 missing,
  2 ambiguous, 5 `link-missing` / `link-broken`, so a missing document is told apart from a
  sibling repo that is not there.
- `stores list` (and `sldb.api.store_links`) report each link's state: `ok`, `missing` or
  `not-a-store`; a broken link is reported, never raised.
- `stores add` records the link relative to the project root (it was absolute outside it), and
  refuses linking a store to itself, aliases outside `[A-Za-z0-9][A-Za-z0-9._-]*` and the
  reserved `local`. Links already written are read as before.
- `stores init` seals the root hash over the empty model layer: a new store, or one that
  only links others, passes `stores check` without a `stores update`.
- `docs show` of a linked doc reads its file from the linked project (`absolute_path` was
  built from the local root).

## 2026-10-01 — SLDB is the substrate again

- The README no longer calls this generation frozen: the v2 seed (`knowledge`) was frozen in
  turn and its evaluator moved to `pron`, so nothing supersedes this package. SLDB is the
  store every surface (`surface/`, `tools/graph_ui`, `tools/sldb-ui`) is a view over. <!-- gone -->
- New README section "Serving and surfaces": `sldb serve` routes grouped by what a UI needs,
  and where the surfaces and their design docs live.

## 2026-09-07 — v1 frozen

- The README marks this generation frozen, with `knowledge` as its successor. Earlier modularization and v0.6 removal plans are historical and do not promise further v1 releases.

## Working tree — `docs delete`

- Add `docs delete` (and `sldb.api.delete_document`): untrack a document **and** remove
  its Markdown file. `docs untrack` was the only way to drop a document, and it keeps
  the file on purpose — so "delete this document" meant untrack, then `rm` by hand, then
  remember that `runtime/cache/extracted.json` still describes the deleted path until
  some later full load rewrites it. `delete` does the three.
- Confirms before removing the file unless `--yes` is given; a non-interactive stdin
  answers no.
- Add `runtime_cache_disk.forget(store, predicate)` so cache entries can be dropped
  without a full store load.

## Working tree — self-documentation follow-up

- Add `selfdoc scan|sync|check` to derive CLI facts from argparse, preserve authored explanations, and synchronize tracked command/surface documents from the selected store root.
- Report obsolete documents without deleting them; check freshness without writing documents or indexes.
- Expose public parser help for the supported `init` and `example` commands.
- Split knowledge document definitions into one class per file, keeping public import references and resolving re-exported definitions for template editing.
- Separate follow-up work into self-documentation, store context/federation, and AST ownership/section contracts. No package version bump or publication is included.

## Historical pending changes

- Add reversible `rev,table[...]` template markers for rendering and extracting Markdown tables backed by `list[dict]` fields.
- Add generic cross-store document writes through linked store aliases and federated model namespaces for workflow tools such as `deskops`.

## 0.2.0 - 2026-05-16

- **Store write concurrency**: atomic writes + advisory `fcntl` locks on all index write paths; `--wait` flag for `stores update`
- **Rebuild auditability**: `RebuildReport` dataclass tracks missing docs, empty sections, and unparseable headings in both semantic and section rebuilds; `--verbose` flag for details
- **CLI deprecation surface**: old singular commands (`store`, `model`, `doc`, `ls`, `get`, etc.) emit deprecation warnings; v0.6 was the historical removal target (see freeze note above).
- **Read-side hot path**: `sections show` and `sections fields` prefer persisted index over full IR rebuild; `--rebuild` flag available on `find`/`sections find`
- **Marker ownership robustness**: field name from the canonical `parse_marker()` is validated against known payload paths; unknown markers log a warning

## 0.1.2 - 2026-04-24

- Reorganize the package into `core`, `models`, `runtime`, `cli`, `assets`, and `examples` subpackages while keeping compatibility re-exports
- Add explicit link recovery and transclusion composition with `recover` and `compose`
- Add structural store queries under `st` with `ls`, `get`, `glob`, and `find --where`
- Add store-local semantic indexing under `se` and explicit federated semantic navigation under `gse`
- Add model semantic metadata, canonical model registration, semantic equivalence mapping, and bundled tests for the new workflows

## 0.1.1 - 2026-04-24

- Add current-system architecture docs and diagrams under `docs/architecture/`
- Add feature proposal docs under `desk/` for future SLDB features: link/recover/compose, store tree indexing, semantic DAG indexing, canonical/global-local semantics
- Add desk workspace with task board, self-docs, and operating procedures

## 0.1.0 - 2026-04-21

- Rename the package and CLI from `nldb` to `sldb`
- Add safe-by-default Python marker execution with configurable unsafe mode
- Ship the SLDB example bundle and CLI workflows for extract, render, validate, init, and example
- Add release basics: MIT license, package metadata, and CI

FILE:instruccion
Cold-bundle de la tarea task-gd23: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_select_documents.py
- TMPDIR=/dev/shm pytest -q tests/store/test_queries_expanded.py
- TMPDIR=/dev/shm pytest -q tests/test_linked_structural.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/ sin nombres nuevos contra el commit base 6b80df36 (salida de ambos en esta sección)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- sldb docs select --prefix P --one --format json sobre el store temporal del test
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, límite de clases por archivo; cuenta como test de los archivos tocados aunque output_scope no lo nombre)
- git fetch y rebase sobre origin/main antes de integrar (main trae SV01, SV02, SV04 en 6ba8bb20 y GO04 en d7eefdeb); en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio

