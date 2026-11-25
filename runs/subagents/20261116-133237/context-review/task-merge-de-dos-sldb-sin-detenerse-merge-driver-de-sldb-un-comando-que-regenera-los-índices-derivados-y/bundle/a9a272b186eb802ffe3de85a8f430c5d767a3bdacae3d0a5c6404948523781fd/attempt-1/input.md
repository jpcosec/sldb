FILE:desk/tasks/task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y.md
---
sldb:
  by: agent
  at: '2026-11-16T13:12:18Z'
  authority: generated
  via: create_document
id: task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md
depends_on: []
pills: []
files:
- src/sldb/store/io/__init__.py
- src/sldb/api/stores/update_store_indexes.py
- src/sldb/cli/parsers/stores.py
- tests/store/test_update_fault_tolerance.py
- tests/store/test_merkle_shards.py
- docs/versionado-y-colaboracion.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
---

# Merge de dos .sldb sin detenerse: merge driver de sldb, un comando que regenera los índices derivados y un error que dice exactamente qué correr (une la decisión de JP y H2 de velocidad-hooks)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP (2026-11-16, vía supervisor) sobre la tarea task-decisión-de-jp-cómo-se-resuelve-un-conflicto-de-git-en-los-índices-derivados-de-sldb-store-index-yam: hacerlo mucho más explícito, para que los agentes dejen de detenerse al mezclar dos .sldb. Hoy cualquier escritura reescribe .sldb/core/store_index.yaml (store_hash) y .sldb/core/models/<Modelo>.yaml (roster_hash, documents_count), así que dos ramas que tocan documentos distintos siempre chocan ahí aunque los shards se mezclen limpios; sldb stores update empieza con load_store_index (src/sldb/store/io/__init__.py:79), que falla con los marcadores de conflicto, y no hay .gitattributes ni merge driver (en a3514755 se quitaron a mano). Une con H2 de velocidad-hooks-brief.md (merge driver para los índices generados que regenera en vez de marcar conflicto, une los include de store.yaml, aviso en stores init si otra rama ya tiene store, procedimiento documentado) y responde la nota de MEPU 20261115-195033 (un store por rama). Origen: desk/inbox/inbox-note-un-conflicto-de-git-en-los-índices-derivados-de-sldb-no-se-resuelve-con-un-comando.md.

## Goal

_Describe the concrete result this task must produce._

Un merge o rebase de dos ramas que tocaron .sldb termina sin intervención: el merge driver de sldb resuelve store_index.yaml y models/*.yaml y une los include de store.yaml; si aun así quedan índices derivados ilegibles (por ejemplo, marcadores de un merge hecho sin el driver), cualquier comando de sldb que los lea falla con un mensaje que dice el comando exacto a correr, y ese comando los regenera desde los shards. El procedimiento está en AGENTS.md del repo y en la ayuda del CLI.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) `sldb stores rebuild-index`: regenera .sldb/core/store_index.yaml y .sldb/core/models/*.yaml desde los shards de .sldb/core/documents/ y el contrato de cada modelo, sin leer los índices derivados actuales (los ignora si tienen marcadores o no parsean); usa las funciones que ya calculan esos niveles (documents_hash._hash_b, hashing.hash_model_layer, ops.cascade_store_hash; localizarlas con grep). (2) `sldb stores merge-driver %O %A %B %P`: para un archivo derivado (store_index.yaml o models/*.yaml) deja en %A la versión de la rama actual y sale 0 (el índice correcto lo deja rebuild-index); para .sldb/store.yaml une las listas include de las dos ramas (por model, sin duplicar rutas) y conserva lo demás de %A; para cualquier otro archivo sale 1 (conflicto normal). (3) `sldb stores merge-driver --install`: escribe en .gitattributes del repo las líneas `.sldb/core/store_index.yaml merge=sldb`, `.sldb/core/models/*.yaml merge=sldb` y `.sldb/store.yaml merge=sldb`, y configura en .git/config `merge.sldb.driver = sldb stores merge-driver %O %A %B %P` y `merge.sldb.name`; es idempotente. (4) Mensaje de error: donde se carga store_index.yaml o un models/*.yaml (load_store_index y load_models_index en src/sldb/store/io/__init__.py) un archivo con marcadores `<<<<<<<` o que no parsea lanza SLDBStoreError con el texto exacto "<ruta> is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)". (5) `sldb stores init` avisa con una alerta si `git ls-tree` de otra rama local del mismo repo ya tiene .sldb/store.yaml. (6) Documentación: AGENTS.md nuevo en la raíz del repo de sldb con la sección "Merge de .sldb" (los tres comandos y cuándo), la misma sección en docs/versionado-y-colaboracion.md, y el help de los tres subcomandos. (7) Tests en tests/store/test_update_fault_tolerance.py y tests/store/test_merkle_shards.py: rebuild-index sobre un store con store_index.yaml y un models/*.yaml con marcadores deja índices iguales a los de un build limpio; el driver une includes de store.yaml; --install es idempotente; el mensaje de error es exacto. CHANGELOG.md. (8) Al cerrar: responder la nota de MEPU con deskops message send --to mepu explicando el procedimiento. No entra: H1 (hooks install), H3, H4; cambiar qué se versiona (lo hace la tarea de separar .sldb_store y .sldb_cache, que depende de esta); stores build completo como reemplazo de rebuild-index.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/io/__init__.py (load_store_index, load_models_index), src/sldb/api/stores/update_store_indexes.py, src/sldb/cli/parsers/stores.py y el comando de stores en src/sldb/cli/commands/, y las funciones de hash citadas. 2) Implementar rebuild-index en la API (src/sldb/api/stores/) y su subcomando. 3) Implementar merge-driver e --install. 4) Mensaje de error en la carga. 5) Aviso en stores init. 6) AGENTS.md, doc y help. 7) Tests y CHANGELOG. 8) Probar a mano en /dev/shm: dos ramas de un repo de prueba que tocan documentos distintos, merge con el driver instalado, sin conflicto; y merge sin driver, error exacto, rebuild-index, stores check verde.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos de Validation pasan con los tests nuevos; la prueba a mano de dos ramas (con y sin driver) queda en result-summary.md con su salida; AGENTS.md y docs/versionado-y-colaboracion.md tienen la sección "Merge de .sldb"; `sldb stores --help` lista rebuild-index y merge-driver; CHANGELOG y commit; nota respondida a mepu.

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

FILE:desk/atoms/atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past.md
---
id: atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past
title: The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git
  history is the past
five_wh_one_plus: what
tags:
- system:sldb
- topic:store-layout
- topic:journal
---

# The store is .sldb (versioned) plus .sldb_cache (regenerable, ignored); git history is the past

## Answer

An sldb store is two sibling directories at the repo root: .sldb/ holds store.yaml and core/ (store_index, models, documents) and is versioned in git; .sldb_cache/ holds everything derived (edges, sections, semantic, graphs, caches, locks), is git-ignored and is rebuilt by stores build. There is no journal: the past of a store is asked of git history (sldb docs history). stores check fails with stores/core_ignored when core/ or store.yaml are ignored and alerts with stores/cache_not_ignored when the cache line is missing; stores migrate-layout moves an old .sldb/runtime/ into .sldb_cache/. Owner decision of 2026-10-29.

FILE:src/sldb/store/io/__init__.py
from pathlib import Path
from sldb.store.io.lock import StoreIOLock
from sldb.store.io.store_index import StoreIndexIO
from sldb.store.io.models_index import ModelsIndexIO
from sldb.store.io.documents_index import DocumentsIndexIO
from sldb.store.io.sections_index import SectionsIndexIO
from sldb.store.io.semantic_dag import SemanticDAGIO
from sldb.store.io.semantic_index import SemanticIndexIO
from sldb.store.models import DocumentsIndex, ModelsIndex, SectionsIndex, SemanticDAG, SemanticIndex, StoreIndex

def store_lock(store_path: Path, wait: bool = False):
    return StoreIOLock(store_path).acquire(wait)

# -- index cache ---------------------------------------------------------------------------
#
# The three yaml indexes are read by every query and every operation, many times per call
# chain. Each parsed index is kept keyed by its file's path, mtime and size, and returned as
# a deep copy so a caller that mutates and saves it never changes the cached object; the save
# changes the file, and the next load sees a new signature.

from sldb.store.layout import semantic_dag_path as _semantic_dag_path, store_index_path as _store_index_path

_INDEXES: dict[str, tuple[tuple, object]] = {}


def _file_signature(path: Path) -> tuple:
    try:
        st = path.stat()
        return (st.st_mtime_ns, st.st_size)
    except OSError:
        return (0, 0)


def _fast_copy(index):
    """An independent copy of a parsed index, cheaper than `model_copy(deep=True)`: pydantic's
    own dump/validate round-trip instead of the generic recursive `copy.deepcopy` it uses
    internally (PLAN 15 M2) — ~4x faster on a realistic SectionsIndex in this codebase's own
    measurements, and every caller through `_cached` already only reads validated data back."""
    return type(index).model_validate(index.model_dump())


def _cached(path: Path, loader):
    key = str(path)
    sig = _file_signature(path)
    hit = _INDEXES.get(key)
    if hit is None or hit[0] != sig:
        hit = (sig, loader())
        _INDEXES[key] = hit
        _SAVED[key] = (sig, _digest(hit[1]))
    return _fast_copy(hit[1])


def invalidate_index_cache() -> None:
    _INDEXES.clear()
    _SAVED.clear()


_SAVED: dict[str, tuple[tuple, str]] = {}   # path -> (file signature, digest of what was last saved there)


def _digest(index) -> str:
    import hashlib
    import json
    return hashlib.sha256(json.dumps(index.model_dump(), sort_keys=True, default=str).encode()).hexdigest()


def _save_if_changed(path: Path, index, saver) -> None:
    """Write only when the content differs from what the file already holds: a rebuild that
    changes nothing leaves the file, its mtime and every cache keyed on it alone."""
    digest = _digest(index)
    prior = _SAVED.get(str(path))
    if prior is not None and prior[1] == digest and prior[0] == _file_signature(path):
        return
    saver()
    _SAVED[str(path)] = (_file_signature(path), digest)
    _INDEXES[str(path)] = (_file_signature(path), _fast_copy(index))


def load_store_index(store_path: Path) -> StoreIndex:
    return _cached(_store_index_path(store_path), lambda: StoreIndexIO.load(store_path))

def save_store_index(store_path: Path, index: StoreIndex) -> None:
    _save_if_changed(_store_index_path(store_path), index, lambda: StoreIndexIO.save(store_path, index))

def load_models_index(path: Path) -> ModelsIndex:
    return _cached(path, lambda: ModelsIndexIO.load(path))

def save_models_index(path: Path, index: ModelsIndex) -> None:
    _save_if_changed(path, index, lambda: ModelsIndexIO.save(path, index))

def load_documents_index(path: Path) -> DocumentsIndex:
    # PLAN 15 capa 7: composed from per-document shards, not one file at `path` (which may not
    # exist at all once sharded) — see load_sections_index for why the (path, mtime/size)
    # cache above cannot be reused here.
    return DocumentsIndexIO.load(path)

def save_documents_index(path: Path, index: DocumentsIndex) -> None:
    DocumentsIndexIO.save(path, index)

def load_sections_index(path: Path) -> SectionsIndex:
    # PLAN 15 capa 5: composed from per-document shards, not one file at `path` (which may not
    # exist at all once sharded) — the (path, mtime/size) cache above would freeze on its first
    # ever call for this path (signature (0, 0), forever, once there is no file there). Shards
    # already cache themselves, per shard, in sldb.store.io.shards.
    return SectionsIndexIO.load(path)

def save_sections_index(path: Path, index: SectionsIndex) -> None:
    SectionsIndexIO.save(path, index)

def load_semantic_dag(store_path: Path) -> SemanticDAG:
    return _cached(_semantic_dag_path(store_path), lambda: SemanticDAGIO.load(store_path))

def save_semantic_dag(store_path: Path, dag: SemanticDAG) -> None:
    _save_if_changed(_semantic_dag_path(store_path), dag, lambda: SemanticDAGIO.save(store_path, dag))

def load_semantic_index(store_path: Path) -> SemanticIndex:
    # PLAN 15 capa 5: composed from per-document shards, not the one (now legacy) file this
    # cache is keyed on — see load_sections_index for why that cache cannot be reused here.
    return SemanticIndexIO.load(store_path)

def save_semantic_index(store_path: Path, index: SemanticIndex) -> None:
    SemanticIndexIO.save(store_path, index)

FILE:src/sldb/api/stores/update_store_indexes.py
"""Refresh a store's indexes after its Markdown documents were edited outside sldb."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.stores.index_commit import commit_index_updates
from sldb.api.stores.include_losers import untrack_losers
from sldb.api.stores.index_refresh import _process_models
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.api.stores.store_update_report import StoreUpdateReport
from sldb.store.io import load_store_index


def update_store_indexes(store: str | Path | None, pythonpath: str | None = None, wait: bool = False) -> StoreUpdateReport:
    """Untrack the rows a more specific include rule beat (`include_losers`), rehash changed
    documents, save model indexes and rebuild the derived indexes.

    Args:
        store: The store to refresh (path, alias, or None to discover it).
        pythonpath: Import root for the store's model modules.
        wait: Wait for the store lock instead of failing when another writer holds it.

    Returns:
        What was refreshed and which models or documents had to be skipped.
    """
    location = open_store(store)
    untrack_losers(location.store_path, location.project_root, pythonpath)
    return StoreIndexRefresh(location, pythonpath)(wait)


class StoreIndexRefresh:
    """One refresh pass: accumulates skipped models/documents and the indexes to save."""

    def __init__(self, location: StoreLocation, pythonpath: str | None) -> None:
        """Prepare a refresh of the store at `location`, importing models from `pythonpath`."""
        self.location, self.pythonpath = location, pythonpath
        self.skipped_models: list[str] = []
        self.skipped_documents: list[str] = []
        self.pending: list[tuple[Any, Any, Any]] = []
        self.changed: dict[str, list[Any]] = {}

    def __call__(self, wait: bool) -> StoreUpdateReport:
        """Rehash, commit under the store lock (waiting for it if asked) and report."""
        sp, root = self.location.store_path, self.location.project_root
        idx = load_store_index(sp)
        _process_models(idx, root, self.pythonpath, self.skipped_models, self.skipped_documents, self.pending, self.changed)
        sem, sec = commit_index_updates(sp, root, idx, self.pending, self.changed, self.pythonpath, wait)
        return StoreUpdateReport(store_path=sp, skipped_models=self.skipped_models, skipped_documents=self.skipped_documents, semantic_index=sem, sections_index=sec)

FILE:src/sldb/cli/parsers/stores.py
from __future__ import annotations
import argparse

def add_stores_group(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("stores", help="Store lifecycle and federation.")
    sub = p.add_subparsers(dest="stores_command", required=True)
    _init(sub); _add(sub); _remove(sub); _check(sub); _update(sub); _reconcile(sub)
    _semantic_map(sub); _semantic_export(sub); _list(sub); _migrate_hashes(sub)
    _migrate_layout(sub); _declare(sub); _build(sub); _scaffold(sub)

def _init(s):
    i = s.add_parser("init", help="Init .sldb store.")
    i.add_argument("--path", default=".")
    i.add_argument("--force", action="store_true")

def _add(s):
    a = s.add_parser("add", help="Link federated store.")
    a.add_argument("path", help="Store path")
    a.add_argument("--name", help="Store name")
    a.add_argument("--store", help="Local store path")
    a.add_argument("--replace", action="store_true", help="Point a link already recorded under that name here")

def _remove(s):
    r = s.add_parser("remove", help="Remove a store link; refused while a model here is inherited from it.")
    r.add_argument("name", help="Link name")
    r.add_argument("--store", help="Local store path")

def _check(s):
    c = s.add_parser("check", help="Integrity check: reports each finding and its category.")
    c.add_argument("--store", help="Store path")
    c.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    c.add_argument("--quiet", action="store_true", help="Only the PASS/FAIL line, without per-document findings")
    c.add_argument("--apply", action="store_true", help="Run what the store's policy answers to each finding: `reindex` and `hook: <command>`")
    c.add_argument("--pythonpath", help="Project path")

def _update(s):
    u = s.add_parser("update", help="Recompute store hashes.")
    u.add_argument("--wait", action="store_true", help="Wait for store lock if busy")
    u.add_argument("--verbose", action="store_true", help="Print individual skip details")
    u.add_argument("--prune-missing", action="store_true", help="Untrack documents whose file no longer exists (reports which)")
    u.add_argument("--store", help="Store path")
    u.add_argument("--pythonpath", help="Project path")

def _migrate_hashes(s):
    m = s.add_parser("migrate-hashes", help="Rename hash_a..hash_d to store/model/source/content.")
    m.add_argument("--store", help="Store path")

def _migrate_layout(s):
    m = s.add_parser("migrate-layout", help="Move the cache from .sldb/runtime/ to .sldb_cache/ (sibling of .sldb/), drop the journal and fix the root .gitignore.")
    m.add_argument("--store", help="Store path")
    m.add_argument("--force", action="store_true", help="Replace an existing, non-empty .sldb_cache/")

def _reconcile(s):
    r = s.add_parser("reconcile", help="Explicitly reconcile a catalog against a subtree.")
    r.add_argument("--path", default=".", help="Subtree to discover")
    r.add_argument("--catalog", help="Catalog store path; defaults to ~/.sldb")
    r.add_argument("--apply", action="store_true", help="Replace catalog entries with discovered stores")
    r.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _semantic_map(s):
    m = s.add_parser("semantic-map", help="Map equivalent semantic concepts.")
    m.add_argument("concept_a", help="First concept")
    m.add_argument("concept_b", help="Second concept")
    m.add_argument("--store", help="Store path")

def _semantic_export(s):
    e = s.add_parser("semantic-export", help="Export semantic payloads.")
    e.add_argument("--store", help="Store path")
    e.add_argument("--pythonpath", help="Project path")
    e.add_argument("--format", choices=("sldb",), default="sldb", help="Payload contract: sldb_kgdb_semantic_export v1")
    e.add_argument("--encoding", choices=("json", "yaml"), default="json")
    e.add_argument("--output", "-o", default="-", help="Output path or -")
    e.add_argument("--rebuild", action="store_true", help="Refresh semantic and section indexes")

def _list(s):
    l = s.add_parser("list", help="List federated stores.")
    l.add_argument("--store", help="Store path")
    l.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _declare(s):
    d = s.add_parser("declare", help="Print the store.yaml declaration the current index implies.")
    d.add_argument("--store", help="Store path")
    d.add_argument("--write", action="store_true", help="Write it to .sldb/store.yaml")

def _build(s):
    b = s.add_parser("build", help="Rebuild the store from .sldb/store.yaml, the tracked Markdown and the models.")
    b.add_argument("--store", help="Store path")
    b.add_argument("--check", action="store_true", help="Rebuild a scratch copy of the sources and compare, writing nothing here")
    b.add_argument("--format", choices=("text", "json", "yaml"), default="text")

def _scaffold(s):
    b = s.add_parser("scaffold", help="Create the folders and seed files .sldb/store.yaml declares; without --apply, report what is pending.")
    b.add_argument("--store", help="Store path")
    b.add_argument("--apply", action="store_true", help="Write them (default: report only)")
    b.add_argument("--format", choices=("text", "json", "yaml"), default="text")

FILE:tests/store/test_update_fault_tolerance.py
from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest
from sldb.cli import main as cli_main
from pathlib import Path


_SRC = str(Path(__file__).resolve().parent.parent.parent / "src")


def _setup_store(root: Path) -> Path:
    """Create a minimal store with one model for testing."""
    cli_main(["stores", "init", "--path", str(root)])
    store_path = root / ".sldb"
    model_py = root / "models.py"
    model_py.write_text(
        "from pydantic import Field\nfrom sldb import StructuredNLDoc\n"
        "class MyDoc(StructuredNLDoc):\n"
        "    __template__ = '\u2e22rev\u2022title\u2e25'\n"
        "    title: str = Field(description='The title')"
    )
    cli_main(
        [
            "models",
            "add",
            "models:MyDoc",
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )
    doc_path = root / "doc.md"
    cli_main(
        [
            "docs",
            "create",
            "--model",
            "MyDoc",
            "-o",
            str(doc_path),
            '{"title": "Hello"}',
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )
    return store_path, doc_path


def test_store_update_skips_missing_doc(tmp_path, capsys):
    root = tmp_path / "root"
    root.mkdir()
    store_path, doc_path = _setup_store(root)

    doc_path.unlink()

    exit_code = cli_main(
        ["stores", "update", "--store", str(store_path), "--pythonpath", str(root)]
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Skipped missing documents: doc" in captured.out
    assert "Updated store at" in captured.out


_LOCK_HOLDER_SCRIPT = """\
import os, sys, time
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from sldb.store.io import store_lock
sp = Path(sys.argv[2])
ready_file = Path(sys.argv[4])
duration = float(sys.argv[3])
with store_lock(sp):
    ready_file.write_text("ready")
    time.sleep(duration)
"""


def test_store_lock_fails_fast_when_busy(tmp_path):
    """A subprocess holding the store lock causes parallel write to fail fast."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    ready_file = tmp_path / "lock_ready"
    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "5.0", str(ready_file)],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    for _ in range(50):
        if ready_file.exists():
            break
        time.sleep(0.1)

    assert ready_file.exists(), "Subprocess never acquired the lock"

    with pytest.raises(SystemExit) as exc:
        cli_main(
            ["stores", "update", "--store", str(store_path), "--pythonpath", str(root)]
        )

    lock_holder.terminate()
    lock_holder.wait()
    assert "busy" in str(exc.value.code).lower() or exc.value.code != 0


def test_store_lock_wait_blocks_until_released(tmp_path):
    """The --wait flag blocks until the lock is released, then succeeds."""
    root = tmp_path / "root"
    root.mkdir()
    store_path, _doc_path = _setup_store(root)

    ready_file = tmp_path / "lock_ready_wait"
    lock_holder = subprocess.Popen(
        [sys.executable, "-c", _LOCK_HOLDER_SCRIPT, _SRC, str(store_path), "1.5", str(ready_file)],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )

    for _ in range(30):
        if ready_file.exists():
            break
        time.sleep(0.1)

    assert ready_file.exists(), "Subprocess never acquired the lock"

    exit_code = cli_main(
        [
            "stores",
            "update",
            "--wait",
            "--store",
            str(store_path),
            "--pythonpath",
            str(root),
        ]
    )

    lock_holder.wait()
    assert exit_code == 0


def test_atomic_write_cleans_up_temp_file(tmp_path):
    """_atomic_write leaves no .tmp file behind after success."""
    from sldb.store.io.utils import StoreIOUtils
    _atomic_write = StoreIOUtils._atomic_write

    target = tmp_path / "test.yaml"
    _atomic_write(target, "hello: world\n")
    assert target.exists()
    assert target.read_text() == "hello: world\n"
    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []


def test_atomic_write_creates_parent_dirs(tmp_path):
    """_atomic_write creates intermediate directories."""
    from sldb.store.io.utils import StoreIOUtils
    _atomic_write = StoreIOUtils._atomic_write

    target = tmp_path / "a" / "b" / "c.yaml"
    _atomic_write(target, "key: val\n")
    assert target.exists()
    assert target.read_text() == "key: val\n"

FILE:tests/store/test_merkle_shards.py
"""PLAN 15 capa 5: semantic and sections indexes are per-document shards under
`.sldb/runtime/{semantic,sections}/<Model>/<doc>.yaml`. The invariant: the aggregate
`load_semantic_index`/`load_sections_index` compose from shards equals what extracting every
document directly (bypassing the whole index machinery) would produce — after add, change,
and untrack. Also: untracking removes the shard, and a store still in the old single-file
shape is migrated into shards (and the old files removed) the next time it is touched."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.io import load_documents_index, load_models_index, load_sections_index, load_semantic_index, load_store_index
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import (
    project_root,
    sections_index_relpath,
    sections_shards_dir,
    semantic_index_path,
    semantic_shards_dir,
    store_index_path,
)
from sldb.store.migration import migrate_store_layout
from sldb.store.section_rebuild import _extract_sections
from sldb.store.semantic_tags import collect_document_semantic_tags


def _write_model(project: Path) -> str:
    package = project / "shardnotes"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class Note(StructuredNLDoc):\n"
        "    __semantics__ = {'domain': ['notes']}\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n## Body\\n\\n⸢rev•body⸥'\n"
        "    title: str = Field(description='Title')\n"
        "    body: str = Field(description='Body')\n"
        "    semantic_tags: list[str] = Field(default_factory=list, description='Tags')\n",
        encoding="utf-8",
    )
    return "shardnotes.models:Note"


class _Args:
    def __init__(self, store: Path, pythonpath: Path):
        self.store, self.pythonpath, self.wait, self.verbose = str(store), str(pythonpath), False, False


def _store(tmp_path: Path, n: int) -> tuple[Path, Path]:
    model_ref = _write_model(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", model_ref, "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    for i in range(n):
        _create_doc(tmp_path, store, i)
    return store, tmp_path


def _create_doc(root: Path, store: Path, i: int) -> None:
    doc = root / f"note-{i}.md"
    tag = "type.even" if i % 2 == 0 else "type.odd"
    payload = {"title": f"Note {i}", "body": f"Body of note {i}", "semantic_tags": [tag]}
    import json

    assert cli_main(["docs", "create", "--model", "Note", "-o", str(doc), "--name", f"note-{i}", json.dumps(payload), "--store", str(store), "--pythonpath", str(root)]) == 0


def _reference(root: Path, store: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Every tracked Note's tags and section titles, extracted directly — no index, no cache."""
    note_type = resolve_model_ref("shardnotes.models:Note", str(root))
    idx = load_store_index(store)
    m_entry = next(m for m in idx.models if m.name == "Note")
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    tags: dict[str, list[str]] = {}
    sections: dict[str, list[str]] = {}
    for doc in d_idx.documents:
        text = (root / doc.path).read_text(encoding="utf-8")
        tags[doc.name] = collect_document_semantic_tags(note_type, _payload_of(note_type, text))
        sections[doc.name] = [s["title"] for s in _extract_sections(text)]
    return tags, sections


def _payload_of(model_type, text: str) -> dict:
    from sldb.store.codec import default_codec

    return default_codec.extract(model_type, text)


def _composed(root: Path, store: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    semantic = load_semantic_index(store)
    m_idx = load_models_index(root / next(m for m in load_store_index(store).models if m.name == "Note").models_index)
    sections_idx = load_sections_index(root / m_idx.sections_index) if m_idx.sections_index else None
    tags = {name: rec.tags for name, rec in semantic.documents.items()}
    secs = {ds.doc_name: [s.title for s in ds.sections] for ds in (sections_idx.documents if sections_idx else [])}
    return tags, secs


def test_shard_aggregate_equals_direct_extraction(tmp_path: Path):
    store, root = _store(tmp_path, 8)
    update_store(_Args(store, root))
    ref_tags, ref_secs = _reference(root, store)
    got_tags, got_secs = _composed(root, store)
    assert got_tags == ref_tags
    assert got_secs == ref_secs


def test_shard_aggregate_equals_direct_extraction_after_writes(tmp_path: Path):
    store, root = _store(tmp_path, 5)
    update_store(_Args(store, root))
    _create_doc(root, store, 5)  # add
    assert cli_main(["docs", "update", "note-1", '{"title": "Note 1", "body": "changed", "semantic_tags": ["type.odd"]}', "--store", str(store), "--pythonpath", str(root)]) == 0  # change
    assert cli_main(["docs", "untrack", "note-2", "--store", str(store), "--pythonpath", str(root)]) == 0  # untrack
    update_store(_Args(store, root))
    ref_tags, ref_secs = _reference(root, store)
    got_tags, got_secs = _composed(root, store)
    assert got_tags == ref_tags
    assert got_secs == ref_secs
    assert "note-2" not in got_tags and "note-2" not in got_secs


def test_untrack_deletes_the_shards_not_just_the_aggregate_entry(tmp_path: Path):
    store, root = _store(tmp_path, 3)
    update_store(_Args(store, root))
    sem_dir, sec_dir = semantic_shards_dir(store, "Note"), sections_shards_dir(store, "Note")
    assert (sem_dir / "note-1.yaml").exists()
    assert (sec_dir / "note-1.yaml").exists()
    assert cli_main(["docs", "untrack", "note-1", "--store", str(store), "--pythonpath", str(root)]) == 0
    update_store(_Args(store, root))
    assert not (sem_dir / "note-1.yaml").exists()
    assert not (sec_dir / "note-1.yaml").exists()


def test_migrates_a_legacy_single_file_store_into_shards(tmp_path: Path):
    store, root = _store(tmp_path, 3)
    update_store(_Args(store, root))
    ref_tags, ref_secs = _reference(root, store)

    # Simulate a store still on the old single-file shape: write the legacy files by hand,
    # and remove the shards a real capa-5 store would already have.
    m_idx_path = None
    for m in load_store_index(store).models:
        if m.name == "Note":
            m_idx_path = root / m.models_index
    m_idx = load_models_index(m_idx_path)
    legacy_semantic = {"tags": {}, "documents": {n: {"model": "Note", "path": f"note-{n.split('-')[1]}.md", "tags": t} for n, t in ref_tags.items()}}
    semantic_index_path(store).parent.mkdir(parents=True, exist_ok=True)
    semantic_index_path(store).write_text(yaml_dump(legacy_semantic), encoding="utf-8")
    legacy_sections_path = root / sections_index_relpath(store, "Note")
    legacy_sections = {"documents": [{"doc_name": n, "sections": [{"path": t.lower(), "title": t, "breadcrumbs": [t], "semantic_tags": [], "slug": t.lower(), "level": 2} for t in titles]} for n, titles in ref_secs.items()]}
    legacy_sections_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_sections_path.write_text(yaml_dump(legacy_sections), encoding="utf-8")
    import shutil

    shutil.rmtree(semantic_shards_dir(store, "Note").parent, ignore_errors=True)
    shutil.rmtree(sections_shards_dir(store, "Note"), ignore_errors=True)

    assert semantic_index_path(store).exists()
    assert legacy_sections_path.exists()
    migrate_store_layout(store, root)
    assert not semantic_index_path(store).exists()
    assert not legacy_sections_path.exists()
    assert (semantic_shards_dir(store, "Note") / "note-0.yaml").exists()
    got_tags, got_secs = _composed(root, store)
    assert got_tags == ref_tags
    assert got_secs == ref_secs

FILE:docs/versionado-y-colaboracion.md
# Versionado y colaboración en sldb serve

Investigación previa al protocolo de edición concurrente (modelo ProseMirror collab):
una autoridad central que acepta/rebasa según versión. Este documento responde con
evidencia del código actual; no implementa el protocolo.

## 0. Estado del transporte hoy (2026-09-21, rama main)

- Lectura: `GET /health /schema /graph /document?id= /document/ir?id= /edges/* /graph/* /models /lint /semantic-export`.
- Escritura (todos bajo `SAVE_LOCK`, optimistic-lock por payload): `POST /save` (single + batch),
  `POST /docs/create|track|untrack`.
- `/save` usa control optimista por `expected`: el cliente manda el payload que cree que hay
  (`save_plan.update_target`: `existing.payload != expected -> 409`). Detecta el conflicto pero
  no lo resuelve: el segundo cliente debe recargar y rehacer su edición.

## 1. Qué hay hoy (inventario con evidencia)

### Hashes del store (`src/sldb/store/hashing.py`, `store/ops.py`, `store/documents_hash.py`)

| hash | firma | donde vive | cuando rota |
|---|---|---|---|
| `store_hash` (alias deprecado `hash_a`) | root de todo el store: SHA-256 de `[{name, model_hash}]` ordenado (`hash_models_layer`) | store index | cualquier write en cualquier modelo |
| `model_hash` (alias deprecado `hash_b`) | por modelo: SHA-256 de `[{name, source_hash, content_hash}]` ordenado (`hash_document_entries`, order-independent) | models index | cualquier write de cualquier doc del modelo |
| `source_hash` (alias deprecado `hash_c`) | contenido: SHA-256 del texto markdown (`hash_text`) | documento shard | cualquier reescritura del archivo |
| `content_hash` (alias deprecado `hash_d`) | campos: SHA-256 del JSON del payload extraído, claves ordenadas (`hash_payload`/`hash_fields`) | documento shard | solo cuando cambian los campos |

Los cuatro valores conservan su nombre viejo (`hash_a`..`hash_d`) como alias de lectura:
un store viejo sigue cargando y la primera escritura, o `sldb stores migrate-hashes`,
reescribe las claves nuevas. Los valores no cambian con el renombre.

`hash_d` es **función pura del payload**: `hash_payload(codec.extract(model, markdown))`.
Dos prints del mismo payload → mismo `hash_d`; un cambio de campo lo rota siempre. Se calcula en
`ops.track_document` y en `payload_save_steps.write_rendered_document`.

### Journal: retirado el 2026-11-04

El journal (un YAML por write en `.sldb/runtime/journal/`, encadenado por hash) fue retirado:
`.sldb/core/` se versiona entero y el pasado del árbol es la historia de git de sus shards
(`sldb docs history <doc>`, `git log -- .sldb/core/`). Ninguna escritura lo produce,
`sldb stores migrate-layout` borra el que un store tenía y `sldb journal show` imprime el aviso
([architecture/journal-authority.md](architecture/journal-authority.md)).

### Pasos de una escritura (`payload_save_steps.py` + `payload_save.py`)

`save_document_payload`: render (`render_checked`: render + roundtrip obligatorio) →
`write_rendered_document` (escribe `.md`, recalcula `hash_c`/`hash_d` al shard) →
`save_document_indexes` (bajo `store_lock`: shard, `hash_b`, semantic/sections/edges rebuild,
`cascade_hash_a`) → `record(...)` al journal con todo el before/after.

`payload_diff.changed_paths`/`field_label` ya nombran los campos cambiados entre dos payloads
(eso alimenta `entry.field` del journal). `payload_path_writing` ya tiene `deep_get/deep_set/deep_delete`.

## 2. Respuestas con evidencia

### (a) ¿Existe un «número de versión por documento» que sirva como «la versión que el cliente tiene»?

**No existe ningún contador ni versión entera por documento.** No hay campo version en
`DocumentEntry`, ni en `RuntimeDocument`, ni en el documento shard.

**El token que cumple el rol sin inventar nada es `hash_d`** (la firma de los campos):

- Es una función pura del payload → dos clientes con el mismo payload tienen la misma versión;
  el `expected` de hoy (comparación de payloads) coincide exactamente con comparar `hash_d`.
- Ya vive en el documento shard, ya rota en cada write, ya está _before/after_ en el journal.
- El cliente no necesita calcularlo: el servidor lo expone y el cliente lo devuelve tal cual.
- `hash_c` también sirve (firma del contenido) pero es más débil: depende del markdown como bytea,
  no de los campos; un re-render con otro template lo rota sin cambio semántico. `hash_d` es la
  firma semántica y la que alinea con la semántica actual de `/save`.

### (b) ¿El journal permite INVERTIR una escritura o solo auditarla?

**Hoy solo audita.** Evidencia:

- `verify_chain` solo valida la cadena; `read_entries` solo lista. No existe
  función de replay ni de `apply` inverso.
- Para `save_document_payload` la entrada **sí** trae `previous_value` (el payload completo
  anterior) y `hash_d_before`; un single-step undo es *posible a mano* (re-save de
  `previous_value`), pero nada lo ejecuta.
- Para `create_document`/`track_document_file`/`untrack_document` **no alcanza**: `create` y
  `track` no registran payload previo, `untrack` registra solo hashes before (el contenido del
  shard borrado no está en el journal; solo sobrevive el `.md` en disco).
- El journal es opcional (`SLDB_JOURNAL_OFF=1`): no puede ser fuente de verdad del estado.

Conclusión: el journal es **log de auditoría** (quién, qué, antes/después, encadenado y
verificable); habilita undo de un solo paso solo para saves completos, reconstruyendo
manualmente desde `previous_value`, pero no reconstruye estados arbitrarios del store.

### (c) ¿Qué falta para que `/save` acepte `{doc, base_version, changes}`?

Ya existe casi todo; faltan tres piezas pequeñas en el transporte:

1. **Leer la versión actual del doc en el handler de save**: `doc_hashes(store_path, model, doc)`
   (shard) da `hash_d` barato — de hecho hoy se podría comparar `base_version` contra el
   `payload` ya cargado por `load_runtime_documents`. Necesita: comparar
   `base_version != current_hash_d` y en ese caso responder 409 **con el doc completo actual**
   (`serialize_document` + `version`), que ya existe tras esta ronda.
2. **Aplicar `changes` como parches de campos**: el transporte puede resolver `changes`
   = lista de `{op: set|delete, path, value}` contra el payload base del cliente usando
   `deep_set`/`deep_delete`, y luego escribir con `save_document_payload` (render+roundtrip
   ya garantizado). El `field` del journal ya se deduce con `payload_diff`.
3. **Responder la versión resultante**: `hash_d_after` del shard (o del journal del write),
   para que el cliente rebase sin recargar. Hoy `/save` responde `{ok, doc}` sin versión.

Nada del motor del store cambia: sigue siendo `save_document_payload` + journal. El modo
actual `{doc, payload}` (sin `base_version`) debe seguir funcionando (compatibilidad).

## 3. Implementado en esta ronda (solo aditivo)

- `sldb.api.documents.serialize_document` (contrato compartido) ahora emite
  `"version": <hash_d del documento>` — leído del shard vía `api.journal.doc_hashes`.
  Única clave nueva; shape existente intacta.
- Como consecuencia, la versión aparece en:
  - `GET /graph` → cada documento trae `version`.
  - `POST /docs/create|track` (doc recién escrito) y `POST /docs/untrack`
    (versión capturada antes de borrar el shard; bug de orden detectado y corregido por test).
- `GET /document` / `GET /document/ir` **no** incluyen `version`: su envelope lo serializa
  `_flat()` en `src/sldb/cli/serve/document_routes.py`, archivo de otro agente en curso
  (fuera de mi alcance). El cliente del protocolo la toma de `/graph` o de la respuesta de
  los writes; pendiente de coordinar con el dueño de esa ruta.
- Tests: `tests/test_serve.py` +25 (lifecycle completo con versión, rotación de `version`
  tras un `/save`, contratos de error 400/404/409/422).

## 4. Propuesta concreta de protocolo (vuelta siguiente)

```jsonc
// Cliente -> servidor
POST /save
{ "doc": "atom-x",
  "base_version": "<hash_d que el cliente tiene>",
  "changes": [ {"op": "set", "path": "title", "value": "..."},
               {"op": "delete", "path": "obsolete" } ] }

// Servidor, si base_version == hash_d actual del doc (acepta)
200 { "ok": true, "doc": { "...": "...", "version": "<hash_d_after>" } }

// Servidor, si difiere (rebasa)
409 { "ok": false, "error": "Conflicto. Recarga sobre la versión vigente.",
      "doc": { "id": ..., "model_name": ..., "path": ..., "version": "<hash_d actual>",
               "payload": { ... }, "semantic_tags": [...] } }
```

Reglas propuestas:

- El cliente **nunca mergea solo**: ante 409 muestra el payload vigente (va en el cuerpo del
  409) y la UI decide rebasar manualmente (o re-aplicar sus cambios encima y reintentar con la
  nueva `base_version`).
- `changes` se resuelve contra el payload **base del cliente** (no contra el del servidor):
  evita dependencia de orden de llegada; el servidor valida el resultado final con el modelo.
- Tolerancia de reloj nula (no hay timestamps): el `base_version` ES el token de orden.
- Modo legacy `{doc, payload}` sin `base_version` se mantiene (equivalente a `changes=[]`
  con `expected=payload` actual).
- `hash_c` no se usa para el conflicto; queda para detectar ediciones *fuera de banda* del
  `.md` (cambio de hash_c sin cambio de hash_d) en un futuro aviso, no bloqueo.

Trabajo pendiente detectado (fuera de alcance): decidir con el dueño de `document_routes.py`
si el envelope de `/document` debe emitir `version` para que un solo endpoint alimente al
cliente; y que `/save` devuelva la versión resultante (la vuelta siguiente lo necesita).

## 5. Validación real

- `python3 -m pytest tests/test_serve.py -q` → **25 passed**.
- `python3 -m pytest tests/ -q` → **4 failed, 952 passed**; los 4 fallos son **pre-existentes**
  a esta ronda (idénticos a la baseline anterior): `selfdoc/test_preflight.py::test_invalid_existing_document_prevents_any_sync`,
  `test_clean_code_rules[sldb/selfdoc/python_relation_registry.py]`,
  `test_clean_code_rules[sldb/cli/commands/selfdoc.py]`, `test_cli_v2::test_find_supports_physical_and_semantic`.
- Clean-code gate sobre los archivos tocados: OK.
- curl real contra `AgentsKBs/knowledge_psp` (servidor propio en `:8311`, código nuevo;
  el de `:8310` corre un snapshot anterior):
  - `GET /graph` → 168 documentos, cada uno con `version` (ej.
    `atom-antonia-aplicacion -> 272e83a3…c1258ac`).
  - `GET /document?id=atom-antonia-bienvenida` → envelope `{id, model_name, path, payload, semantic_tags, ir}`
    **sin** `version` (ruta de otro agente, ver §3).

FILE:instruccion
Cold-bundle de la tarea task-merge-de-dos-sldb-sin-detenerse-merge-driver-de-sldb-un-comando-que-regenera-los-índices-derivados-y: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_update_fault_tolerance.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_merkle_shards.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py

