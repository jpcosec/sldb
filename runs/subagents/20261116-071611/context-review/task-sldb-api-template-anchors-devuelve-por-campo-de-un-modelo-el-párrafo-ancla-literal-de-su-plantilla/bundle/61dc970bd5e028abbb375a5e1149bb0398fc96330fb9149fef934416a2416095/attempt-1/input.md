FILE:desk/tasks/task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla.md
---
sldb:
  by: agent
  at: '2026-11-16T05:53:59Z'
  authority: generated
  via: save_document_payload
id: task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-h1-de-placeholder-deskops-api-pública-para-leer-los-párrafos-ancla-literales-de-la-plantilla-de-un-m.md
depends_on: []
pills: []
files:
- src/sldb/api/model_registry/template_anchors.py
- src/sldb/api/__init__.py
- src/sldb/core/template_extractor.py
- tests/test_literal_paragraph_anchor.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-template-de-un-modelo-es-estable-sus-recetas-se-calculan-una-vez-no-en-cada-extract
---

# sldb.api.template_anchors devuelve, por campo de un modelo, el párrafo ancla literal de su plantilla

## Rationale

_Explain why this task exists or the business driver behind it._

deskops (task.debug "edit no guarda el párrafo placeholder de la plantilla como contenido") necesita saber qué párrafo literal ancla cada campo (como "_Outline the expected implementation route or affected surface._" antes de implementation_path) para no guardarlo como valor. Hoy lo saca con internos de sldb: AST_Handler().split_nodes sobre model.__template__ y TemplateExtractor().extract_nodes (src/sldb/core/template_extractor.py), recorriendo las recetas (outer_type paragraph, anchor, props). 9dcabd9a arregló un caso vecino (tests/test_literal_paragraph_anchor.py) pero no hay API pública. Se elige la opción (a) de la nota, API de lectura, porque es aditiva; la opción (b), descartar en render/save un valor igual a su ancla, cambia el contrato de escritura y no se hace aquí. Origen: desk/inbox/inbox-note-h1-de-placeholder-deskops-api-pública-para-leer-los-párrafos-ancla-literales-de-la-plantilla-de-un-m.md.

## Goal

_Describe the concrete result this task must produce._

sldb.api.template_anchors(model_type) -> dict[str, str] devuelve, para cada campo cuyo marcador en __template__ va precedido por un párrafo literal que ancla su extracción, el texto exacto de ese párrafo tal como render lo escribe y extract lo consume; los campos sin párrafo ancla no aparecen.

## Scope

_State what is in scope and what is out of scope._

Entra: módulo nuevo src/sldb/api/model_registry/template_anchors.py que usa las mismas recetas que el extractor (TemplateExtractor y el split de nodos), sin reimplementar el parseo; export en sldb.api. Tests en tests/test_literal_paragraph_anchor.py: para un modelo de prueba con dos campos anclados por párrafos en cursiva y uno sin ancla, el dict tiene exactamente las dos claves con el texto literal; para TaskDoc de deskops no se prueba (es otro repo). CHANGELOG.md. No entra: la opción (b), cambiar render o extract, ni tocar deskops (aviso al cerrar).

Precisiones (preflight-1): el párrafo ancla de un campo es el párrafo literal (texto sin marcadores) inmediatamente anterior al marcador del campo dentro de la misma sección del __template__, que es el que la receta del extractor registra como anchor del campo (outer_type paragraph). El valor devuelto es el texto del párrafo tal como aparece en __template__, con sus delimitadores de cursiva (por ejemplo "_Outline the expected implementation route or affected surface._"), sin espacios al final. template_anchors recibe la clase del modelo (type[StructuredNLDoc]); con cualquier otra cosa lanza TypeError. Vive en src/sldb/api/model_registry/template_anchors.py y sldb.api lo reexporta en __init__ y __all__. Las recetas se obtienen como las obtiene el extractor: leer src/sldb/core/template_extractor.py y usar la misma llamada que hace Validator(model).extract para calcular recetas (sin reparsear la plantilla con código propio).

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/core/template_extractor.py, src/sldb/runtime/validation.py (65-68) y tests/test_literal_paragraph_anchor.py. 2) Ubicar en las recetas el anchor de tipo paragraph previo a cada campo. 3) Implementar y exportar. 4) Tests. 5) bash tools/check.sh --fast por las capas (api puede importar core).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_literal_paragraph_anchor.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

`from sldb.api import template_anchors` funciona; el test del modelo de prueba pasa; check.sh --fast pasa; CHANGELOG, commit y aviso a deskops con deskops message send --to deskops.

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

FILE:desk/atoms/atom-el-template-de-un-modelo-es-estable-sus-recetas-se-calculan-una-vez-no-en-cada-extract.md
---
id: atom-el-template-de-un-modelo-es-estable-sus-recetas-se-calculan-una-vez-no-en-cada-extract
title: 'El template de un modelo es estable: sus recetas se calculan una vez, no en
  cada extract'
five_wh_one_plus: how
tags:
- system:sldb
- topic:performance
- topic:parsing
provenance: src/sldb/runtime/validation.py
---

# El template de un modelo es estable: sus recetas se calculan una vez, no en cada extract

## Answer

Las recetas de extracción de sldb dependen solo del string __template__ del modelo, no del documento: se memoizan por template (runtime/validation.py:_recipes, lru_cache). Rehacerlas en cada extract y validate era el mayor costo evitable del pipeline (~35% de la extracción en el store de sldb). Lo mismo vale para el parser markdown-it de las secciones (store/section_rebuild.py, uno por proceso); AST_Handler todavía crea un MarkdownIt por instancia. Lo que sí depende del documento (su AST) se parsea una vez por texto.

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

FILE:src/sldb/core/template_extractor.py
import re
from typing import Any
from sldb.core.exceptions import SLDBASTError
from sldb.core.node import SLDBNode
from sldb.core.node_handler import SharedNodeHandler

class TemplateExtractor:
    """Extracts deterministic search recipes from template block nodes."""

    def __init__(self):
        self.node_handler = SharedNodeHandler()

    def extract_nodes(self, block_nodes: list[SLDBNode]) -> list[dict[str, Any]]:
        extracted_recipes = []
        for outer_index, block_node in enumerate(block_nodes):
            state = {"found": False, "recipes": extracted_recipes, "idx": outer_index, "node": block_node}
            self._dive(block_node, [], state)
            if not state["found"]: self._add_anchor_recipe(state)
        self._validate_invariants(extracted_recipes)
        return extracted_recipes

    def _dive(self, node: SLDBNode, current_path: list[int], state: dict[str, Any]) -> None:
        handler_key = self.node_handler.get_handler_for_node(node)
        if handler_key and handler_key != "text" and self._process_non_text_handler(node, current_path, state, handler_key): return
        if (handler_key == "text" or not node.children) and self._process_text_handler(node, current_path, state): return
        for child_idx, child in enumerate(node.children):
            self._dive(child, current_path + [child_idx], state)

    def _process_non_text_handler(self, node: SLDBNode, current_path: list[int], state: dict[str, Any], handler_key: str) -> bool:
        handler_recipes = self.node_handler.handlers[handler_key].compile_recipe(node)
        if not handler_recipes: return False
        for recipe in handler_recipes:
            self._update_and_append_recipe(recipe, state, current_path)
            state["found"] = True
        return True

    def _process_text_handler(self, node: SLDBNode, current_path: list[int], state: dict[str, Any]) -> bool:
        literal_recipes = self.node_handler.handlers["text"].compile_recipe(node)
        if not literal_recipes: return False
        for recipe in literal_recipes:
            self._check_section_body(recipe, node, state)
            self._update_and_append_recipe(recipe, state, current_path)
            state["found"] = True
        return True

    def _check_section_body(self, recipe: dict[str, Any], node: SLDBNode, state: dict[str, Any]) -> None:
        """Lone data marker: paragraph → block range, heading → regex, else error.

        A lone marker owns its section body; block range is the only capture that
        keeps line breaks. Gating on `is_reversible` alone made `optrev` fall to
        the regex path and lose everything past the first line break, silently.
        """
        props = recipe.get("props_info", [])
        if not self._is_lone_data_marker(recipe, node, props):
            return
        if state["node"].type == "paragraph":
            recipe["capture_mode"] = "section_body"
        elif state["node"].type != "heading":
            self._reject_marker_block(props[0].name, state["node"].type)

    def _is_lone_data_marker(self, recipe: dict[str, Any], node: SLDBNode, props: list[Any]) -> bool:
        text = self.node_handler.handlers["text"].get_text(node).strip()
        return (len(props) == 1 and text.startswith("⸢") and text.endswith("⸥")
                and recipe.get("regex") == "^(.*?)$" and (props[0].is_reversible or props[0].is_optional))

    def _reject_marker_block(self, name: str, block_type: str) -> None:
        raise SLDBASTError(f"Field '{name}' is a lone marker in a '{block_type}' block; move it to its own paragraph.")

    def _update_and_append_recipe(self, recipe: dict[str, Any], state: dict[str, Any], current_path: list[int]) -> None:
        recipe.update({
            "outer_index": state["idx"],
            "outer_type": recipe.get("match_outer_type", state["node"].type),
            "outer_tag": recipe.get("match_outer_tag", state["node"].tag),
            "inner_path": current_path,
        })
        state["recipes"].append(recipe)

    def _add_anchor_recipe(self, state: dict[str, Any]) -> None:
        content = self.node_handler.handlers["text"].get_text(state["node"]).strip()
        state["recipes"].append({
            "outer_index": state["idx"], "outer_type": state["node"].type, "outer_tag": state["node"].tag,
            "inner_path": [], "props": [], "regex": f"^{re.escape(content)}$" if content else "^$",
            "handler": "text", "anchor": True,
        })

    def _validate_invariants(self, recipes: list[dict[str, Any]]) -> None:
        rev_counts = {}
        for recipe in recipes:
            for marker in self._extract_markers(recipe):
                if marker.is_reversible: rev_counts[marker.name] = rev_counts.get(marker.name, 0) + 1
        for name, count in rev_counts.items():
            if count > 1: raise SLDBASTError(f"Multiple canonical 'rev' markers found for field '{name}'.")

    def _extract_markers(self, recipe: dict[str, Any]) -> list[Any]:
        if "props_info" in recipe: return recipe["props_info"]
        if "marker" in recipe: return [recipe["marker"]]
        if "markers" in recipe: return [item["marker"] for item in recipe["markers"]]
        return []

FILE:tests/test_literal_paragraph_anchor.py
"""A template's literal paragraph anchors only a paragraph with that text.

deskops' InboxNoteDoc and TaskDoc templates carry a placeholder paragraph
(`_Describe the incoming message..._`). A document written without it had its first real
paragraph taken as the placeholder and dropped, so every rewrite of the document deleted it
(the first paragraph of several sldb inbox notes; `why`, `goal` and `done_when` of a task).
"""

from __future__ import annotations

import pytest
from pydantic import Field

from sldb import StructuredNLDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n_Describe the message._\n\n⸢rev,markdown•body⸥\n"
    title: str = Field(description="Title.")
    body: str = Field(description="Body.")


@pytest.mark.parametrize("md", [
    "# T\n\nFirst paragraph.\n\n## Scope\n\nmore\n",                       # without the placeholder
    "# T\n\n_Describe the message._\n\nFirst paragraph.\n\n## Scope\n\nmore\n",  # with it
])
def test_the_first_paragraph_is_the_bodys_with_or_without_the_placeholder(md):
    assert extract_model_data(Note, md)["body"] == "First paragraph.\n\n## Scope\n\nmore"


def test_a_rewrite_keeps_it():
    payload = extract_model_data(Note, "# T\n\nFirst paragraph.\n")
    again = extract_model_data(Note, render_model_markdown(Note, payload))
    assert again["body"] == "First paragraph."

FILE:instruccion
Cold-bundle de la tarea task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/test_literal_paragraph_anchor.py
- bash tools/check.sh --fast

