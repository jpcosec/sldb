FILE:desk/tasks/task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for.md
---
sldb:
  by: agent
  at: '2026-11-19T10:43:21Z'
  authority: generated
  via: save_document_payload
id: task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-080455-suggestion-docs-track-force-re-indexa-sin-validar-pedido-de-un-re-index-que-valide.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/track_document_file.py
- src/sldb/store/ops.py
- src/sldb/cli/parsers/docs1.py
- tests/api/test_api_documents.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
---

# docs track --reindex re-indexa un documento ya trackeado validándolo, sin saltar el round-trip como --force

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, docs track --force sobre un documento ya trackeado devuelve rc 0 aunque el archivo no valide (enum inválido, frontmatter YAML roto) y queda indexado; después docs show falla. Es lo que dice el contrato: --force salta el round-trip. Por eso la UI guarda con untrack + track (5,5-6,2 s contra 4-5 s). Origen: desk/inbox/20261117-080455-suggestion-docs-track-force-re-indexa-sin-validar-pedido-de-un-re-index-que-valide.md.

## Goal

_Describe the concrete result this task must produce._

docs track --reindex (y track_document_file(..., reindex=True)) re-indexa desde el archivo un documento ya trackeado en la misma ruta, como --force, pero corre las mismas validaciones que un track normal: si el archivo no valida falla con el error de validación y deja el índice como estaba. --force no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: el flag --reindex en el parser y el comando de docs track, el parámetro reindex en track_document_file (src/sldb/api/documents/track_document_file.py) y su paso hasta StoreOperations.track (src/sldb/store/ops.py); --reindex y --force juntos se rechazan con un error claro; tests en tests/api/test_api_documents.py: reindex de un archivo válido editado deja el payload nuevo, de uno inválido falla y no cambia el índice, sobre un documento no trackeado se comporta como track. CHANGELOG y ayuda. No entra: cambiar --force.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/api/documents/track_document_file.py, src/sldb/store/ops.py (StoreOperations.track y el camino de force de la tarea CI2) y el parser y el comando de docs track. 2) Tests que fallen antes, en tests/api/test_api_documents.py: --reindex sobre un documento ya trackeado y válido lo re-indexa; sobre uno cuyo archivo no valida falla con el error de validación y el índice queda byte a byte igual; --reindex con --force da un error claro; --force no cambia. 3) Implementar. 4) Como hay un flag nuevo (--reindex), correr 'PYTHONPATH=src sldb selfdoc sync' y commitear la referencia CLI que regenere; después 'PYTHONPATH=src sldb selfdoc check' en 0. 5) CHANGELOG. 6) quick_gates del desk (bash tools/check.sh --fast) en 0 antes del commit, con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a sldb-ui.

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

FILE:desk/atoms/atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta.md
---
sldb:
  by: agent
  at: '2026-11-16T22:50:52Z'
  authority: generated
  via: create_document
id: atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta
title: track con force re-indexa desde el archivo un documento ya trackeado en la
  misma ruta
five_wh_one_plus: what
tags:
- system:sldb
- topic:store
provenance: tarea CI2 (nota sldb-ui 162239 y job store del CI sobre c5cb52f0), ejecutor
  deskops-e-146155e482b3, tester deskops-t-eab6088c807b PASA
---

# track con force re-indexa desde el archivo un documento ya trackeado en la misma ruta

## Answer

track_document_file(..., force=True) y docs track --force saltan la comprobación de round-trip y, si el documento (modelo, nombre) ya está trackeado en la misma ruta del proyecto, lo re-indexan desde el contenido actual del archivo (shard, índice y aristas) bajo store_lock; repetirlo sin cambios es idempotente y declare_tracked no duplica la entrada. Con force y otra ruta falla con SLDBStoreError que nombra las dos rutas (para mover está move). Sin force, el error 'Doc <n> already tracked.' no cambia.

FILE:src/sldb/api/documents/track_document_file.py
"""Start tracking an existing Markdown file as a document of a registered model."""

from __future__ import annotations
from sldb.api.stores.declaration_sync import declare_tracked, project_relative

from pathlib import Path

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.documents.on_write_gate import check_entering_text
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.stores.policy import Policy
from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.ops import track_document
from sldb.store.source_read import read_source_text, refuse_unreadable


def track_document_file(store: str | Path | None, model_name: str, path: str | Path, name: str | None = None, pythonpath: str | None = None, force: bool = False, actor: str | None = None) -> DocumentReference:
    """Index a Markdown file as a document of a model.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file; a relative path is relative to the project root, not the cwd.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        force: Track without checking that the file round-trips under the model; a document
            already tracked with this model and name at this same path is re-indexed from the
            file's current content instead of refused (one at another path is still refused: use move).
        actor: Optional caller label; accepted for compatibility, no longer recorded (the journal was retired on 2026-11-04).

    Returns:
        The tracked document.

    Raises:
        SLDBStoreError: When the model is not registered, when the document is already tracked
            and `force` is False, or when it is tracked at another path.
        SLDBValidationError: When the file does not round-trip, or when it carries
            headings the model does not declare, and `force` is False.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    doc_path = _resolve_path(path, location.project_root)
    doc_name = name or doc_path.stem
    text = read_source_text(doc_path)
    if not force:
        _refuse_unfit(registered.model_type, text, doc_name, location.store_path)
    check_entering_text(location.store_path, registered.model_type, registered.entry.name, doc_name, text, force)
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath, force)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    """The path to track, refused before it is opened when it is a symlink or escapes the root
    (`source_read.refuse_unreadable`): resolving it first would track what it points to."""
    joined = root / Path(raw)
    refuse_unreadable(root, joined)
    return joined.resolve()


def _track(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None, force: bool) -> None:
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath, force)
    declare_tracked(sp, root, registered.entry.name, project_relative(root, doc_path), doc_name)


def _refuse_unfit(model_type: type, text: str, doc_name: str, store_path: Path) -> None:
    """Refuse a text that does not round-trip, or carries noise or frontmatter the model does not declare."""
    _check_roundtrip(model_type, text)
    refuse_structural_noise(model_type, text, doc_name, Policy.of_store(store_path))
    refuse_undeclared_frontmatter(model_type, text, doc_name)


def _check_roundtrip(model_type: type, text: str) -> None:
    """Refuse a file that does not extract and re-render identically under the model."""
    valid, details = validate_model_input_roundtrip(model_type, text)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)

FILE:src/sldb/store/ops.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash
from sldb.store.hashing import hash_fields_with_map, hash_models_layer, hash_text
from sldb.store.model_node import stamp_model_node
from sldb.store.io import (
    load_models_index, save_models_index, save_store_index, store_lock,
)
from sldb.store.io.shards import load_document_shard, save_document_shard
from sldb.store.layout import documents_shard_path
from sldb.store.models import DocumentEntry, StoreIndex
from sldb.store.runtime_codec import index_block
from sldb.store.edge_rebuild import rebuild_edges_indexes
from sldb.store.section_rebuild import rebuild_sections_indexes
from sldb.store.semantic import rebuild_semantic_indexes
from sldb.store.source_read import read_source_text


class StoreOperations:
    """Operations for the SLDB store."""

    @staticmethod
    def track(store_path: Path, project_root: Path, store_index: StoreIndex, model_type: type, model_entry: Any, doc_path: Path, doc_name: str, resolve_model_ref: Callable, pythonpath: str | None = None, force: bool = False) -> None:
        """With `force`, a document already tracked at the same path is re-indexed from the file."""
        rel = _get_rel(doc_path, project_root)
        StoreOperations._pre_check(store_path, rel, model_entry, doc_name, force)
        txt = read_source_text(doc_path)  # O_NOFOLLOW; `track_document_file` refused a symlink or an escape first
        with store_lock(store_path):
            StoreOperations._pre_check(store_path, rel, model_entry, doc_name, force)
            StoreOperations._do_track(store_path, project_root, store_index, model_type, model_entry, doc_name, rel, txt, resolve_model_ref, pythonpath)

    @staticmethod
    def _pre_check(store_path, rel_path, model_entry, doc_name, force=False):
        """Refuse a document already tracked, unless `force` and its shard names the same path."""
        from sldb.store.exceptions import SLDBStoreError
        tracked = load_document_shard(documents_shard_path(store_path, model_entry.name, doc_name))
        if tracked is not None and not force:
            raise SLDBStoreError(f"Doc '{doc_name}' already tracked.")
        if tracked is not None and tracked.path != rel_path:
            raise SLDBStoreError(f"Doc '{doc_name}' already tracked at '{tracked.path}', not '{rel_path}'; use move.")

    @staticmethod
    def _do_track(store_path, root, st_idx, m_type, m_entry, d_name, rel_path, text, res_ref, py_path):
        content_hash, field_hashes = _safe_hashes(m_type, text)
        entry = DocumentEntry(name=d_name, path=rel_path, hash_c=hash_text(text), hash_d=content_hash, field_hashes=field_hashes, provenance=index_block(text))
        save_document_shard(documents_shard_path(store_path, m_entry.name, d_name), entry)
        documents_hash.note(store_path, m_entry.name, entry)
        _update_model_summary(store_path, root, m_entry, m_type)
        rebuild_semantic_indexes(store_path, root, res_ref, py_path)
        rebuild_sections_indexes(store_path, root, res_ref, py_path)
        rebuild_edges_indexes(store_path, root, res_ref, py_path)
        cascade_store_hash(store_path, root, st_idx)


def _update_model_summary(store_path: Path, root: Path, m_entry: Any, model_type: Any = None) -> None:
    """The model node and its children, from the operation's own child-hash map — no re-read
    of every document shard (PLAN 15 capa 7)."""
    m_idx = load_models_index(root / m_entry.models_index)
    stamp_model_node(m_idx, documents_hash.roster_hash_of(store_path, m_entry.name), model_type)
    m_idx.documents_count = documents_hash.count_of(store_path, m_entry.name)
    save_models_index(root / m_entry.models_index, m_idx)


def track_document(store_path: Path, project_root: Path, store_index: StoreIndex, model_type: type, model_entry: Any, doc_path: Path, doc_name: str, resolve_model_ref: Callable, pythonpath: str | None = None, force: bool = False) -> None:
    """Track a document in the store and update hashes; with `force`, re-index one already tracked at the same path."""
    StoreOperations.track(store_path, project_root, store_index, model_type, model_entry, doc_path, doc_name, resolve_model_ref, pythonpath, force)

def cascade_store_hash(store_path: Path, project_root: Path, store_index: StoreIndex) -> None:
    """Recompute the Merkle root from every model node and persist it."""
    indices = [load_models_index(project_root / m.models_index) for m in store_index.models]
    store_index.store_hash = hash_models_layer(indices)
    save_store_index(store_path, store_index)


cascade_hash_a = cascade_store_hash   # deprecated alias

def _get_rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)

def _safe_hash(model_type: type, text: str) -> str:
    return _safe_hashes(model_type, text)[0]


def _safe_hashes(model_type: type, text: str) -> tuple[str, dict[str, str]]:
    """A document's `content_hash` and per-field map, or empties when it no longer extracts.

    An empty map means "could not be computed", never "no fields": a consumer comparing
    against it has to fall back to the whole document.
    """
    try:
        return hash_fields_with_map(model_type, text)
    except Exception:
        return "", {}

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
    t.add_argument("--force", action="store_true", help="Skip the round-trip check; a doc already tracked at this same path is re-indexed from the file")

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

FILE:tests/api/test_api_documents.py
"""`sldb.api` document operations and the `sldb.cli` bridges over them."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import sldb.api as api
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import save_declaration
from sldb.cli import dict_utils
from sldb.cli.commands.fields_save import save_payload
from sldb.core.exceptions import SLDBError, SLDBPayloadSaveError, SLDBStoreError, SLDBValidationError
from sldb.store.query import load_runtime_documents

from tests.store.invalid_memo_store import store_with_invalid  # noqa: F401 - the fixture

from .conftest import PAYLOAD


def _title(api_store, name: str) -> str:
    docs = load_runtime_documents(api_store.store, api.resolve_model_ref, api_store.pythonpath)
    return next(d.payload["title"] for d in docs if d.name == name)


def test_save_document_payload_rewrites_markdown_and_indexes(api_store):
    saved = api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Fixed login"}, api_store.pythonpath)
    assert saved.path.resolve() == (api_store.root / "login.md").resolve()
    assert "# Fixed login" in saved.path.read_text(encoding="utf-8")
    api.open_store(api_store.store)
    assert _title(api_store, "login") == "Fixed login"


def test_save_document_payload_refuses_unknown_documents_and_models(api_store):
    with pytest.raises(SLDBPayloadSaveError, match="Doc 'ghost' not registered."):
        api.save_document_payload(api_store.store, "TicketDoc", "ghost", PAYLOAD, api_store.pythonpath)
    with pytest.raises(SLDBPayloadSaveError, match="Model 'NopeDoc' not registered."):
        api.save_document_payload(api_store.store, "NopeDoc", "login", PAYLOAD, api_store.pythonpath)


def test_cli_save_payload_still_exits_with_the_message(api_store):
    doc = SimpleNamespace(model_name="TicketDoc", name="ghost")
    with pytest.raises(SystemExit, match="Doc 'ghost' not registered."):
        save_payload(doc, PAYLOAD, str(api_store.store), api_store.pythonpath)


def test_track_document_file_refuses_a_file_the_model_cannot_read(api_store):
    (api_store.root / "broken.md").write_text("not a ticket\n", encoding="utf-8")
    with pytest.raises((SLDBValidationError, ValidationError)):
        api.track_document_file(api_store.store, "TicketDoc", "broken.md", pythonpath=api_store.pythonpath)


def test_track_document_file_resolves_relative_paths_against_the_project_root(api_store):
    api_store.write_document("signup", PAYLOAD)
    tracked = api.track_document_file(api_store.store, "TicketDoc", "signup.md", pythonpath=api_store.pythonpath, force=True)
    assert (tracked.model, tracked.name, tracked.path) == ("TicketDoc", "signup", (api_store.root / "signup.md").resolve())


def test_untrack_document_drops_it_from_the_store(api_store):
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    untracked = api.untrack_document(api_store.store, "signup", api_store.pythonpath)
    assert (untracked.model, untracked.name) == ("TicketDoc", "signup")
    assert (api_store.root / "signup.md").exists()
    with pytest.raises(SLDBError, match="not found"):
        api.untrack_document(api_store.store, "signup", api_store.pythonpath)


def test_a_document_can_be_named_by_its_absolute_path(api_store):
    """The store records paths relative to the project root; an absolute one used to miss."""
    path = (api_store.root / "signup.md").resolve()
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    deleted = api.delete_document(api_store.store, str(path), api_store.pythonpath)
    assert (deleted.model, deleted.name) == ("TicketDoc", "signup")
    assert not path.exists()


def test_payload_paths_are_the_cli_helpers():
    assert dict_utils.deep_get is api.deep_get and dict_utils.deep_set is api.deep_set
    payload = {"items": [{"name": "a"}]}
    api.deep_set(payload, "items.0.name", "b")
    api.deep_set(payload, "meta.owner", "jp", create=True)
    assert api.deep_get(payload, "items.0.name") == "b"
    assert api.deep_delete(payload, "meta.owner") == {"items": [{"name": "b"}], "meta": {}}
    with pytest.raises(TypeError):
        api.ensure_list(payload, "meta")


def test_move_document_moves_the_file_and_keeps_the_name(api_store):
    moved = api.move_document(api_store.store, "login", "tickets/login.md", api_store.pythonpath)
    assert (moved.model, moved.name, moved.path) == ("TicketDoc", "login", (api_store.root / "tickets" / "login.md").resolve())
    assert not (api_store.root / "login.md").exists()
    assert api.doc_status(api_store.store, "login").exists
    assert _title(api_store, "login") == "Broken login"


def test_move_document_refuses_a_taken_destination_without_moving(api_store):
    (api_store.root / "taken.md").write_text("# Taken\n", encoding="utf-8")
    with pytest.raises(SLDBStoreError, match="already exists"):
        api.move_document(api_store.store, "login", "taken.md", api_store.pythonpath)
    assert (api_store.root / "login.md").exists()


def test_load_runtime_documents_skip_returns_the_sound_ones_and_names_the_invalid(store_with_invalid):
    root, sp, py = store_with_invalid
    loaded = api.load_runtime_documents(sp, py, on_invalid="skip")
    assert isinstance(loaded, api.RuntimeDocuments)
    assert [d.name for d in loaded.documents] == ["c"]
    assert [(i.path, i.model) for i in loaded.invalid] == [("a.md", "Memo"), ("b.md", "Memo")]
    assert all(isinstance(i, api.InvalidDocument) and "status bad is not a status" in i.error for i in loaded.invalid)


def test_load_runtime_documents_raise_names_the_path_of_the_invalid_document(store_with_invalid):
    root, sp, py = store_with_invalid
    with pytest.raises(SLDBValidationError, match=r"(?s)^a\.md:.*status bad is not a status") as raised:
        api.load_runtime_documents(sp, py)
    assert isinstance(raised.value.__cause__, ValidationError)


def test_load_runtime_documents_default_still_returns_a_list(api_store):
    docs = api.load_runtime_documents(api_store.store, api_store.pythonpath)
    assert isinstance(docs, list) and docs
    skipped = api.load_runtime_documents(api_store.store, api_store.pythonpath, on_invalid="skip")
    assert [d.name for d in skipped.documents] == [d.name for d in docs] and skipped.invalid == []


def _retrack(api_store, path="login.md", force=True):
    return api.track_document_file(api_store.store, "TicketDoc", path, "login", api_store.pythonpath, force=force)


def test_track_force_reindexes_a_document_already_tracked_at_the_same_path(api_store):
    """sldb-ui saves the file and re-tracks it with --force (inbox 20261116-162239)."""
    api_store.write_document("login", {**PAYLOAD, "title": "Edited outside"})
    assert _retrack(api_store).name == "login"
    assert _title(api_store, "login") == "Edited outside"
    report = api.check_store(api_store.store, api_store.root, api_store.pythonpath)
    assert report["ok"], report


def test_track_without_force_still_refuses_a_document_already_tracked(api_store):
    with pytest.raises(SLDBStoreError, match="Doc 'login' already tracked."):
        _retrack(api_store, force=False)


def test_track_force_refuses_a_document_tracked_at_another_path_and_names_both(api_store):
    api_store.write_document("other", PAYLOAD)
    with pytest.raises(SLDBStoreError, match=r"already tracked at 'login\.md', not 'other\.md'"):
        _retrack(api_store, "other.md")
    assert _title(api_store, "login") == "Broken login"


def _index_state(api_store):
    return sorted((str(p), p.read_bytes()) for p in api_store.store.rglob("*.yaml") if p.name != "store.yaml")


def test_track_force_twice_without_changes_is_idempotent(api_store):
    """declare_tracked neither duplicates the path nor rewrites store.yaml."""
    declaration = save_declaration(api_store.store, declare_store(api_store.store, api_store.root))
    before = declaration.read_bytes()
    _retrack(api_store)
    state = _index_state(api_store)
    _retrack(api_store)
    assert _index_state(api_store) == state and declaration.read_bytes() == before
    assert before.count(b"login.md") <= 1
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]

FILE:instruccion
Cold-bundle de la tarea task-docs-track-reindex-re-indexa-un-documento-ya-trackeado-validándolo-sin-saltar-el-round-trip-como-for: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

