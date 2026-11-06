FILE:desk/tasks/task-go06-ruledoc-rules-check-y-rules-explain.md
---
id: task-go06-ruledoc-rules-check-y-rules-explain
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
- src/sldb/models/rule_doc.py
- src/sldb/models/__init__.py
- src/sldb/api/rules/__init__.py
- src/sldb/api/rules/rules_check.py
- src/sldb/api/rules/rules_explain.py
- src/sldb/api/rules/rule_subjects.py
- src/sldb/api/__init__.py
- src/sldb/cli/commands/rules.py
- src/sldb/cli/parsers/rules.py
- src/sldb/cli/parsers/__init__.py
- src/sldb/cli/dispatcher.py
- contracts/layers.toml
- docs/architecture/rules.md
- docs/opsys/bridge_primitives/README.md
- CHANGELOG.md
- tests/api/test_rules.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# GO06: RuleDoc, rules check y rules explain

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO06 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK03. sldb evalua reglas declaradas y los consumidores las autoran como documentos (G_BOUNDARY, atom-sldb-evaluates-declared-rules-consumers-author-them). GO05 (8be66bde) dejo el lenguaje de predicados y GraphBackend.eval completos; GO06 agrega el documento RuleDoc y los comandos que lo evaluan.

## Goal

_Describe the concrete result this task must produce._

Modelo RuleDoc (subject como expresion model <= X, where opcional, condition, severidad error|alert, momento on_write|on_transition|on_check, message opcional) validado al escribir; sldb rules check [--subject DOC] emite Finding de core con exit 1 solo ante error; sldb rules explain RULE SUBJECT devuelve el finding de eval con exits 0/1/2/3; docs/architecture/rules.md y CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

En alcance: el modelo RuleDoc, api/rules (check, explain, resolucion de sujetos y reglas), el comando sldb rules (check, explain) con su parser y su registro en el dispatcher, docs/architecture/rules.md, la marca de reemplazo en docs/opsys/bridge_primitives/README.md, CHANGELOG.md, tests. Fuera: evaluacion incremental y cableado on_write/on_transition (GO08), anclas doc: (GO07), transiciones como datos (GO09), retiro de shims (GO10).

PRINCIPIO DEL DUENO (2026-11-05): las invariantes de UN documento van como validadores pydantic del modelo; las invariantes entre documentos, como RuleDoc. Los tests solo prueban rechazo. Aplicado aqui: (q1) que condition y where parseen, que subject sea una expresion del lenguaje de la forma model <= X (o conjuncion que la contenga), y el vocabulario de severidad y momento (Literal) son validadores pydantic de RuleDoc (field_validator / Literal), de modo que construir o escribir una RuleDoc mal formada levanta el ValidationError del modelo con el campo y el motivo, por la via de escritura existente (sldb docs create/edit y la API). Que X resuelva a un modelo registrado depende del store, no del documento: se comprueba en la escritura (api) con el error existente de sldb para modelo desconocido, y no como validador del modelo. (q2) Los tests de RuleDoc mal formada prueban rechazo: un test por campo (condition, where, severidad, momento, sujeto) que espera el error; no hay tests que reafirmen que una RuleDoc valida se acepta mas alla de los que la aceptacion pide para check y explain.

HEREDADO: (h1) la familia de model <= X sale de base_models (GO05 p9, 8d7bee13). (h2) El finding de eval es el de rules-language.md seccion 4 (node, holds, clause, seen); la clave del envelope para rules explain la fija este nodo (H10 de rules-language). (h3) GO05 H6: los cambios de resultado del lenguaje nuevo frente a where_parse/FieldCondition ya estan en main; las reglas usan solo el lenguaje nuevo.

PRECISIONES (preflight de GO06, 2026-11-06):
p1 (envelope de rules explain): data = {"rule": "RuleDoc:<nombre>", "subject": "<Model:name>", "finding": {"node", "holds", "clause", "seen"}}, con el finding exactamente como lo devuelve GraphBackend.eval / eval_predicate (rules-language.md seccion 4; holds como "true", "false" o "incomplete"). La clave finding cierra H10 de rules-language.md para rules explain; el doc lo dice.
p2 (Finding.what): explicacion = "<clause> (seen: <seen en JSON compacto, claves ordenadas, ensure_ascii=False>)". Con message: what = message + " | " + explicacion. Sin message: what = explicacion.
p3 (exit 3): data = {"rule": "RuleDoc:<nombre>", "subject": "<Model:name>", "applies": false, "reason": "subject" | "where", "detail": "<texto>"}: reason subject cuando el documento no esta en la familia del sujeto (detail = la expresion subject de la regla); reason where cuando el where da false o incomplete (detail = la clause del where que decidio). Sin clave finding.
p4 (Finding.subject y document): subject = el Model:name del documento (con prefijo <store>: si viene de un store enlazado, como en GO05 H11); document = la ruta del documento relativa a la raiz del proyecto, como la guarda el registro.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO06 scope): Modelo RuleDoc: sujeto = familia de modelo (expresión model <= X, resuelta con la herencia de modelos ya existente en sldb: base_models del registro, la misma que usan source_types y target_types de RelationTypeDoc) más un campo where opcional (predicado en el lenguaje, evaluado sobre cada candidato antes de la condición; false o incomplete = la regla no aplica a ese documento); condición (campo condition); severidad (error | alert); momento (on_write | on_transition | on_check); message opcional (si existe, Finding.what = message seguido de la explicación de GO02; si no, solo la explicación). Validación al escribir una RuleDoc: condition y where parsean, severidad y momento están en su vocabulario, el sujeto resuelve a un modelo registrado; cualquier fallo rechaza la escritura con el error. Registro como cualquier documento. Comando sldb rules check [--subject DOC]: con --subject evalúa sobre ese documento todas las reglas cuyo sujeto lo incluye, de cualquier momento; sin --subject evalúa todas las reglas on_check sobre todos los documentos de su familia. Emite Finding (src/sldb/core/finding.py: level, code, subject, what, fix, document) por el canal existente: level = severidad de la regla, code = rules/<nombre de la RuleDoc>, subject = el documento, what = message seguido de la explicación de GO02 (o solo la explicación si no hay message), fix = "" (la regla no prescribe remedio), document = ruta del documento sujeto. El sujeto se guarda en el campo subject como string con la expresión del lenguaje (p. ej. "model <= TaskDoc"), validada al escribir como cualquier predicado. rules check convierte a Finding de core solo los resultados false e incomplete: false → level = severidad de la regla, code rules/<nombre>; incomplete → level alert, code rules/<nombre>/incomplete, sin importar la severidad. Exit 1 si hay al menos un Finding error, 0 en otro caso (los alerts nunca fallan). DOC en --subject y SUBJECT en explain aceptan Model:name o ruta; RULE acepta RuleDoc:<nombre>, <nombre> o ruta. Una referencia que no resuelve (documento o regla) es el error existente de documento desconocido de sldb, con su exit y mensaje. Una RuleDoc mal formada se rechaza con el error de validación existente al escribir documentos (el ValidationError del modelo en el envelope, con el campo y el motivo). sldb rules explain RULE SUBJECT imprime en el envelope el finding de eval tal como lo define GO02 (node, holds, clause, seen), también cuando holds es true; exit 0 si true, 1 si false, 2 si incomplete, 3 si la regla no aplica al sujeto (familia o where), con solo el motivo en el envelope y sin finding de eval; la severidad no afecta el exit. Hash de regla = content_hash del RuleDoc; GO08 lo incluye en la clave de su caché derivada. docs/opsys/bridge_primitives/README.md: la sección Constraint se marca como reemplazada por RuleDoc con enlace a rules.md. ACEPTACION: En un store temporal con modelos Base, X < Base, Y < X y Z < Base, una RuleDoc con sujeto model <= X aplica a X e Y y no a Z; rules check reporta error y alert como Finding con cláusula y nodo, con exit 1 solo ante error; rules check sin --subject recorre solo on_check; --subject acepta Model:name y ruta; rules explain devuelve el finding de eval y los exits 0/1/2, y exit 3 con una regla cuyo where excluye al documento; un resultado incomplete en rules check sale como alert rules/<nombre>/incomplete; una regla mal formada en condition, where, severidad, momento o sujeto es rechazada al escribirla con el error correspondiente; documentación en docs/architecture/rules.md; CHANGELOG. OUTPUT_SCOPE: src/sldb/models/rule_doc.py, src/sldb/api/rules/, src/sldb/cli/commands/rules.py, docs/architecture/rules.md, docs/opsys/bridge_primitives/README.md, CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla; regla 6: ante un contrato ausente registrar la hipotesis, no inventar API). Lenguaje: docs/architecture/rules-language.md; costura: docs/architecture/graph-backend.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest tests/api/test_rules.py sin fallos ni saltados
- store temporal Base, X < Base, Y < X, Z < Base: RuleDoc con sujeto model <= X aplica a X e Y y no a Z
- rules check: Finding error/alert con clausula y nodo; exit 1 solo ante error; sin --subject solo on_check; --subject por Model:name y por ruta; incomplete como alert rules/<nombre>/incomplete
- rules explain: finding de eval y exits 0/1/2; exit 3 con una regla cuyo where excluye al documento
- RuleDoc mal formada (condition, where, severidad, momento, sujeto) rechazada al escribir, un test de rechazo por campo
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO06 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.

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

FILE:src/sldb/models/__init__.py
from sldb.models.anchor_state import AnchorState
from sldb.models.code_anchor_doc import CodeAnchorDoc
from sldb.models.structured_doc import M, StructuredNLDoc
from sldb.models.notation_models import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
)

__all__ = [
    "M",
    "StructuredNLDoc",
    "CodeAnchorDoc",
    "AnchorState",
    "SpecDoc",
    "SpecNodeDoc",
    "NotationDoc",
    "GlyphDoc",
    "LinkDoc",
    "PaletteDoc",
    "ViewDoc",
]

FILE:src/sldb/api/__init__.py
"""sldb's library API: the store, model and document operations the CLI performs, as functions.

Consumers (pron, deskops, graph_ui...) call these instead of instantiating `sldb.cli` command
classes with fake argparse namespaces. Each operation that names a store opens it the way a
CLI command does (`open_store`), returns a pydantic model instead of printing, and raises
`sldb.core.exceptions` errors instead of exiting. Layering: `sldb.cli` -> `sldb.api` ->
`sldb.store` / `sldb.runtime` / `sldb.core`; nothing here imports `sldb.cli`.
"""

from __future__ import annotations

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
    "create_model", "anchor_node_id", "bare", "check_edges", "check_store",
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
    "WherePredicateError", "edges_holding", "remove_model", "where_matches", "inherit_model", "is_model_registered", "registered_models",
    "StructuredNLDoc", "UnresolvedReference", "unresolved_references",
    "GlyphDoc", "LinkDoc", "NotationDoc", "PaletteDoc", "SpecDoc", "SpecNodeDoc", "ViewDoc",
    "resolve_view", "resolve_documents", "evaluate_projection_view", "list_projection_views", "save_projection_view", "sync_notation", "sync_palette",
]

FILE:src/sldb/cli/parsers/__init__.py


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
        self.handlers.update({"edges": EdgesCLI().run, "anchors": AnchorsCLI().run, "graph": GraphCLI().run, "notations": NotationsCLI().run})

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

FILE:contracts/layers.toml
# Contrato de capas
#
# El orden de dependencia entre paquetes, declarado donde se puede leer sin abrir
# código. `tools/check_layers.py` lo verifica y rechaza lo que lo viole.
#
# Regla: un paquete puede importar de su propia capa o de cualquiera MÁS BAJA.
# Nunca hacia arriba. La capa 0 no importa nada del sistema, y por eso es la
# única que se puede extraer y usar sola.
#
# El orden no es una preferencia de estilo: es lo que decide si una pieza se
# puede probar aislada y si alguien puede entender una parte sin cargar el resto.

[[layers]]
level = 0
name = "núcleo"
packages = ["core", "models", "runtime", "code", "notations"]
rationale = """
Convierte texto en estructura y estructura en texto, junto con los tipos de
documento y la configuración que decide qué se permite al renderizar.

Los tres están en la misma capa porque están entrelazados: el renderizador
necesita el tipo base de documento, el tipo base necesita la extracción, y la
extracción necesita el renderizador. Separarlos en capas distintas produciría
tres ciclos en vez de describir el sistema.

Declararlos juntos no disuelve el problema: lo nombra. Mientras esta capa tenga
tres paquetes mutuamente dependientes, ninguno se puede extraer solo. Partirla
es trabajo futuro con diseño propio, no una excepción que se tacha.
"""

[[layers]]
level = 2
name = "persistencia"
packages = ["store", "links"]
rationale = """
Guarda, indexa y consulta. Conoce los contratos, no conoce la interfaz ni la
forma en que un humano pide las cosas.
"""

[[layers]]
level = 3
name = "operaciones"
packages = ["api"]
rationale = """
Las operaciones compuestas sobre el almacén: lo que un programa querría llamar.
Es la frontera pública para quien integra sin pasar por la línea de comandos.
"""

# La capa de transporte traduce entre un humano o un proceso y las operaciones.
# No debe contener lógica que un programa necesite: si algo ahí hace falta sin la
# terminal, va en la capa 3.

[[layers]]
level = 4
name = "transporte"
packages = ["cli", "selfdoc"]
rationale = """
`selfdoc` está acá y no más arriba porque la interfaz lo importa en 14 sitios: no
es un derivado del sistema, es parte de lo que el sistema expone. Clasificarlo
como derivado fue el primer error que esta puerta encontró en su propio contrato.
"""

[[layers]]
level = 5
name = "derivados"
packages = ["examples", "assets", "templates"]
rationale = """
Se derivan del sistema: ejemplos y plantillas. Pueden mirar todo porque nada
depende de ellos.
"""

# ---------------------------------------------------------------------------
# Excepciones vigentes
#
# Cada una es un import que viola el orden de arriba. Están acá para que la
# puerta pase hoy y la deuda quede contada, no escondida: mientras esta lista
# tenga entradas, el orden de capas es aspiracional, no bloqueable.
#
# Las cinco son la arista minoritaria de un ciclo. En cada caso la dirección
# mayoritaria tiene decenas o cientos de aristas y la culpable tiene una sola,
# así que el ciclo es un accidente reparable y no un diseño fusionado.
#
# Retirar una entrada de esta lista es el criterio de terminado de su reparación.
# ---------------------------------------------------------------------------

[allow]
upward = [
  ["selfdoc", "cli"],      # R5
]

# R2 (core→store) se reparó: `StoreError` bajó a `core/exceptions/store_error.py`
# y el almacén ahora la reexporta. Importar el núcleo pasó de 103 a 58 módulos.
# La entrada sale de esta lista porque la puerta avisa de excepciones vencidas:
# dejarla autorizaría algo que ya no ocurre.

# R1 (core→runtime) y R3 (models→runtime) ya no figuran acá: al poner los tres
# paquetes del núcleo en la misma capa dejaron de violar el orden. El ciclo
# sigue existiendo y está declarado arriba como lo que impide extraer el núcleo.
# Esto es la diferencia entre resolver y reclasificar, y conviene no confundirlas.

[[pending]]
id = "R1"
edge = "core → runtime"
at = "src/sldb/core/renderer_engine/python_expr.py#L5"
imports = "runtime.config.python_expression_is_allowed"
cycle_weight = "core→runtime: 1 arista · runtime→core: 4 aristas"
repair = """
El núcleo pregunta a la configuración si puede evaluar una expresión. Invertir:
que quien llama pase el permiso como argumento. El núcleo no debe consultar
estado global para decidir qué le está permitido.
"""

[[done]]
id = "R2"
edge = "core → store"
at = "src/sldb/core/exceptions/sldb_store_error.py#L2"
imports = "store.exceptions.StoreError"
cycle_weight = "core→store: 1 arista · store→core: 8 aristas"
repaired = """
Hecho. `StoreError` vive en `core/exceptions/store_error.py` y
`store/exceptions.py` la reexporta. Efecto medido: importar `core.renderer` pasó
de 103 a 58 módulos y de 149 ms a 131 ms, y `tools/check.sh` tiene una puerta que
rechaza la reaparición de la fuga.
"""

[[pending]]
id = "R3"
edge = "models → runtime"
at = "src/sldb/models/structured_doc.py#L67"
imports = "runtime.validation.extract_model_data"
cycle_weight = "models→runtime: 1 arista diferida · runtime→models: 1 arista"
repair = """
Escrito dentro de un método para esquivar el ciclo en tiempo de importación.
El import diferido es la evidencia: alguien ya sabía que el ciclo estaba ahí.
Mover la extracción a la capa que ya depende de ambos, o inyectarla.
"""

[[done]]
id = "R4"
edge = "store → api"
at = "src/sldb/store/edge_index/model_contribution.py#L41"
imports = "api.schema.describe_field.describe_field"
cycle_weight = "store→api: 1 arista diferida · api→store: 195 aristas"
repaired = """
Hecho (2026-10-18). `describe_field` y sus piezas (kinds, descriptor, description) bajaron a
`models/field_schema/`, que el almacén y las operaciones ven; `api/schema` las reexporta. El
almacén las lee por su costura `store/model_contract.py`, y `tests/test_store_seams.py`
rechaza cualquier import del almacén hacia `api`, `cli` o `selfdoc`.
"""

[[pending]]
id = "R5"
edge = "selfdoc → cli"
at = "src/sldb/selfdoc/python_relation_registry.py#L7"
imports = "cli.model_utils.resolve_model_ref"
cycle_weight = "selfdoc→cli: 1 arista · cli→selfdoc: 14 aristas"
repair = """
Resolver una referencia a un modelo no es trabajo de la interfaz: es una
operación. Subirla a la capa 3 y que ambos la llamen desde ahí.
"""

# ---------------------------------------------------------------------------
# Ejes de capacidad
#
# Las capas de arriba responden «¿quién puede importar a quién?». Esto responde
# otra pregunta: «¿qué sabe hacer el sistema?».
#
# Son dimensiones ortogonales. Una capacidad puede repartirse entre capas, y dos
# paquetes de la misma capa pueden no tener nada que ver. El mapa completo, con
# el acoplamiento medido entre ejes, en propuesta/04-LOS-EJES.md.
#
# Cada eje declara su dependencia externa. Esa es la prueba más simple de que un
# eje es real: si una biblioteca de terceros está confinada a un eje, el eje
# tiene frontera.
#
# No todas se confinan. `pydantic` y `pyyaml` son transversales por diseño —el
# sistema entero está hecho de modelos validados— y vigilar su confinamiento
# produce decenas de falsos positivos que entierran los hallazgos reales. Se
# declaran acá como transversales para que la puerta no las persiga.
#
# Las que SÍ se confinan son las interesantes: `markdown-it-py` en superficie,
# `jinja2` en render, `networkx` en grafo y semántica. Cada una delimita un motor
# reemplazable.

[axis_external]
pervasive = ["pydantic", "pyyaml"]
confined = ["markdown-it-py", "jinja2", "networkx"]
# ---------------------------------------------------------------------------

[[axis]]
id = "superficie"
paths = ["core/ast", "core/segments", "core/handlers"]
external = ["markdown-it-py"]
does = "texto a árbol unificado; la puerta de entrada de cualquier superficie"
identity = true

[[axis]]
id = "representacion"
paths = ["core/ir", "core/contracts", "core/node.py", "core/node_handler.py"]
external = ["pydantic"]
does = "MeaningNode y SurfaceNode: significado y superficie como proyecciones ancladas"
identity = true
note = "es *la* idea del sistema; sin esto lo que queda es un conversor de formato"

[[axis]]
id = "render"
paths = ["core/renderer_engine", "core/renderer.py", "core/extractor", "core/template_extractor.py", "core/data_extractor.py"]
external = ["jinja2"]
does = "árbol a texto reversible; sin esto la representación es un volcado, no un lugar donde trabajar"
identity = true

[[axis]]
id = "contrato"
paths = ["models"]
external = ["pydantic"]
does = "qué es un documento válido"
identity = true

[[axis]]
id = "runtime"
paths = ["runtime"]
external = []
does = "la configuración que decide qué se permite al renderizar, y la validación que une modelo con texto"
identity = true
note = """
Pequeño y de identidad: `extract_model_data` es la operación que convierte texto
en un modelo validado, que es la mitad del contrato del sistema. `config` decide
si una expresión puede evaluarse. Tres archivos que ningún eje puede absorber sin
volverse otra cosa.
"""

[[axis]]
id = "persistencia"
paths = ["store/io", "store/models", "store/layout.py"]
external = []
does = "guardar, indexar, fragmentar, hashear"
identity = false

[[axis]]
id = "consulta"
paths = ["store/query_engine", "api/search.py", "api/where.py"]
external = []
does = "buscar y filtrar por campo"
identity = false

[[axis]]
id = "grafo"
paths = ["store/graph"]
external = ["networkx"]
does = "recorrer, ciclos, orden, centralidad, similitud estructural"
identity = false
extractable = false
note = """
Casi extraíble, y la puerta lo precisó mejor que yo.

Afirmé que no importaba nada fuera de sí mismo. Falso: cinco archivos lo hacen
—`convert.py`, `node_view.py`, `traversal.py`, `analysis/relations.py`— y traen
`edge_index`, `store.models` y `contrato`. Mi comprobación había truncado las
rutas y vi solo los imports internos.

Lo que sí es cierto: 28 de 33 archivos son autónomos, y las cinco aristas se
concentran en la conversión entre el formato del índice de aristas y el del
motor. Eso es una frontera de adaptación, no una fusión — pero hay que cortarla
antes de llamar al eje extraíble.

Aparte: importarlo arrastra 125 módulos porque `store/__init__.py` se ejecuta
antes. Mismo defecto que R2, otra escala.
"""

[[axis_boundary_debt]]
axis = "grafo"
files = ["store/graph/convert.py", "store/graph/node_view.py", "store/graph/traversal.py", "store/graph/analysis/relations.py"]
imports = ["store/edge_index", "store/models", "models"]
repair = """
El motor debería recibir nodos y aristas en su propio formato. Hoy sabe leer el
del índice. Mover la conversión al índice —que ya depende del motor— deja el
motor sin dependencias y lo vuelve extraíble de verdad.
"""

[[axis]]
id = "indice_de_aristas"
paths = ["store/edge_index"]
external = []
does = "derivar aristas de documentos; el constructor, no el motor"
identity = false
note = "contado junto al grafo en el primer mapa, y es un error: el motor no sabe de documentos"

[[axis]]
id = "recuperacion"
paths = ["api/matching", "api/corpus"]
external = []
does = "similitud aproximada por coseno, con caché de vectores y auditoría del índice"
identity = false
note = """
Sin dependencia externa declarada porque es un PUERTO: la aplicación inyecta un
`Embedder` y sin uno degrada a `difflib`. El eje mejor diseñado del sistema, e
invisible desde las dependencias del proyecto — su diseño consiste en no tenerlas.
"""

[[axis]]
id = "bitacora"
paths = ["store/journal", "api/journal.py"]
external = []
does = "una entrada encadenada por hash por cada escritura, con verificación de la cadena"
identity = false

[[axis]]
id = "adaptadores"
paths = ["selfdoc"]
external = ["ast", "argparse", "click"]
does = "derivar documentos de código y de interfaces"
identity = false
note = "tres adaptadores derivados frente a una sola superficie autorada"

[[axis]]
id = "semantica"
paths = ["store/semantic_parents.py", "store/semantic_dag_sync.py", "store/semantic_doc_contribution.py", "store/semantic_dag_graph.py", "store/semantic.py", "store/semantic_tags.py", "store/semantic_doc_tags.py", "api/semantic"]
external = ["networkx"]
does = "jerarquía de tipos como DAG"
identity = false

[[axis]]
id = "enlaces"
paths = ["links"]
external = []
does = "relaciones declaradas entre documentos"
identity = false

# ---------------------------------------------------------------------------
# Deuda de ejes
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Ejes de operación
#
# Los de arriba son motores: saben hacer una cosa con una técnica. Estos son las
# operaciones compuestas que un programa llama, y sin ellos el mapa cubría el
# 40% del sistema.
#
# Mi primer mapa los omitió porque excluí `api/` y `store/` enteros del recuento,
# y ahí vive casi todo el código. Un mapa que ignora el 60% de lo que describe no
# es un mapa.
# ---------------------------------------------------------------------------

[[axis]]
id = "op_documentos"
paths = ["api/documents", "api/actor.py", "api/segments", "store/section_doc_contribution.py", "store/section_paths.py", "store/section_rebuild.py", "store/section_sync.py", "store/documents_dirty.py"]
external = ["markdown-it-py"]
note = """
`section_rebuild.py` usa `markdown-it-py` directamente, fuera del eje de
superficie. Es la única fuga de esa dependencia y vale mirarla: reconstruir las
secciones de un documento debería pedírselo al analizador, no reanalizar.
"""
does = "seguir, dejar de seguir, guardar y navegar documentos y sus tramos editables"
identity = false

[[axis]]
id = "op_modelos"
paths = ["api/model_drafts", "api/model_registry", "api/model_create", "api/schema", "store/model_origin.py", "store/model_import_root.py"]
external = ["ast"]
note = """
Usa `ast` igual que `adaptadores`, y para otra cosa: aquél LEE código para
derivar documentos, éste lo EDITA para modificar un contrato en borrador.

La puerta lo marcó como fuga y no lo es: es la misma herramienta en dos oficios.
Vale declararlo porque la próxima lectura va a dudar igual.
"""
does = "resolver, registrar, describir y editar contratos de modelo en borrador"
identity = false

[[axis]]
id = "op_almacen"
paths = ["api/stores", "api/records", "store/ops.py", "store/export.py", "store/package_version.py", "store/catalog_reconcile.py", "store/runtime_cache.py", "store/diagnostics_models", "store/diagnostics.py", "store/field_set_drift.py"]
external = []
does = "abrir, enlazar, refrescar índices, exportar y diagnosticar un almacén"
identity = false

[[axis]]
id = "op_aristas"
paths = ["api/edges", "api/graph", "store/edge_sync.py", "store/edge_rebuild.py", "store/edge_doc_contribution.py", "store/model_node.py"]
external = []
does = "leer, reconstruir y verificar el índice de aristas; ejecutar consultas de grafo"
identity = false

[[axis]]
id = "codigo"
paths = ["code"]
external = ["ast", "tree-sitter", "tree-sitter-python"]
does = "leer código Python como símbolos con tree-sitter, y un fingerprint por nodo de cada definición (portado de kimun)"
identity = false
note = "no importa nada de sldb: es la superficie de entrada del código, como `core/ast` lo es del Markdown"

[[axis]]
id = "anclaje"
paths = ["api/anchors"]
external = []
does = "anclar una afirmación a un símbolo de código: grabar lo visto, comprobarlo, reconectar lo que se movió"
identity = false

[[axis]]
id = "cache"
paths = ["store/built_cache.py", "store/runtime_cache.py", "store/runtime_cache_disk.py", "store/runtime_cache_signature.py", "store/user_cache.py", "store/derived_rebuild.py"]
external = []
does = "memorizar lo derivado y saber cuándo invalidarlo"
identity = false

[[axis]]
id = "codec"
paths = ["store/codec.py", "store/runtime_codec.py", "store/model_contract.py"]
external = []
does = "serializar y deserializar el estado del almacén, y leer lo que una clase de modelo declara: las costuras del almacén hacia el resto de sldb"
identity = false

[[axis]]
id = "migracion"
paths = ["store/migration.py", "store/migration_hash_names.py", "store/migration_legacy_layout.py", "store/legacy_contract.py"]
external = []
does = "leer almacenes escritos por versiones anteriores"
identity = false
note = "aquí viven las decisiones que los diagnosticadores encontraron solo en comentarios"

[[axis]]
id = "federacion"
paths = ["store/catalog.py", "store/resolver.py", "store/facade.py", "store/query.py", "store/predicates.py"]
external = []
does = "encontrar almacenes, resolver entre varios y ofrecer la fachada de consulta"
identity = false

[[axis]]
id = "errores"
paths = ["core/exceptions", "store/exceptions.py", "core/finding.py"]
external = []
does = "la jerarquía de excepciones del sistema, y el hallazgo (error o alerta) que reporta un comando"
identity = false
note = "la capa más baja que todas las demás necesitan nombrar; por eso R2 importaba"

[[axis]]
id = "identidad_y_hash"
paths = ["store/hashing.py", "store/documents_hash.py"]
external = []
does = "calcular y comparar las huellas que detectan deriva"
identity = true
note = """
De identidad porque es lo que hace que un documento derivado sea verificable
contra su origen. Sin esto el sistema produce documentación; con esto produce
proyecciones con detección de rancidez.
"""

[[axis_debt]]
id = "dos-lenguajes-de-consulta"
between = ["consulta", "grafo"]
what = """
`store/query_engine/where_parse.py` usa `=`, `!=`, `<=`, `>=`.
`store/graph/language/field_condition.py` usa `eq`, `ne`, `lt`, `gt`, `contains`,
`starts_with`, `is_null`, `is_not_null`.

Dos vocabularios para filtrar por campo. No es código duplicado: son dos
lenguajes que alguien tiene que aprender por separado para hacer lo mismo en dos
ejes, y un cambio en uno no llega al otro.
"""
repair = "un solo lenguaje de condiciones, compartido por los dos ejes"

[[axis_debt]]
id = "adaptador-sin-uso"
between = ["adaptadores"]
what = """
`selfdoc/click_scanner.py` está escrito completo y no se referencia desde `src/`
ni desde `tests/`. Ningún documento del almacén viene de él.

Y hay algo peor, verificado: **importa `click` en la línea 8, sin `try`, y `click`
no está en las dependencias del proyecto.**

No falla porque nadie lo carga: `sldb.selfdoc` se importa sin traer `click`, y
`click` está en el entorno local por dependencias ajenas (typer, langgraph-cli).
En un entorno limpio, cualquiera que importara este módulo obtendría
`ModuleNotFoundError`.

Es un fallo latente que solo existe porque el código está muerto. La prueba de
que no se ejercita es que el defecto sobrevivió.
"""
repair = """
Dos opciones honestas: declarar `click` como dependencia opcional y ejercitar el
adaptador con un caso real, o retirarlo. Lo que no sirve es dejarlo: parece una
capacidad y es un error de importación esperando.
"""

[[axis_debt]]
id = "superficie-autorada-unica"
between = ["superficie"]
what = """
`MarkdownASTHandler` es la única implementación concreta de `BaseASTHandler` tras
317 commits. La abstracción está ejercitada por tres adaptadores derivados y por
ninguna segunda superficie autorada.
"""
repair = """
Una segunda superficie autorada — o la declaración de que la abstracción es para
superficies derivadas y Markdown es la única autorada por diseño.
"""

# ---------------------------------------------------------------------------
# Unidades viables
#
# Los niveles de arriba son orden de dependencia. Esto es otra cosa: qué partes
# se pueden sostener por separado.
#
# La diferencia importa porque es el error natural al leer el grafo: los seis
# niveles del DAG NO son las unidades. Una unidad viable absorbe su propia
# variedad —cuando algo cambia dentro, se repara dentro— y un nivel no tiene por
# qué.
#
# La prueba: ¿tiene esta pieza sus propias siete funciones? El razonamiento
# completo en propuesta/06-NIVELES-NO-SON-UNIDADES.md.
# ---------------------------------------------------------------------------

[[axis]]
id = "vocabulario_visual"
paths = ["notations", "models/notation", "models/notation_models.py"]
external = ["pydantic", "pyyaml"]
does = "notaciones, glifos, enlaces, paletas y vistas como modelos y catálogos builtin; absorbido de spec2viz (SV01)"
identity = false
note = """
Capa 0 a propósito: es vocabulario, no operación. La comprobación de que un `where`
parsea es un PUERTO (`where_check.set_where_parser`) que `api/notations` conecta al
parser del almacén; sin él no se comprueba, igual que cuando vivía fuera de sldb.
"""

[[axis]]
id = "vistas"
paths = ["api/notations"]
external = []
does = "resolver una notación sobre documentos del almacén y evaluar vistas de proyección; sincronizar notaciones y paletas (SV02)"
identity = false

[[unit]]
id = "nucleo"
axes = ["superficie", "representacion", "render", "contrato", "runtime", "identidad_y_hash", "errores", "codigo"]
needs = 4  # medido 2026-11-06 tras SV01/SV02: models reexporta notation_models; antes 3/35
needed_by = 39  # medido 2026-11-06 tras SV01/SV02: models reexporta notation_models; antes 3/35
indivisible = false
why = """
Los cinco ejes de identidad forman un nudo de 11 aristas internas. Lo declaré
indivisible y es falso: el corte mínimo son 4 aristas de peso total 6, calculado
por fuerza bruta sobre las 11.

Primero afirmé que bastaba mover `runtime/validation.py`. Lo simulé y el nudo
seguía: mover un archivo cambia de sitio el problema sin resolverlo.
"""

[nucleo_min_cut]
edges = 4
total_weight = 6
cuts = [
  { edge = "superficie → render", at = "core/segments/instrumented_render.py#L16", imports = "SLDBRenderer", weight = 3, note = "un render instrumentado dentro del eje de superficie: está del lado equivocado" },
  { edge = "representacion → superficie", at = "core/node_handler.py#L3", imports = "SharedNodeHandler", weight = 1, note = "una pieza de representación que conoce al que la va a manejar" },
  { edge = "render → runtime", at = "core/renderer_engine/python_expr.py#L5", imports = "python_expression_is_allowed", weight = 1, note = "es R1" },
  { edge = "contrato → runtime", at = "models/structured_doc.py#L67", imports = "extract_model_data", weight = 1, note = "es R3; import diferido" },
]

[[unit]]
id = "persistencia"
axes = ["persistencia", "consulta", "federacion", "cache", "codec", "migracion", "bitacora", "semantica", "indice_de_aristas"]
needs = 19  # medido 2026-11-06 tras GO04 y SV02; antes 16/35
needed_by = 36  # medido 2026-11-06 tras GO04 y SV02; antes 16/35
why = "el centro de gravedad del sistema: 110 aristas entran desde los ejes de operación"

[[unit]]
id = "grafo"
axes = ["grafo"]
needs = 5  # GO03: eval de store/graph/backend reutiliza el parser where de store/query_engine
needed_by = 4  # GO05: consulta (query_engine.rules y los shims where_parse/where_subject) usa el lenguaje de store/graph/language
extractable_today = false
why = """
Unidad propia: 33 archivos, 28 de ellos autónomos. Necesita 7 imports de cuatro
ejes y lo necesitan 20 —casi todos de `op_aristas`—, así que produce mucho más de
lo que consume.

No extraíble hoy por la deuda `axis_boundary_debt`: cinco archivos convierten
entre el formato del índice de aristas y el del motor. Cortar esa conversión
—moviéndola al índice, que ya depende del motor— lo deja sin dependencias.
"""

[[unit]]
id = "adaptadores"
axes = ["adaptadores"]
needs = 5
needed_by = 0
extractable_today = true
why = "nadie depende de él; deriva documentos de Python, argparse y click"

[adaptadores_recursion]
answer = "R2 existe acá"
evidence = """
Dos ramas que no comparten código de extracción: 8 archivos `python_*` que leen
el AST de Python, 7 que leen argparse y click. Lo único compartido es
`planned_document`, el contrato de salida, cuya docstring dice: «Declare the
planned-document contract shared by planning, persistence, and inspection. It
does not write files, register models, or decide which documents need saving.»
"""
subunits = [
  { id = "python-ast", files = 8, absorbs = "cambios en el AST de Python" },
  { id = "interfaz", files = 7, absorbs = "cambios en argparse y click" },
]
contract = "planned_document"
why_it_is_recursion = """
Un adaptador nuevo —otro lenguaje— se repara DENTRO de `adaptadores`: implementa
el contrato y nada más cambia. Eso es absorber su propia variedad, que es la
definición de unidad viable.
"""

[[unit]]
id = "recuperacion"
axes = ["recuperacion"]
needs = 4
needed_by = 0
extractable_today = true
why = "nadie depende de él; puerto Embedder sin dependencia vectorial propia"

# No son unidades, y conviene decir por qué:

[[unit]]
id = "notacion"
axes = ["vocabulario_visual", "vistas"]
needs = 3  # medido 2026-11-06
needed_by = 2  # medido 2026-11-06
indivisible = false
why = """
Lo que spec2viz hacía fuera del repositorio, adentro: el vocabulario (capa 0) y
el resolvedor (capa 3) son una capacidad con una superficie propia (`sldb
notations`, `/notations/*`, `/views/projection*`). Las cuentas las dice la puerta.
"""

[[non_unit]]
id = "operacion"
axes = ["op_almacen", "op_documentos", "op_modelos", "op_aristas", "anclaje"]
needs = 47  # medido 2026-11-06 tras SV02: api/notations la necesita; antes 47/8
needed_by = 9  # medido 2026-11-06 tras SV02: api/notations la necesita; antes 47/8
verdict = "fachada"
why = """
158 archivos, el grupo más grande, y el candidato más obvio por tamaño. Pero
necesita 16 ejes de fuera y solo 6 lo necesitan: es un consumidor neto.

Compone operaciones sobre lo que otras unidades producen y no produce nada que
otras necesiten. Eso es legítimo —es transporte— pero no absorbe su propia
variedad: cualquier cambio en las unidades de abajo la obliga a cambiar.
"""

[[non_unit]]
id = "enlaces"
axes = ["enlaces"]
needs = 2
needed_by = 0
verdict = "capacidad sin superficie"
why = """
7 archivos que parsean, resuelven y recuperan referencias entre documentos, y
componen un documento a partir de otros. Solo los usa la interfaz.

Lo descarté primero por tamaño y era mal criterio: `compose_document` es una
capacidad real que está construida y no expuesta. No es una sobra, es una
superficie que falta.
"""

# ---------------------------------------------------------------------------
# Lo que falta para que las unidades sean viables
#
# Las cuatro tienen ejecución —es lo que hacen— y les faltan las mismas dos
# funciones, por la misma razón: están organizadas fuera de ellas.
# ---------------------------------------------------------------------------

[[unit_gap]]
function = "auditoria"
missing_in = ["nucleo", "persistencia", "grafo", "adaptadores", "recuperacion"]
evidence = """
`tests/` tiene 3 carpetas para 24 ejes y 26 archivos sueltos en la raíz.
`tests/core/` no existe: el eje `representacion` —la idea central del sistema— no
tiene ninguna prueba que lo ejercite directamente, igual que `bitacora`.
"""
criterion = """
`tests/<unidad>/` corre sola y pasa, sin cargar las otras unidades. Hoy es
imposible: las pruebas no están agrupadas por unidad.
"""

[[unit_gap]]
function = "regulacion"
missing_in = ["nucleo", "persistencia", "grafo", "adaptadores", "recuperacion"]
evidence = """
Las tres reglas mecanizadas viven en `tests/test_clean_code_rules.py` y recorren
`src/` entero: una clase por archivo, diez líneas por función, ochenta por
archivo. Ninguna unidad tiene una regla que le aplique solo a ella.
"""
criterion = "cada unidad declara sus reglas y algo las verifica solo contra ella"

# ---------------------------------------------------------------------------
# Los alfileres
#
# 32 imports de peso 1 o 2 sostienen los dos nudos. Mientras existan, cualquier
# reorganización de carpetas es cosmética: el acoplamiento no está en la
# estructura de directorios.
#
# Precedente medido: en la Fase 0, una arista de peso 1 costaba 46 módulos.
# ---------------------------------------------------------------------------

[pins]
core_knot = 6
operation_knot = 26
note = """
Ignorando las de peso ≤2 el nudo de 11 se parte en 3, el mayor de 4. Ese 4 es la
fusión real; el resto es conveniencia acumulada.
"""

# ---------------------------------------------------------------------------
# Lo que a `persistencia` le falta para absorber su variedad
#
# Hallazgo de propuesta/09-DUDAS-CERRADAS.md: no hay versionado del formato de
# almacenamiento. La migración detecta versiones antiguas POR LA EXISTENCIA DE
# ARCHIVOS:
#
#   # store/migration_legacy_layout.py:37
#   if store_index_path(store_path).exists() or not legacy_store_index_path(...).exists():
#       return False
#
#   «si existe el archivo nuevo, o no existe el viejo, no hay nada que migrar»
#
# Eso funciona y no escala: cada formato nuevo exige una función `legacy_*_path`
# más, y que cada lector tolere ambas formas. Lo tercero escapa de la unidad, y
# ahí es donde las reglas de compatibilidad terminan viviendo en comentarios.
# ---------------------------------------------------------------------------

[persistencia_gap]
missing = "layout_version en el índice de almacén"
detection_today = "por existencia de archivos"
evidence_of_leak = """
«tolerancia a almacenes escritos antes de `field_hashes`: absent is unknown,
never no-fields» — una regla de compatibilidad de formato que vive en dos
comentarios de código, encontrada por los diagnosticadores sin saber qué era.

Con un número de versión sería una condición explícita en un solo lugar.
"""
consequence = """
`persistencia` es una unidad —produce más de lo que consume— pero no absorbe
cambios de formato: se propagan a cada lector. Es la única de las cinco unidades
a la que le falta algo además de auditoría y regulación.
"""

# ---------------------------------------------------------------------------
# Lo que falta como operación, no como diseño
# ---------------------------------------------------------------------------

[[missing_operation]]
id = "lectura-de-indices"
evidence = """
deskops/deskops/operations.py:2801 encadena tres lecturas para recorrer un
almacén: índice de almacén → índice de modelos → índice de documentos. Nadie
debería conocer esa cadena.
"""
asymmetry = """
La escritura SÍ existe como operación: `api/stores/update_store_indexes.py`.
Hay operación para escribir los índices y no para leerlos, y por eso el
consumidor bajó a `store/io`.
"""
repair = "una operación de lectura que oculte la cadena; entonces las tres funciones vuelven a ser internas"

FILE:docs/opsys/bridge_primitives/README.md
# Opsys Bridge Primitives

## Purpose

This document defines the primitives that connect the documentary surface to the code surface.

The documentary surface holds intent, policy, procedure, evidence, and declared structure.
The code surface holds implementation, executable behavior, and runtime constraints.

Bridge primitives let both surfaces remain distinct while still being linked, checked, and synchronized.

## Why A Bridge Layer Exists

Without a bridge layer:

- documentation drifts from implementation
- code loses declared intent
- procedures become stale prose
- examples rot silently
- operational rules stay trapped in team memory

With a bridge layer:

- documentary records can point to code precisely
- alignment rules can be expressed explicitly
- drift can be linted and tested
- transforms can synchronize both surfaces intentionally

## Bridge Primitive Set

The first bridge primitive set is:

1. `Reference`
2. `Constraint`
3. `Lint`
4. `Probe`
5. `Transform`

## Reference

### Definition

A `Reference` links an operational record or documentary artifact to a code target.

The reference should be resolvable, not just textual.

### Why It Exists

- to connect intent to implementation
- to make traceability explicit
- to support navigation in both directions
- to let later lints and probes verify the link

### Static Shape

Suggested fields:

- `source_kind`
- `source_id`
- `target_kind`
- `target_locator`
- `target_display`
- `relation_type`
- `resolution_method`
- `status`
- `notes`

### Target Kinds

Typical target kinds:

- file
- module
- class
- function
- method
- test
- command
- flag
- symbol
- generated artifact

### Resolution Methods

Typical resolution methods:

- path exists
- symbol resolves
- command resolves
- glob match
- parser target exists
- test target exists

### Action Surface

- `references create`
- `references show`
- `references list`
- `references verify`
- `references trace`
- `references repair`

### Notes

`Reference` should become the minimal cross-surface currency of the system.

If a documentary artifact cannot reference the code surface in a durable way, the system will struggle to support trustworthy transforms, lints, or probes later.

## Constraint

### Definition

A `Constraint` is a declared rule that should hold across documentary and code surfaces.

### Why It Exists

- to turn expectations into named rules
- to let the team reason about alignment explicitly
- to support linting and probing from shared semantics

### Static Shape

Suggested fields:

- `name`
- `scope`
- `statement`
- `severity`
- `evaluation_mode`
- `source_surfaces`
- `target_surfaces`
- `remediation_hint`

### Constraint Examples

- every first-class CLI noun must have help coverage
- every documented command example must resolve to a real command path
- every onboarding ritual must reference at least one executable probe
- every routine with a hook must define a trigger

### Action Surface

- `constraints create`
- `constraints show`
- `constraints list`
- `constraints check`
- `constraints violations`

## Lint

### Definition

A `Lint` is a cheap, frequent, mostly deterministic executable check over one or more surfaces.

### Why It Exists

- to detect drift early
- to keep standards operational
- to provide fast feedback before deeper probes or tests run

### Static Shape

Suggested fields:

- `name`
- `scope`
- `constraint_ref`
- `inputs`
- `severity`
- `autofixable`
- `fix_hint`

### Lint Examples

- broken references
- stale command examples
- unresolved symbol links
- missing help coverage for documented command groups
- routine/checklist mismatch

### Action Surface

- `lints list`
- `lints show`
- `lints run`
- `lints result`
- `lints fix`

## Probe

### Definition

A `Probe` is an executable alignment check that tests whether documentary claims and code behavior still agree.

### Why It Exists

- to validate cross-surface truth
- to test behavior, not just structure
- to catch subtle divergence that lint cannot detect

### Static Shape

Suggested fields:

- `name`
- `intent`
- `target_surface`
- `documentary_inputs`
- `code_inputs`
- `expected_shape`
- `failure_signal`
- `evidence_mode`

### Probe Examples

- run a documented CLI example and compare output shape
- verify a documented command group exists in parser/help/runtime
- verify references to files and symbols still resolve
- verify documented onboarding steps remain recoverable

### Action Surface

- `probes create`
- `probes show`
- `probes list`
- `probes run`
- `probes result`
- `probes explain`

## Transform

### Definition

A `Transform` converts one surface representation into another while preserving intended meaning.

### Why It Exists

- to reduce duplicate maintenance
- to generate useful derivatives
- to synchronize documentary and code surfaces intentionally

### Static Shape

Suggested fields:

- `name`
- `source_kind`
- `target_kind`
- `inputs`
- `outputs`
- `direction`
- `reversible`
- `safety_level`

### Transform Examples

- generate help docs from structured command definitions
- derive checklist stubs from routine definitions
- materialize code annotations from documentary records
- build documentary views from code metadata

### Action Surface

- `transforms create`
- `transforms show`
- `transforms list`
- `transforms preview`
- `transforms run`
- `transforms diff`

## Bridge Execution Order

The bridge layer should usually work in this order:

1. define references
2. declare constraints
3. run lints for cheap drift detection
4. run probes for executable alignment validation
5. use transforms where synchronization should be automated

## Relation To Documentary Primitives

Bridge primitives are not replacements for documentary primitives.

They extend them.

Examples:

- an `IssueReport` can have references and probes
- a `Routine` can have constraints and transforms
- a `Checklist` can be guarded by lints or probes
- a `Ritual` can require reference verification before closure

## First Credible Slice

The smallest useful bridge slice is:

1. `Reference`
2. one or two high-value `Constraint` definitions
3. a `Lint` for broken or stale references
4. a `Probe` for at least one documented CLI walkthrough

That is enough to prove the documentary-to-code bridge without overbuilding the system.

## Open Questions

1. Should `Reference` targets be purely symbolic, purely path-based, or support both from the first slice?
2. Should `Lint` and `Probe` both derive from a shared executable-check primitive?
3. Which transforms should remain advisory only, and which should be allowed to write changes automatically?
4. Which failures should block workflow progression, and which should only warn?

FILE:CHANGELOG.md
# Changelog

Version note (2026-09-13, updated 2026-10-18): `pyproject.toml` declares `0.1.12`; it was `0.1.0` while PyPI already had `0.1.1`. Existing entries below are historical development records, not a verified registry release inventory. The product-generation label “v1” is separate from package versioning. No new package version or release is created by this documentation reconciliation.

## 0.1.13 — not released yet (no tag, not on PyPI)

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
Cold-bundle de la tarea task-go06-ruledoc-rules-check-y-rules-explain: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest tests/api/test_rules.py sin fallos ni saltados
- store temporal Base, X < Base, Y < X, Z < Base: RuleDoc con sujeto model <= X aplica a X e Y y no a Z
- rules check: Finding error/alert con clausula y nodo; exit 1 solo ante error; sin --subject solo on_check; --subject por Model:name y por ruta; incomplete como alert rules/<nombre>/incomplete
- rules explain: finding de eval y exits 0/1/2; exit 3 con una regla cuyo where excluye al documento
- RuleDoc mal formada (condition, where, severidad, momento, sujeto) rechazada al escribir, un test de rechazo por campo
- TMPDIR=/dev/shm pytest tests/test_clean_code_rules.py tests/test_store_seams.py en verde
- suite completa sin rojos (una vez, al final del nodo, la corre el supervisor)

