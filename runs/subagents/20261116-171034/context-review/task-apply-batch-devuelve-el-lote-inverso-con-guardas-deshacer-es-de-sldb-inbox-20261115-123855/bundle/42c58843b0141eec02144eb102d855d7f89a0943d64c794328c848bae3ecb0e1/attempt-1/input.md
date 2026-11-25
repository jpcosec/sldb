FILE:desk/tasks/task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855.md
---
sldb:
  by: agent
  at: '2026-11-16T16:28:54Z'
  authority: generated
  via: save_document_payload
id: task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-apply-batch-guardas-expected-source-hash-bajo-el-cerrojo-del-store-inbox-20261115-022444
pills: []
files:
- src/sldb/api/documents/apply_batch.py
- src/sldb/api/documents/batch_report.py
- tests/api/test_transaction.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# apply_batch devuelve el lote inverso con guardas: deshacer es de sldb (inbox 20261115-123855)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: deshacer es de sldb, no de los consumidores (specIR, deskops, la UI).

## Goal

_Describe the concrete result this task must produce._

BatchReport lleva el lote inverso, en la forma que acepta apply_batch; deshacer = apply_batch(report.inverse).

## Scope

_State what is in scope and what is out of scope._

Pedido del inbox sldb 20261115-123855. Crear X se invierte en borrar X; actualizar en restaurar campos o texto previos; borrar en recrear con el contenido previo; aristas igual sobre sus RelationDoc. Cada operación del inverso lleva expected_source_hash del estado que dejó el lote, así que aplicarlo tras un cambio ajeno se rechaza como ConflictError sin escritura parcial. Procedencia del inverso registrada como cualquier escritura. Decidir si se apoya en los snapshots que Transaction ya tiene para el rollback (pregunta de la nota). Cuando esté, la tool undo_changes del MCP de sldb (tarea sldb mcp) lo expone.

Precisiones (coordinador, 2026-11-16): el inverso se arma con payloads, no con bytes: un documento canónico (el render de su payload) vuelve byte a byte; la procedencia del front matter (sldb.by/at/via) puede cambiar y no cuenta para 'igual'. Si el inverso de un delete encuentra el documento recreado por otro, el rechazo es el SLDBStoreError 'already exists' de la prevalidación, que se documenta como conflicto. Esta tarea depende de la tarea de guardas bajo el cerrojo (022444), que debe estar cerrada antes: el inverso se arma dentro de su lock.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) BatchReport (src/sldb/api/documents/batch_report.py) gana inverse: list[dict] = []. 2) Un módulo nuevo batch_inverse.py en el paquete sldb.api.documents con before(...) que, dentro del lock y antes de la transacción, guarda por cambio el modelo, la ruta, current_payload (de batch_prevalidate) y el source_hash del documento existente; e inverse(...) que, después de la transacción y todavía bajo el lock, arma el lote inverso: create -> delete con expected_source_hash del estado nuevo; update -> update con el payload previo completo y expected_source_hash nuevo; delete -> create con el payload, modelo y ruta previos; move -> move de vuelta con hash nuevo; track <-> untrack. 3) apply_batch (src/sldb/api/documents/apply_batch.py) devuelve BatchReport(saved, inverse) con ese inverso, sin pasar de 10 líneas de lógica; prevalidate_changes sigue siendo nombre de módulo en apply_batch.py (el test del lock lo parchea); batch_prevalidate.py está en 80 líneas y no crece. 4) Tests en tests/api/test_transaction.py: aplicar un lote de create+update+delete y después apply_batch(report.inverse) deja payloads, entradas del índice y bytes de los documentos canónicos iguales a los previos; tocar un documento entre medio hace que el inverso se rechace con ConflictError y sin escritura parcial.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los dos tests nuevos; deshacer = apply_batch(report.inverse) deja el store como antes (payloads e índice iguales; bytes iguales para documentos canónicos); CHANGELOG y commit; aviso a IR anotado en result-summary.md.

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

FILE:src/sldb/api/documents/apply_batch.py
"""Several document changes applied as one: prevalidated together, then written in one
transaction, so a batch applies whole or not at all."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.api.documents.batch_prevalidate import prevalidate_changes
from sldb.api.documents.batch_report import BatchReport
from sldb.api.documents.transaction import Transaction, transaction
from sldb.api.stores.open_store import open_store
from sldb.store.io import store_lock

_ORDER = {"create": 0, "track": 0, "update": 1, "move": 2, "untrack": 3, "delete": 3}
_APPLY: dict[str, Callable[[Transaction, dict[str, Any]], Any]] = {
    "create": lambda tx, c: tx.create(c["model"], c["id"], c["payload"], c.get("path")),
    "track": lambda tx, c: tx.track(c["path"], c["model"], c["id"]),
    "update": lambda tx, c: tx.update(c["id"], c["payload"], c.get("expected_source_hash"), c.get("expected")),
    "move": lambda tx, c: tx.move(c["id"], c["path"]),
    "untrack": lambda tx, c: tx.untrack(c["id"]),
    "delete": lambda tx, c: tx.delete(c["id"]),
}


def apply_batch(store: str | Path | None, changes: list[dict[str, Any]], pythonpath: str | None = None) -> BatchReport:
    """Prevalidate `changes` and apply them in one transaction, creates and tracks first, then
    updates, moves, and last untracks and deletes (request order within each group).

    Args:
        store: The store (path, alias, or None to discover it).
        changes: One dict per change: `id` (the document name, unique in the batch), `action`
            (`create`, `update`, `move`, `delete`, `track`, `untrack`), and by action `model`
            (create, track), `payload` (create, update), `path` (move, track; optional for
            create, else the model's default directory), and the guards `expected_source_hash`
            and `expected` (the full current payload) on any action over a tracked document.
        pythonpath: Directory to import the store's model modules from.

    Returns:
        The ids applied, in order.

    Raises:
        SLDBValidationError: A malformed change, or a payload the model rejects (G4).
        ConflictError: A guard that does not match the document's current state.
        SLDBStoreError: A document or file that exists where it must not, or is missing.
        RollbackError: A failure while applying whose rollback could not restore every file.
        The store lock is held (waiting for it) from prevalidation to the last write, so a
        concurrent process cannot change a guarded document in between.
        Nothing is written when prevalidation raises; a failure while applying rolls the
        whole batch back and re-raises.
    """
    location = open_store(store)
    with store_lock(location.store_path, wait=True):  # guards are checked and writes made under one lock
        plan = sorted(prevalidate_changes(location, changes, pythonpath), key=lambda change: _ORDER[change["action"]])
        with transaction(location.store_path, pythonpath) as tx:
            saved = [_applied(tx, change) for change in plan]
    return BatchReport(saved=saved)


def _applied(tx: Transaction, change: dict[str, Any]) -> str:
    _APPLY[change["action"]](tx, change)
    return change["id"]

FILE:src/sldb/api/documents/batch_report.py
"""What `apply_batch` applied."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BatchReport(BaseModel):
    """The changes a batch wrote, all of them: a batch that fails halfway writes none."""

    saved: list[str] = Field(description="Change ids in the order they were applied: creates and tracks, then updates, moves, and finally untracks and deletes.")

FILE:tests/api/test_transaction.py
"""`sldb.api.transaction` and `sldb.api.apply_batch`: writes visible at once, undone together.

The fixture store is `tests/api/conftest.py`'s (TicketDoc, one tracked document `login`); the
moves test registers a referencing pair of models so an incoming edge can be followed.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import pytest

import sldb.api as api
from sldb.api.documents import transaction_ops
from sldb.core.exceptions import ConflictError, SLDBStoreError, SLDBValidationError
from sldb.store.io.rollback import RollbackError
from sldb.store.io import rollback
from sldb.store.io.shards import load_document_shard
from sldb.store.layout import documents_shard_path

from .conftest import PAYLOAD

REF_MODULE = "sldb_transaction_ref_models"
REF_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Linked(StructuredNLDoc):
    __references__ = ["about"]
    __template__ = "---\\nabout: ⸢rev•about⸥\\n---\\n\\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    about: str = Field(default="", description="Referenced document export id.")
'''


def _files(root: Path) -> dict[str, str]:
    """sha256 of every file under the project (lock files and the on-disk composed index aside): bytes, entries and shards.
    The composed index is a cache H11 keeps outside a transaction (prevalidation reads it before one opens)."""
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file() and "locks" not in p.parts and "composed" not in p.parts}


def _edges(store: Path) -> list:
    return [e.model_dump() for e in api.load_edge_index(store).edges]


def _title(api_store, name: str) -> str:
    return next(d.payload["title"] for d in api.load_runtime_documents(api_store.store, api_store.pythonpath) if d.name == name)


def _entry(api_store, name: str):
    return load_document_shard(documents_shard_path(api_store.store, "TicketDoc", name))


def _failing_create(monkeypatch, at_call: int):
    """`create_document` as the transaction sees it, raising on call number `at_call`."""
    calls, real = {"n": 0}, transaction_ops.create_document

    def injected(*args: Any, **kwargs: Any):
        calls["n"] += 1
        if calls["n"] == at_call:
            raise SLDBValidationError("injected validation failure")
        return real(*args, **kwargs)

    monkeypatch.setattr(transaction_ops, "create_document", injected)


def test_a_batch_whose_third_change_fails_leaves_bytes_entries_and_index_as_before(api_store, monkeypatch):
    before, edges_before = _files(api_store.root), _edges(api_store.store)
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]
    _failing_create(monkeypatch, 3)
    changes = [{"id": f"t{i}", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": f"T{i}"}} for i in (1, 2, 3)]
    with pytest.raises(SLDBValidationError, match="injected"):
        api.apply_batch(api_store.store, changes, api_store.pythonpath)
    assert _files(api_store.root) == before
    assert _edges(api_store.store) == edges_before
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]
    assert not (api_store.root / "t1.md").exists() and api.doc_status(api_store.store, "t1").exists is False


def test_nested_transactions_the_inner_ending_well_and_the_outer_failing_revert_both(api_store):
    before = _files(api_store.root)
    with pytest.raises(RuntimeError, match="outer"):
        with api.transaction(api_store.store, api_store.pythonpath) as outer:
            outer.update("login", {**PAYLOAD, "title": "Outer"})
            with api.transaction(api_store.store, api_store.pythonpath) as inner:
                inner.create("TicketDoc", "inner", {**PAYLOAD, "title": "Inner"}, "inner.md")
            assert (api_store.root / "inner.md").exists()
            raise RuntimeError("outer failed")
    assert _files(api_store.root) == before
    assert _title(api_store, "login") == "Broken login"


def test_an_update_is_read_with_its_new_value_inside_the_transaction(api_store):
    with api.transaction(api_store.store, api_store.pythonpath) as tx:
        saved = tx.update("login", {**PAYLOAD, "title": "Inside"})
        assert "# Inside" in saved.path.read_text(encoding="utf-8")
        assert _title(api_store, "login") == "Inside"
    assert _title(api_store, "login") == "Inside"


def test_write_file_with_another_sha256_fails_without_writing(api_store):
    notes = api_store.root / "notes.txt"
    notes.write_text("v1", encoding="utf-8")
    with pytest.raises(ConflictError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.write_file("notes.txt", b"v2", expected_sha256="0" * 64)
    assert (info.value.ref, info.value.expected, info.value.actual) == ("notes.txt", "0" * 64, hashlib.sha256(b"v1").hexdigest())
    assert notes.read_text(encoding="utf-8") == "v1"


def test_write_file_and_record_are_restored_by_the_rollback(api_store):
    (api_store.root / "own.txt").write_text("mine", encoding="utf-8")
    with pytest.raises(RuntimeError):
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.write_file("new.txt", b"new", expected_sha256=None)
            (api_store.root / tx.record("own.txt")).write_text("changed", encoding="utf-8")
            raise RuntimeError("boom")
    assert not (api_store.root / "new.txt").exists()
    assert (api_store.root / "own.txt").read_text(encoding="utf-8") == "mine"


def test_a_stale_expected_source_hash_is_a_conflict_and_writes_nothing(api_store):
    actual = _entry(api_store, "login").source_hash
    with pytest.raises(ConflictError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.update("login", {**PAYLOAD, "title": "Nope"}, expected_source_hash="stale")
    assert (info.value.ref, info.value.expected, info.value.actual) == ("login", "stale", actual)
    assert _title(api_store, "login") == "Broken login"


def test_the_source_hash_guard_is_checked_before_the_payload_guard(api_store):
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, [{"id": "login", "action": "update", "payload": PAYLOAD, "expected_source_hash": "stale", "expected": {"title": "also stale"}}], api_store.pythonpath)
    assert info.value.expected == "stale"
    with pytest.raises(ConflictError) as info:
        api.apply_batch(api_store.store, [{"id": "login", "action": "update", "payload": PAYLOAD, "expected": {"title": "also stale"}}], api_store.pythonpath)
    assert (info.value.expected, info.value.actual) == ({"title": "also stale"}, PAYLOAD)


def test_a_failure_during_the_rollback_is_raised_with_the_unrestored_paths(api_store, monkeypatch):
    real = rollback._restore

    def refusing(path: Path, data: bytes | None) -> None:
        if path.name == "login.md":
            raise OSError("disk says no")
        real(path, data)

    monkeypatch.setattr(rollback, "_restore", refusing)
    with pytest.raises(RollbackError) as info:
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.update("login", {**PAYLOAD, "title": "Half"})
            raise RuntimeError("original failure")
    assert info.value.unrestored == ["login.md"]
    assert isinstance(info.value.__cause__, RuntimeError) and str(info.value.__cause__) == "original failure"


def test_apply_batch_refuses_everything_when_one_change_is_invalid_and_writes_nothing(api_store):
    before = _files(api_store.root)
    changes = [{"id": "fine", "action": "create", "model": "TicketDoc", "payload": PAYLOAD}, {"id": "login", "action": "update", "payload": {"title": 7}, "expected": PAYLOAD}]
    with pytest.raises(SLDBValidationError, match="login"):
        api.apply_batch(api_store.store, changes, api_store.pythonpath)
    assert _files(api_store.root) == before


def test_apply_batch_orders_creates_updates_moves_untracks_and_deletes(api_store):
    api_store.write_document("loose", PAYLOAD)
    api.track_document_file(api_store.store, "TicketDoc", "loose.md", pythonpath=api_store.pythonpath)
    report = api.apply_batch(api_store.store, [
        {"id": "loose", "action": "delete", "expected": PAYLOAD},
        {"id": "login", "action": "move", "path": "moved/login.md", "expected_source_hash": _entry(api_store, "login").source_hash},
        {"id": "fresh", "action": "create", "model": "TicketDoc", "payload": {**PAYLOAD, "title": "Fresh"}},
        {"id": "untracked", "action": "track", "model": "TicketDoc", "path": str(api_store.write_document("untracked", PAYLOAD).relative_to(api_store.root))},
    ], api_store.pythonpath)
    assert report.saved == ["fresh", "untracked", "login", "loose"]
    assert (api_store.root / "TicketDoc" / "fresh.md").exists() is False and (api_store.root / "fresh.md").exists()
    assert _entry(api_store, "login").path == "moved/login.md" and not (api_store.root / "loose.md").exists()


def test_create_and_move_refuse_a_path_outside_the_project_root(api_store, tmp_path):
    with pytest.raises(SLDBStoreError, match="outside"):
        with api.transaction(api_store.store, api_store.pythonpath) as tx:
            tx.create("TicketDoc", "escaped", PAYLOAD, tmp_path / "escaped.md")
    with pytest.raises(SLDBStoreError, match="outside"):
        api.move_document(api_store.store, "login", tmp_path / "login.md", api_store.pythonpath)


@pytest.fixture
def linked_store(tmp_path: Path):
    """`n1` (Note) referenced by `l1` (Linked.about = Note:n1)."""
    (tmp_path / f"{REF_MODULE}.py").write_text(REF_MODELS, encoding="utf-8")
    root = tmp_path / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("Note", "Linked"):
        api.add_model(store, f"{REF_MODULE}:{model}", str(tmp_path))
    api.create_document(store, "Note", "n1.md", {"title": "n1"}, "n1", str(tmp_path))
    api.create_document(store, "Linked", "l1.md", {"title": "l1", "about": "Note:n1"}, "l1", str(tmp_path))
    yield root, store, str(tmp_path)
    sys.modules.pop(REF_MODULE, None)


def test_move_keeps_the_name_and_the_incoming_edges_keep_resolving(linked_store):
    root, store, py = linked_store
    incoming = [e.model_dump() for e in api.edges_to(store, "Note:n1", "references")]
    assert incoming
    with api.transaction(store, py) as tx:
        moved = tx.move("n1", "notes/n1.md")
    assert (moved.model, moved.name, moved.path) == ("Note", "n1", (root / "notes" / "n1.md").resolve())
    assert not (root / "n1.md").exists()
    assert [e.model_dump() for e in api.edges_to(store, "Note:n1", "references")] == incoming
    assert api.check_store(store, root, py)["ok"]


def test_a_failed_move_puts_the_file_and_the_entry_back(linked_store):
    root, store, py = linked_store
    before = _files(root)
    with pytest.raises(RuntimeError):
        with api.transaction(store, py) as tx:
            tx.move("n1", "notes/n1.md")
            raise RuntimeError("after the move")
    assert _files(root) == before
    assert api.check_store(store, root, py)["ok"]

FILE:instruccion
Cold-bundle de la tarea task-apply-batch-devuelve-el-lote-inverso-con-guardas-deshacer-es-de-sldb-inbox-20261115-123855: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_transaction.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_write_paths_validate.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_serve.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

