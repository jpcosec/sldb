FILE:desk/tasks/task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent.md
---
sldb:
  by: agent
  at: '2026-11-17T15:14:25Z'
  authority: generated
  via: save_document_payload
id: task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/store/documents_dirty.py
- tests/store/test_merkle_operation_cache.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El conjunto de documentos sucios se persiste en .sldb_cache para que el modo incremental funcione entre corridas (V2)

## Rationale

_Explain why this task exists or the business driver behind it._

Para la mejora de velocidad V2, el conjunto de documentos sucios (src/sldb/store/documents_dirty.py) vive solo en la memoria del proceso: cada corrida nueva no sabe qué cambió y el modo incremental no sirve entre procesos. Origen: un análisis de sldb que el supervisor del desk verificó en parte (2026-11-16).

## Goal

_Describe the concrete result this task must produce._

El conjunto de documentos sucios se guarda en .sldb_cache (regenerable, sin versionar) y una corrida nueva lo lee, de modo que una actualización incremental en un proceso nuevo procesa solo lo que cambió; si el archivo falta o está corrupto, se vuelve al cálculo completo sin error.

## Scope

_State what is in scope and what is out of scope._

Entra: persistir y leer el conjunto en .sldb_cache con escritura atómica y bajo el lock del store; invalidarlo cuando cambia la firma del store; tests en tests/store/test_merkle_operation_cache.py o un archivo de tests de store existente (proceso nuevo ve el dirty del anterior; archivo corrupto cae al cálculo completo). CHANGELOG. No entra: versionar el archivo, cambiar qué se considera sucio.

Precisiones (coordinador, bundle-1): el archivo es documents_dirty.json en el directorio .sldb_cache del store que ya usa src/sldb/store/user_cache.py; JSON {"signature": <firma>, "entries": [[modelo, namespace, [nombres...]], ...]}. La firma es la de runtime_cache_signature.signature(s_path) (src/sldb/store/runtime_cache_signature.py) serializada. Escritura atómica (tmp + os.replace) dentro de store_lock (src/sldb/store/io/__init__.py). Carga perezosa: la primera llamada a names() para un store lee el archivo una vez y llena _DIRTY; mark, clear e invalidate reescriben el archivo. Corrupto = no parsea como JSON o no tiene esas claves: se borra el archivo y names() devuelve None (cálculo completo), sin log ni error. La lógica nueva va a un módulo nuevo documents_dirty_persist.py en el paquete sldb.store para que documents_dirty.py no pase de 80 líneas.

Precisiones (coordinador, bundle-2): los tests nuevos van en tests/store/test_merkle_operation_cache.py. La firma se guarda como json.dumps(list(signature), default=str) y se compara por igualdad de esa cadena. Cada mark, clear o invalidate toma store_lock y reescribe el archivo entero. Corrupto también incluye entries con forma distinta de [str, str, [str...]]. El límite de 80 líneas es el que mide tests/test_clean_code_rules.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer documents_dirty.py, user_cache.py y quién consume el conjunto. 2) Implementar persistencia y lectura. 3) Tests con subprocess. 4) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_operation_cache.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_runtime_wiped.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_edges_follow_the_contract.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; CHANGELOG y commit.

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

FILE:src/sldb/store/documents_dirty.py
"""Per-model, per-namespace dirty tracking for `documents_hash`'s `note`/`forget` (PLAN 15
capa 8): one baseline per consumer ("semantic", "sections", ...), so one namespace's catch-up
(`clear`) never erases what another still needs — split out of documents_hash.py to keep
both files under this repo's clean-code line limit."""

from __future__ import annotations

from pathlib import Path

_DIRTY: dict[tuple[str, str, str], set[str]] = {}
_NAMESPACES = ("semantic", "sections", "edges")


def mark(s_path: Path, model_name: str, name: str) -> None:
    for ns in _NAMESPACES:
        if (known := _DIRTY.get((str(s_path), model_name, ns))) is not None:
            known.add(name)


def invalidate(s_path: Path, model_name: str) -> None:
    for ns in _NAMESPACES:
        _DIRTY.pop((str(s_path), model_name, ns), None)


def clear_all() -> None:
    _DIRTY.clear()


def names(s_path: Path, model_name: str, namespace: str) -> set[str] | None:
    known = _DIRTY.get((str(s_path), model_name, namespace))
    return None if known is None else set(known)


def clear(s_path: Path, model_name: str, namespace: str) -> None:
    _DIRTY[(str(s_path), model_name, namespace)] = set()

FILE:tests/store/test_merkle_operation_cache.py
"""PLAN 15 capa 8: after a write, no consumer walks every leaf.

`compose_documents_entries` (the shard glob + per-shard read behind `load_documents_index`)
runs at most once per operation, reused across operations too while the model's hash_b says
nothing moved — never recomposed just because a fresh `new_operation()` started. Semantic and
sections rebuild use the per-document hash map's dirty set to process only a document whose
hash_c actually differs from what its shard reflects, not every document in the model."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.store import documents_hash
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.io.shard_compose import compose_documents_entries


def _write_model(project: Path) -> str:
    package = project / "opcache"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class Note(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n## Body\\n\\n⸢rev•body⸥'\n"
        "    title: str = Field(description='Title')\n"
        "    body: str = Field(description='Body')\n",
        encoding="utf-8",
    )
    return "opcache.models:Note"


def _store(tmp_path: Path, n: int) -> tuple[Path, Path]:
    model_ref = _write_model(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", model_ref, "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    for i in range(n):
        doc = tmp_path / f"note-{i}.md"
        doc.write_text(f"# Opcache note {i}\n\n## Body\n\nBody of opcache note {i}\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(doc), "--model", "Note", "--name", f"note-{i}", "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    return store, tmp_path


class _Args:
    def __init__(self, store: Path, pythonpath: Path):
        self.store, self.pythonpath, self.wait, self.verbose = str(store), str(pythonpath), False, False


def _count_composes(monkeypatch) -> dict[str, int]:
    calls = {"n": 0}
    import sldb.store.documents_hash as dh

    real = dh._compose

    def counted(s_path, model_name):
        calls["n"] += 1
        return real(s_path, model_name)

    monkeypatch.setattr(dh, "_compose", counted)
    return calls


def test_documents_index_composed_at_most_once_per_operation(tmp_path: Path, monkeypatch):
    store, root = _store(tmp_path, 12)
    documents_hash.invalidate(store, "Note")  # drop what tracking the 12 docs already cached
    calls = _count_composes(monkeypatch)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index

    # Several load_documents_index calls in the same operation: one compose, not several.
    for _ in range(5):
        load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 1, calls


def test_documents_index_cache_reused_across_operations_when_nothing_moved(tmp_path: Path, monkeypatch):
    store, root = _store(tmp_path, 12)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index
    load_documents_index(root / load_models_index(m_idx_path).documents_index)  # warm the cache

    calls = _count_composes(monkeypatch)
    documents_hash.new_operation(store)  # a fresh operation, nothing changed in between
    load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 0, calls  # reused verbatim: the model's hash_b agrees with the cache's


def test_invalidate_forces_exactly_one_recompose_with_correct_content(tmp_path: Path, monkeypatch):
    """`invalidate` (a full scan that could have moved anything outside `note`/`forget`, or a
    cache holding something from a completely different, untracked change) always recomposes
    from the shards on disk exactly once, and gets the right content."""
    store, root = _store(tmp_path, 6)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index
    load_documents_index(root / load_models_index(m_idx_path).documents_index)  # warm the cache
    documents_hash.invalidate(store, "Note")

    calls = _count_composes(monkeypatch)
    got = load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 1, calls
    assert {d.name: d.hash_c for d in got.documents} == {d.name: d.hash_c for d in compose_documents_entries(store, "Note")}


def test_a_hand_edit_through_stores_update_needs_no_recompose_next_operation(tmp_path: Path, monkeypatch):
    """`stores update` keeps the cache in step incrementally (`documents_hash.note` per
    document whose hash_c actually moved) rather than invalidating it outright — so a fresh
    operation right after still reuses it verbatim, and its content is correct."""
    store, root = _store(tmp_path, 5)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index
    load_documents_index(root / load_models_index(m_idx_path).documents_index)  # warm the cache

    (root / "note-0.md").write_text("# Opcache note 0\n\n## Body\n\nHand-edited body\n", encoding="utf-8")
    assert update_store(_Args(store, root)) == 0
    documents_hash.new_operation(store)

    calls = _count_composes(monkeypatch)
    got = load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 0, calls  # stores update's own note() calls already kept it current
    assert {d.name: d.hash_c for d in got.documents} == {d.name: d.hash_c for d in compose_documents_entries(store, "Note")}


def test_a_single_write_processes_only_its_own_document_not_every_document(tmp_path: Path, monkeypatch):
    """documents_hash's dirty set (namespaced per consumer) drives semantic/sections rebuild:
    a write to one document among many marks only that one dirty, and a rebuild right after
    reads (`_get`) the cache once but only opens/extracts the dirty document's own shard."""
    from sldb.store import section_rebuild, semantic_doc_contribution

    store, root = _store(tmp_path, 15)
    update_store(_Args(store, root))  # settle semantic/sections for all 15

    calls = {"semantic": 0, "sections": 0}
    real_semantic = semantic_doc_contribution.process_doc
    real_sections = section_rebuild._process_doc_sections

    def counted_semantic(*a, **kw):
        calls["semantic"] += 1
        return real_semantic(*a, **kw)

    def counted_sections(*a, **kw):
        calls["sections"] += 1
        return real_sections(*a, **kw)

    monkeypatch.setattr(semantic_doc_contribution, "process_doc", counted_semantic)
    monkeypatch.setattr(section_rebuild, "_process_doc_sections", counted_sections)

    assert cli_main(["docs", "update", "note-3", '{"title": "Note 3", "body": "changed body"}', "--store", str(store), "--pythonpath", str(root)]) == 0

    assert calls["semantic"] == 1, calls
    assert calls["sections"] == 1, calls


def test_dirty_namespaces_are_independent(tmp_path: Path):
    """One namespace's `clear_dirty` must not erase what another namespace still needs — the
    bug this test guards against: semantic and sections used to share one dirty set, so
    whichever ran first cleared the signal the other relied on to see the very same write."""
    store, root = _store(tmp_path, 3)
    from sldb.store.models import DocumentEntry

    entry = DocumentEntry(name="note-0", path="note-0.md", hash_c="x", hash_d="y")
    documents_hash.clear_dirty(store, "Note", "semantic")
    documents_hash.clear_dirty(store, "Note", "sections")
    documents_hash.note(store, "Note", entry)
    assert documents_hash.dirty_names(store, "Note", "semantic") == {"note-0"}
    assert documents_hash.dirty_names(store, "Note", "sections") == {"note-0"}
    documents_hash.clear_dirty(store, "Note", "semantic")
    assert documents_hash.dirty_names(store, "Note", "semantic") == set()
    assert documents_hash.dirty_names(store, "Note", "sections") == {"note-0"}  # untouched

FILE:instruccion
Cold-bundle de la tarea task-el-conjunto-de-documentos-sucios-se-persiste-en-sldb-cache-para-que-el-modo-incremental-funcione-ent: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_operation_cache.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_runtime_wiped.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_edges_follow_the_contract.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

