FILE:desk/tasks/task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared.md
---
sldb:
  by: agent
  at: '2026-11-17T06:36:56Z'
  authority: generated
  via: create_document
id: task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-021515-suggestion-read-store-dice-store-not-prepared-para-un-store-inexistente.md
depends_on: []
pills: []
files:
- src/sldb/api/stores/read_store.py
- tests/api/test_api_stores.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# read_store distingue un store inexistente ('store not found') de uno sin preparar ('store not prepared')

## Rationale

_Explain why this task exists or the business driver behind it._

sldb.api.read_store (src/sldb/api/stores/read_store.py) lanza 'store not prepared: run sldb stores update' también cuando el store no existe, porque store_is_prepared devuelve False si falta .sldb o core/store_index.yaml; correr stores update no sirve en ese caso y graph_ui responde 503 guiando mal al operador. Origen: desk/inbox/20261117-021515-suggestion-read-store-dice-store-not-prepared-para-un-store-inexistente.md.

## Goal

_Describe the concrete result this task must produce._

read_store lanza SLDBStoreError 'store not found: <ruta>' cuando no existe el directorio del store, y conserva 'store not prepared: run sldb stores update (<ruta>)' cuando el store existe pero le falta el índice.

## Scope

_State what is in scope and what is out of scope._

Entra: distinguir los dos casos en read_store.py (y en store_is_prepared si hace falta), con el mismo tipo de excepción; tests en tests/api/test_api_stores.py para los dos mensajes. CHANGELOG. No entra: cambiar otros mensajes.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer read_store.py y _resolve_store_arg. 2) Implementar. 3) Tests. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit; aviso a graph_ui.

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

FILE:src/sldb/api/stores/read_store.py
"""Read a store without migrating it: a fresh read-only operation over a prepared store."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_discovery import _find_default_store, _resolve_store_arg
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBStoreError
from sldb.store.documents_hash import new_operation as new_documents_hash_operation
from sldb.store.io import load_store_index
from sldb.store.layout import project_root, store_exists, store_index_path
from sldb.store.migration import _already_canonical
from sldb.store.model_origin import add_owner_import_roots
from sldb.store.runtime_cache_signature import new_operation

NOT_PREPARED = "store not prepared: run `sldb stores update`"


def store_is_prepared(store: Path) -> bool:
    """True when the store exists and its layout is already canonical (nothing to migrate).

    Args:
        store: The store's `.sldb` directory.
    """
    store_path = Path(store)
    if not store_exists(store_path) or not store_index_path(store_path).exists():
        return False
    return _already_canonical(load_store_index(store_path), store_path, project_root(store_path))


def read_store(store: str | Path | None = None) -> StoreLocation:
    """Resolve a store and start a new read-only operation over it, never writing to disk.

    Unlike `open_store`, the layout is never migrated: a reader (a GET) must not rewrite the
    store it reads. Each call starts a new operation, so documents added or removed by another
    process since the previous call are seen.

    Args:
        store: A `.sldb` directory path, the alias of a linked store, or None/"" to discover
            the nearest project store (falling back to the global store, as `mode="readonly"`).

    Returns:
        The resolved store directory and its project root.

    Raises:
        SLDBStoreError: When no store can be found, or when its layout is not canonical
            ("store not prepared: run `sldb stores update`").
    """
    store_path = _resolve_store_arg(str(store)) if store else _find_default_store("readonly")
    root = project_root(store_path)
    if not store_is_prepared(store_path):
        raise SLDBStoreError(f"{NOT_PREPARED} ({store_path})")
    add_owner_import_roots(store_path)  # inherited models import from their owner
    new_operation(store_path)
    new_documents_hash_operation(store_path)
    return StoreLocation(store_path=store_path, project_root=root)

FILE:tests/api/test_api_stores.py
"""`sldb.api` store operations: open, read, link, refresh indexes; and the `sldb.cli` bridges over them."""

from __future__ import annotations

from pathlib import Path

import pytest

from sldb.api import extract_payload, link_store, open_store, read_store, store_is_prepared, track_document_file, update_store_indexes
from sldb.api.stores.indexed_documents import indexed_documents
from sldb.runtime.validation import extract_model_data
from sldb.store.io import load_documents_index, load_models_index, load_semantic_index
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import legacy_semantic_index_path, legacy_store_index_path, store_index_path
from sldb.cli import main as cli_main
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.store.io import load_store_index

from tests.api.conftest import MODULE, PAYLOAD
from tests.store.test_documents_shards import _store


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


def _snapshot(root: Path) -> set[tuple[str, int, int]]:
    """(path, mtime_ns, size) of every file under `root`."""
    return {(str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in root.rglob("*") if p.is_file()}


def _legacy_store(tmp_path: Path) -> Path:
    """A root-level legacy store, built as `tests/store/test_legacy_layout_migration.py` does."""
    (tmp_path / "built").mkdir()
    built, built_root = _store(tmp_path / "built", 3)
    store = tmp_path / "legacy" / ".sldb"
    (store / "models").mkdir(parents=True)
    (store / "documents").mkdir()
    index = load_store_index(built)
    for model in index.models:
        model_index = load_models_index(built_root / model.models_index)
        documents = load_documents_index(built_root / model_index.documents_index)
        (store / "documents" / f"{model.name}.yaml").write_text(
            yaml_dump({"documents": [doc.model_dump() for doc in documents.documents]}), encoding="utf-8"
        )
        data = model_index.model_dump()
        data["documents_index"] = f".sldb/documents/{model.name}.yaml"
        data.pop("sections_index", None)
        (store / "models" / f"{model.name}.yaml").write_text(yaml_dump(data), encoding="utf-8")
        model.models_index = f".sldb/models/{model.name}.yaml"
    legacy_semantic_index_path(store).write_text(yaml_dump(load_semantic_index(built).model_dump()), encoding="utf-8")
    legacy_store_index_path(store).write_text(yaml_dump(index.model_dump()), encoding="utf-8")
    return store


def test_read_store_writes_nothing_on_a_prepared_store(api_store):
    open_store(api_store.store)
    before = _snapshot(api_store.root)
    assert store_is_prepared(api_store.store)
    location = read_store(api_store.store)
    assert (location.store_path, location.project_root) == (api_store.store.resolve(), api_store.root.resolve())
    assert _snapshot(api_store.root) == before


def test_read_store_refuses_an_unprepared_store_and_leaves_it_unmigrated(tmp_path):
    store = _legacy_store(tmp_path)
    before = _snapshot(store.parent)
    assert not store_is_prepared(store)
    with pytest.raises(SLDBStoreError, match="store not prepared: run `sldb stores update`"):
        read_store(store)
    assert _snapshot(store.parent) == before
    assert legacy_store_index_path(store).exists() and not store_index_path(store).exists()


def test_store_is_prepared_is_false_without_a_store(tmp_path):
    assert not store_is_prepared(tmp_path / ".sldb")


def test_read_store_sees_a_document_added_by_another_open_store(api_store):
    first = read_store(api_store.store)
    assert [d["name"] for d in indexed_documents(first.store_path)] == ["login"]
    path = api_store.write_document("logout", {**PAYLOAD, "title": "Broken logout"})
    track_document_file(api_store.store, "TicketDoc", path, "logout", api_store.pythonpath)
    second = read_store(api_store.store)
    assert sorted(d["name"] for d in indexed_documents(second.store_path)) == ["login", "logout"]


def test_extract_payload_matches_extract_model_data(api_store):
    from sldb.api import resolve_model_ref

    model_type = resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    markdown = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert extract_payload(model_type, markdown) == extract_model_data(model_type, markdown)
    assert extract_payload(model_type, markdown)["title"] == PAYLOAD["title"]

FILE:instruccion
Cold-bundle de la tarea task-read-store-distingue-un-store-inexistente-store-not-found-de-uno-sin-preparar-store-not-prepared: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

