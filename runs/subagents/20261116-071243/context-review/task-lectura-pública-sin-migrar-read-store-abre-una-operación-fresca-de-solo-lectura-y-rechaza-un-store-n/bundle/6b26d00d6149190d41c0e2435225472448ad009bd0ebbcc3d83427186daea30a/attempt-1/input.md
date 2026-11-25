FILE:desk/tasks/task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n.md
---
sldb:
  by: agent
  at: '2026-11-16T05:32:46Z'
  authority: generated
  via: save_document_payload
id: task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261102-051843-unclear-falta-lectura-publica-de-store-preparado-sin-open-store-ni-migracion.md
- desk/inbox/20261102-081659-unclear-falta-forma-publica-de-abrir-operacion-de-lectura-sin-open-store.md
- desk/inbox/20261102-141033-unclear-adenda-al-intake-081659-open-store-readonly-sirve-para-ws13-2-sin-ser-api-universal-de-lectura.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/read_store.py
- src/sldb/api/documents/extract_payload.py
- src/sldb/api/__init__.py
- src/sldb/store/migration.py
- tests/api/test_api_stores.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice
---

# Lectura pública sin migrar: read_store abre una operación fresca de solo lectura y rechaza un store no preparado; extract_payload extrae de texto ya leído

## Rationale

_Explain why this task exists or the business driver behind it._

El lector de graph_ui (WS13.1/WS13.2, contrato WS11 §5.4) tiene que leer un store sin migrarlo ni reconstruirlo como efecto de un GET, ver altas y bajas hechas por otro proceso, y rechazar de forma observable un store no preparado. Hoy la única puerta pública es sldb.api.open_store, que llama migrate_store_layout si el store existe (src/sldb/api/stores/open_store.py:37-38) aun con mode="readonly" (ese modo solo controla el fallback al store global). La comprobación de layout canónico es privada (_already_canonical, src/sldb/store/migration.py:63), y graph_ui llama new_operation de sldb.store.runtime_cache_signature y sldb.store.documents_hash, fuera de sldb.api. Además extract_model_data solo está en sldb.runtime.validation (línea 65). Tres notas del inbox piden esto.

## Goal

_Describe the concrete result this task must produce._

sldb.api exporta read_store(store) -> StoreLocation, store_is_prepared(store) -> bool y extract_payload(model, markdown) -> dict; read_store nunca escribe en disco, empieza una operación nueva (ve cambios de otros procesos) y lanza SLDBStoreError con el texto "store not prepared: run `sldb stores update`" si el layout no es canónico.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) src/sldb/api/stores/read_store.py nuevo con read_store(store: str | Path | None = None) que resuelve el store igual que open_store (_resolve_store_arg o _find_default_store("readonly")), NO llama migrate_store_layout, llama store_is_prepared y, si es False, lanza SLDBStoreError con el texto de Goal; si es True llama add_owner_import_roots, new_operation y new_documents_hash_operation y devuelve StoreLocation. (2) store_is_prepared(store) en el mismo módulo: True si store_exists y _already_canonical (se mueve o reexporta desde src/sldb/store/migration.py sin cambiar su lógica). (3) extract_payload(model, markdown) en src/sldb/api/documents/extract_payload.py que llama sldb.runtime.validation.extract_model_data. (4) Export de los tres en sldb.api (__init__ y __all__). (5) Tests: tests/api/test_api_stores.py con un audit hook o comparación de mtimes que prueba cero escrituras al leer un store canónico; un store con layout viejo (fixture de tests/store/test_legacy_layout_migration.py) da SLDBStoreError y queda sin migrar; un documento agregado por otro open_store después del primer read_store aparece en un segundo read_store; extract_payload devuelve lo mismo que extract_model_data. CHANGELOG.md y una línea en docs/architecture/ sobre la diferencia open_store/read_store. No entra: cambiar open_store ni el significado de mode="readonly"; cambiar graph_ui (se le avisa por mensaje al cerrar); servir esto por sldb serve.

Precisiones (preflight-1): Validation tiene cuatro comandos (tres pytest y tools/check.sh --fast). read_store resuelve exactamente como open_store: si store es truthy, _resolve_store_arg(str(store)); si no, _find_default_store("readonly"); después project_root(store_path). store_is_prepared(store) devuelve False si no existe el store (store_exists) o su store_index.yaml (store_index_path), y si no, el valor de _already_canonical(load_store_index(store_path), store_path, project_root(store_path)); _already_canonical se queda en migration.py y se importa desde ahí (no se mueve). Orden en read_store: resolver, comprobar preparado (o lanzar), add_owner_import_roots, new_operation, new_documents_hash_operation, devolver StoreLocation(store_path=..., project_root=...). extract_payload(model_type: type, markdown: str) -> dict[str, Any] devuelve extract_model_data(model_type, markdown). "Cero escrituras": en el test, el conjunto (ruta, mtime_ns, tamaño) de todos los archivos bajo el proyecto de prueba es igual antes y después de read_store. Los tests nuevos van en tests/api/test_api_stores.py; el store de layout viejo se arma copiando lo que hace la fixture de tests/store/test_legacy_layout_migration.py. La línea de doc va en docs/architecture/store-declaration.md.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/stores/open_store.py, src/sldb/store/migration.py (líneas 49-75), src/sldb/api/__init__.py y la fixture de layout viejo en tests/store/test_legacy_layout_migration.py. 2) Implementar read_store.py y extract_payload.py. 3) Exportar. 4) Tests. 5) tools/check.sh --fast (capas). 6) Al cerrar, deskops message send --to graph_ui avisando los nombres nuevos.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm pytest -q tests/store/test_legacy_layout_migration.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los cuatro comandos de Validation pasan; `python -c "from sldb.api import read_store, store_is_prepared, extract_payload"` funciona; el test de cero escrituras y el de store no preparado pasan; CHANGELOG, doc y commit; mensaje enviado a graph_ui.

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

FILE:desk/atoms/atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice.md
---
id: atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice
title: Un consumidor pregunta al store por la API, no leyendo sus archivos de índice
five_wh_one_plus: how_not
tags:
- system:sldb
---

# Un consumidor pregunta al store por la API, no leyendo sus archivos de índice

## Answer

No parsear .sldb/core/store_index.yaml desde otro repo para saber qué modelos hay: su forma es interna y cambia (origin, family). sldb.api.registered_models e is_model_registered (nombre, module:Class o module.Class) y sldb models check son la superficie estable.

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
from sldb.api.edges.referrer import Referrer
from sldb.api.edges.referrers import referrers
from sldb.api.edges.rewrite_references import rewrite_references
from sldb.api.edges.rewrite_report import RewriteReport
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
from sldb.api.views import list_views, run_view
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
from sldb.api.tags import tag_check, tag_evaluations, tag_folder, tag_namespaces, tag_tree
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
    "Referrer", "RewriteReport", "referrers", "rewrite_references",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
    "list_views", "run_view",
    "TagNamespace", "add_semantic_equivalence", "add_semantic_parent", "remove_semantic_parent", "semantic_tag",
    "replace_text", "tag_check", "tag_evaluations", "tag_folder", "tag_namespaces", "tag_tree",
]

FILE:src/sldb/store/migration.py
from __future__ import annotations

from pathlib import Path

from sldb.store.io import (
    load_documents_index,
    load_models_index,
    load_sections_index,
    load_semantic_dag,
    load_semantic_index,
    load_store_index,
    save_documents_index,
    save_models_index,
    save_sections_index,
    save_semantic_dag,
    save_semantic_index,
    save_store_index,
)
from sldb.store.migration_legacy_layout import relocate_legacy_layout
from sldb.store.layout import (
    documents_index_relpath,
    models_index_relpath,
    sections_index_relpath,
    semantic_index_path,
    store_index_path,
)


def _migrate_model(m_entry, store_path: Path, p_root) -> bool:
    m_idx = load_models_index(p_root / m_entry.models_index)
    rels = (models_index_relpath(store_path, m_entry.name), documents_index_relpath(store_path, m_entry.name), sections_index_relpath(store_path, m_entry.name))
    changed = m_idx.documents_index != rels[1] or m_entry.models_index != rels[0]
    _migrate_model_indexes(m_idx, p_root, rels)
    save_models_index(p_root / rels[0], m_idx)
    m_entry.models_index = rels[0]
    return changed


def _migrate_model_indexes(m_idx, p_root, rels: tuple[str, str, str]) -> None:
    n_m_rel, n_d_rel, n_s_rel = rels
    documents = load_documents_index(p_root / m_idx.documents_index)
    save_documents_index(p_root / n_d_rel, documents)
    if m_idx.sections_index:
        save_sections_index(p_root / n_s_rel, load_sections_index(p_root / m_idx.sections_index))
    m_idx.documents_index, m_idx.sections_index = n_d_rel, n_s_rel if m_idx.sections_index else ""
    m_idx.documents_count = len(documents.documents)


def _model_canonical(m_entry, store_path: Path, p_root: Path) -> bool:
    """PLAN 15 capa 5/7: a model's sections and documents are canonical once their old single
    per-model files are gone (sharded into `<store>/{runtime/sections,core/documents}/<model>/`,
    or a section-less model that never had one)."""
    if m_entry.models_index != models_index_relpath(store_path, m_entry.name) or not (p_root / m_entry.models_index).exists():
        return False
    m_idx = load_models_index(p_root / m_entry.models_index)
    if m_idx.documents_index != documents_index_relpath(store_path, m_entry.name) or (p_root / m_idx.documents_index).exists():
        return False
    if m_idx.sections_index and m_idx.sections_index != sections_index_relpath(store_path, m_entry.name):
        return False
    return not m_idx.sections_index or not (p_root / m_idx.sections_index).exists()


def _already_canonical(store_index, store_path: Path, p_root: Path) -> bool:
    """True when every model index already sits at its canonical path, points at canonical
    document and section indexes (capa 5: sections already sharded, the old file gone), and
    the old store-wide semantic index file is gone too (capa 5: sharded): nothing to migrate."""
    if semantic_index_path(store_path).exists():
        return False
    return all(_model_canonical(m_entry, store_path, p_root) for m_entry in store_index.models)


def migrate_store_layout(store_path: Path, project_root: Path) -> bool:
    changed = relocate_legacy_layout(store_path, project_root)
    store_index = load_store_index(store_path)
    if store_index_path(store_path).exists() and _already_canonical(store_index, store_path, project_root):
        return changed   # the common case: an up-to-date store is not rewritten on every context
    changed = _migrate_models(store_index, store_path, project_root) or changed
    _migrate_derived_indexes(store_path)
    if changed: save_store_index(store_path, store_index)
    return changed


def _migrate_models(store_index, store_path: Path, project_root: Path) -> bool:
    """Every model's indexes to their canonical sharded paths; True when any of them moved."""
    changed = not store_index_path(store_path).exists()
    for m_entry in store_index.models:
        if _migrate_model(m_entry, store_path, project_root): changed = True
    return changed


def _migrate_derived_indexes(store_path: Path) -> None:
    """Rewrite the semantic index and DAG from their old single files into their shards."""
    save_semantic_dag(store_path, load_semantic_dag(store_path))
    save_semantic_index(store_path, load_semantic_index(store_path))

FILE:tests/api/test_api_stores.py
"""`sldb.api` store operations: open, link, refresh indexes; and the `sldb.cli` bridges over them."""

from __future__ import annotations

import pytest

from sldb.api import link_store, open_store, update_store_indexes
from sldb.cli import main as cli_main
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index


def test_open_store_resolves_store_and_project_root(api_store):
    location = open_store(str(api_store.store))
    assert location.store_path == api_store.store.resolve()
    assert location.project_root == api_store.root.resolve()
    assert get_store_context(str(api_store.store)) == (location.store_path, location.project_root)


def test_open_store_without_store_outside_any_project_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    with pytest.raises(SLDBStoreError, match="init --path"):
        open_store(None)


def test_link_store_records_link_and_refuses_duplicates(api_store, tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    assert cli_main(["stores", "init", "--path", str(other)]) == 0
    linked = link_store(api_store.store, other / ".sldb", "shared")
    assert (linked.name, linked.path) == ("shared", "../other/.sldb")
    assert [s.name for s in load_store_index(api_store.store).stores] == ["shared"]
    with pytest.raises(SLDBStoreError, match="already linked"):
        link_store(api_store.store, other / ".sldb", "shared")


def test_link_store_refuses_a_directory_without_store(api_store, tmp_path):
    with pytest.raises(SLDBStoreError, match="No store at"):
        link_store(api_store.store, tmp_path / "nowhere" / ".sldb", "ghost")


def test_update_store_indexes_reports_a_complete_refresh(api_store):
    report = update_store_indexes(api_store.store, api_store.pythonpath)
    assert report.complete
    assert report.store_path == api_store.store.resolve()
    assert report.semantic_index.docs_processed >= 0


def test_update_store_indexes_skips_a_missing_document(api_store):
    (api_store.root / "login.md").unlink()
    report = update_store_indexes(api_store.store, api_store.pythonpath)
    assert report.skipped_documents == ["login"]
    assert not report.complete
    assert cli_main(["stores", "update", "--store", str(api_store.store), "--pythonpath", api_store.pythonpath]) == 1


def test_scaffold_store_and_build_store_are_public_and_bridged_by_the_cli(api_store, capsys):
    """GD26: the scaffold of folders and seeds is an `sldb.api` function and a `stores` subcommand."""
    from sldb.api import ScaffoldReport, Seed, StoreDeclaration, build_store, scaffold_store
    from sldb.api.stores.declare_store import declare_store
    from sldb.api.stores.store_declaration import save_declaration

    save_declaration(api_store.store, declare_store(api_store.store, api_store.root))
    declaration = StoreDeclaration(folders=["inbox"], seeds=[Seed(path="inbox/.keep", text="")])
    report = scaffold_store(api_store.store, declaration=declaration, apply=True)
    assert isinstance(report, ScaffoldReport) and report.created == ["inbox", "inbox/.keep"]
    assert build_store(api_store.store)["scaffold"] == {"created": [], "rewritten": [], "present": [], "conflicts": []}
    assert cli_main(["stores", "scaffold", "--store", str(api_store.store), "--format", "json"]) == 0
    assert "created" in capsys.readouterr().out

FILE:instruccion
Cold-bundle de la tarea task-lectura-pública-sin-migrar-read-store-abre-una-operación-fresca-de-solo-lectura-y-rechaza-un-store-n: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm pytest -q tests/store/test_legacy_layout_migration.py
- bash tools/check.sh --fast

