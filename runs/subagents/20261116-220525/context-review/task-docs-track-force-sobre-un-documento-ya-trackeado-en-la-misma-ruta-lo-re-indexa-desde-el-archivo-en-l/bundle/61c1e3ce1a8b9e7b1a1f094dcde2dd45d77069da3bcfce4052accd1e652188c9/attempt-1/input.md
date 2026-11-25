FILE:desk/tasks/task-docs-track-force-sobre-un-documento-ya-trackeado-en-la-misma-ruta-lo-re-indexa-desde-el-archivo-en-l.md
---
sldb:
  by: agent
  at: '2026-11-16T21:48:26Z'
  authority: generated
  via: create_document
id: task-docs-track-force-sobre-un-documento-ya-trackeado-en-la-misma-ruta-lo-re-indexa-desde-el-archivo-en-l
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-162239-unclear-docs-track-force-no-fuerza-sigue-diciendo-already-tracked.md
depends_on: []
pills: []
files:
- src/sldb/store/ops.py
- src/sldb/api/documents/track_document_file.py
- tests/api/test_api_documents.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs track --force sobre un documento ya trackeado en la misma ruta lo re-indexa desde el archivo en lugar de fallar con already tracked

## Rationale

_Explain why this task exists or the business driver behind it._

Dos consumidores necesitan re-trackear un documento que ya está en el store: sldb-ui guarda un archivo y hace docs track --force (nota desk/inbox/20261116-162239-unclear-docs-track-force-no-fuerza-sigue-diciendo-already-tracked.md), y pron, que desde su commit 79ddb2d versiona .sldb/core/, corre make world (pron init --world) sobre un clon que ya trae los shards. El job store del CI de sldb sobre c5cb52f0 falla en 'Prepare pron's store' con SLDBStoreError: Doc 'rt-implements' already tracked, lanzado por StoreOperations._pre_check (src/sldb/store/ops.py) aunque track_document_file recibe force=True. Hoy force solo salta la comprobación de round-trip.

## Goal

_Describe the concrete result this task must produce._

track_document_file(..., force=True) y docs track --force sobre un documento ya trackeado con el mismo modelo, nombre y ruta lo re-indexan desde el contenido actual del archivo (shard, índice y aristas al día) y terminan sin error; sin force sigue fallando con already tracked; make world de pron vuelve a pasar contra este sldb.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) con force, si el shard de (modelo, nombre) existe y apunta a la misma ruta del proyecto, track re-indexa ese documento desde el archivo como lo haría una edición externa reconocida, bajo store_lock, y no duplica la entrada en la declaración del store (declare_tracked queda idempotente). (2) con force, si el shard existe pero apunta a otra ruta, falla con SLDBStoreError que nombra las dos rutas (force no mueve documentos; para eso está move). (3) sin force, el comportamiento no cambia. (4) docstring de track_document_file y ayuda de docs track: force también re-indexa un documento ya trackeado en la misma ruta. (5) Tests en tests/api/test_api_documents.py: re-track con force tras editar el archivo deja el payload nuevo y el índice coherente (check_store ok); sin force falla igual que hoy; otra ruta falla y nombra las dos; repetir el track con force sin cambios es idempotente. CHANGELOG.md. No entra: cambiar pron ni el CI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/ops.py (track, _pre_check, _do_track), src/sldb/api/documents/track_document_file.py, la sincronía de la declaración (declare_tracked) y cómo se re-indexa una edición externa (update o sync de un documento trackeado). 2) Pasar force hasta StoreOperations.track y, con force y la misma ruta, re-indexar reutilizando ese camino en vez de lanzar. 3) Tests. 4) Reproducir pron: clonar pron (master) a /dev/shm, crear un venv con este sldb y pron editables (uv venv; uv pip install -e sldb[code,mcp] -e pron[mcp]) y correr make world allí; anotar el resultado en result-summary.md. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; result-summary.md muestra make world de pron con rc 0 contra este sldb en un clon limpio de pron; CHANGELOG y commit; aviso a sldb-ui y a pron.

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
from sldb.store.io.shards import save_document_shard
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
    def track(store_path: Path, project_root: Path, store_index: StoreIndex, model_type: type, model_entry: Any, doc_path: Path, doc_name: str, resolve_model_ref: Callable, pythonpath: str | None = None) -> None:
        StoreOperations._pre_check(store_path, project_root, model_entry, doc_name)
        rel = _get_rel(doc_path, project_root)
        txt = read_source_text(doc_path)  # O_NOFOLLOW; `track_document_file` refused a symlink or an escape first
        with store_lock(store_path):
            StoreOperations._do_track(store_path, project_root, store_index, model_type, model_entry, doc_name, rel, txt, resolve_model_ref, pythonpath)

    @staticmethod
    def _pre_check(store_path, project_root, model_entry, doc_name):
        if documents_shard_path(store_path, model_entry.name, doc_name).exists():
            from sldb.store.exceptions import SLDBStoreError
            raise SLDBStoreError(f"Doc '{doc_name}' already tracked.")

    @staticmethod
    def _do_track(store_path, root, st_idx, m_type, m_entry, d_name, rel_path, text, res_ref, py_path):
        StoreOperations._pre_check(store_path, root, m_entry, d_name)
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


def track_document(store_path: Path, project_root: Path, store_index: StoreIndex, model_type: type, model_entry: Any, doc_path: Path, doc_name: str, resolve_model_ref: Callable, pythonpath: str | None = None) -> None:
    """Track a document in the store and update hashes."""
    StoreOperations.track(store_path, project_root, store_index, model_type, model_entry, doc_path, doc_name, resolve_model_ref, pythonpath)

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
        force: Track without checking that the file round-trips under the model.
        actor: Optional caller label; accepted for compatibility, no longer recorded (the journal was retired on 2026-11-04).

    Returns:
        The tracked document.

    Raises:
        SLDBStoreError: When the model is not registered.
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
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    """The path to track, refused before it is opened when it is a symlink or escapes the root
    (`source_read.refuse_unreadable`): resolving it first would track what it points to."""
    joined = root / Path(raw)
    refuse_unreadable(root, joined)
    return joined.resolve()


def _track(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None) -> None:
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
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

FILE:tests/api/test_api_documents.py
"""`sldb.api` document operations and the `sldb.cli` bridges over them."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import sldb.api as api
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

FILE:instruccion
Cold-bundle de la tarea task-docs-track-force-sobre-un-documento-ya-trackeado-en-la-misma-ruta-lo-re-indexa-desde-el-archivo-en-l: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

